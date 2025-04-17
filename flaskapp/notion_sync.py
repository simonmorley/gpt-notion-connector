import os
import requests
import markdown
from markdown.extensions import Extension
from bs4 import BeautifulSoup

NOTION_API = 'https://api.notion.com/v1/pages'
NOTION_VERSION = '2022-06-28'
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
NOTION_PARENT_PAGE_ID = os.getenv('NOTION_PARENT_PAGE_ID')

def markdown_to_notion_blocks(markdown_text):
    html = markdown.markdown(markdown_text, extensions=['tables'])
    soup = BeautifulSoup(html, 'html.parser')
    blocks = []

    for el in soup.children:
        text = el.get_text(strip=True)
        if not text:
            continue

        tag = el.name
        if tag in ('h1', 'h2', 'h3'):
            level = int(tag[-1])
            blocks.append(make_heading(text, level))
        elif tag == 'ul':
            blocks.extend(make_list(el, bulleted=True))
        elif tag == 'ol':
            blocks.extend(make_list(el, bulleted=False))
        elif tag == 'blockquote':
            blocks.append(make_quote(text))
        elif tag == 'pre':
            blocks.append(make_code(text))
        else:
            blocks.append(make_paragraph(text))

    return blocks

def make_paragraph(text):
    return {
        'object': 'block',
        'type': 'paragraph',
        'paragraph': {
            'rich_text': [{
                'type': 'text',
                'text': {'content': text[:2000]}
            }]
        }
    }

def make_heading(text, level):
    return {
        'object': 'block',
        'type': f'heading_{level}',
        f'heading_{level}': {
            'rich_text': [{
                'type': 'text',
                'text': {'content': text[:2000]}
            }]
        }
    }

def make_list(el, bulleted=True):
    item_type = 'bulleted_list_item' if bulleted else 'numbered_list_item'
    return [
        {
            'object': 'block',
            'type': item_type,
            item_type: {
                'rich_text': [{
                    'type': 'text',
                    'text': {'content': li.get_text(strip=True)[:2000]}
                }]
            }
        }
        for li in el.find_all('li')
    ]

def make_quote(text):
    return {
        'object': 'block',
        'type': 'quote',
        'quote': {
            'rich_text': [{
                'type': 'text',
                'text': {'content': text[:2000]}
            }]
        }
    }

def make_code(text):
    return {
        'object': 'block',
        'type': 'code',
        'code': {
            'rich_text': [{
                'type': 'text',
                'text': {'content': text[:2000]}
            }],
            'language': 'plain text'
        }
    }

def chunk_blocks(blocks, chunk_size=100):
    for i in range(0, len(blocks), chunk_size):
        yield blocks[i:i + chunk_size]

def update_notion_page(page_id, content):
    url = f'https://api.notion.com/v1/blocks/{page_id}/children'
    headers = {
        'Authorization': f'Bearer {NOTION_TOKEN}',
        'Notion-Version': NOTION_VERSION,
        'Content-Type': 'application/json'
    }
    new_blocks = markdown_to_notion_blocks(content)
    for chunk in chunk_blocks(new_blocks):
        resp = requests.patch(url, headers=headers, json={'children': chunk})
        resp.raise_for_status()
    notion_url = f'https://www.notion.so/{page_id.replace("-", "")}'
    print(f'Replaced Notion page content: {notion_url}')
    return {'id': page_id, 'url': notion_url}

def publish_to_notion(title, content, user_email):
    headers = {
        'Authorization': f'Bearer {NOTION_TOKEN}',
        'Notion-Version': NOTION_VERSION,
        'Content-Type': 'application/json'
    }
    all_blocks = markdown_to_notion_blocks(content)
    first_chunk, *rest = list(chunk_blocks(all_blocks))
    payload = {
        'parent': {'page_id': NOTION_PARENT_PAGE_ID},
        'properties': {'title': [{'text': {'content': title}}]},
        'children': first_chunk
    }
    resp = requests.post(NOTION_API, headers=headers, json=payload)
    resp.raise_for_status()
    page = resp.json()
    page_id = page['id']
    notion_url = f'https://www.notion.so/{page_id.replace("-", "")}'

    for chunk in rest:
        url = f'https://api.notion.com/v1/blocks/{page_id}/children'
        r = requests.patch(url, headers=headers, json={'children': chunk})
        r.raise_for_status()

    print(f'Created Notion page for {user_email}: {notion_url}')
    return {'id': page_id, 'url': notion_url}

