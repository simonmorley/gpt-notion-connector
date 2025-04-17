import os
from flask import Blueprint, request, jsonify, current_app
from .notion_sync import publish_to_notion, update_notion_page

external_bp = Blueprint('external_bp', __name__)

@external_bp.route('/publish_to_notion', methods=['POST'])
def handle_publish():
    if current_app.config['TEST_MODE']:
        print('TEST MODE ENABLED — bypassing token check')

    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    email = data.get('user_email')
    page_id = data.get('page_id')

    try:
        if page_id:
            print(f'Updating existing Notion page {page_id}')
            result = update_notion_page(page_id, content)
        else:
            print('Publishing new Notion page')
            result = publish_to_notion(title, content, email)

        return jsonify({
            'status': 'published',
            'notion_url': result['url'],
            'page_id': result['id']
        }), 200

    except Exception as e:
        print(f'Notion sync error: {e}')
        return jsonify({'error': str(e)}), 500

