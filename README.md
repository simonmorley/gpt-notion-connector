# Notion Sync API

A lightweight Flask API that converts Markdown to Notion blocks and either publishes a new page or updates an existing one using the Notion API.

## Features

- Converts Markdown to Notion-compatible block format
- Publishes new Notion pages under a specified parent
- Updates existing Notion pages by replacing all content
- Built for easy deployment and open-source reuse
- Supports test mode bypass for local/dev use

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/notion-sync-api.git
cd notion-sync-api
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Set environment variables

Copy the example environment config:

```bash
cp .env.example .env
```

Then edit `.env` and fill in your values:

```
NOTION_TOKEN=your_notion_integration_token
NOTION_PARENT_PAGE_ID=your_parent_page_id
TEST_MODE=false
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the app

```bash
export FLASK_APP=flaskapp:create_app
export FLASK_ENV=development  # optional
flask run
```

The app will be available at:  
`http://127.0.0.1:5000/gpt/publish_to_notion`

## API Usage

### Endpoint

```
POST /gpt/publish_to_notion
```

### Request body (JSON)

| Field        | Type   | Required | Description                                   |
|--------------|--------|----------|-----------------------------------------------|
| `title`      | string | ✅       | Title for the Notion page                     |
| `content`    | string | ✅       | Markdown content to publish                   |
| `user_email` | string | ✅       | Email address for internal logging            |
| `page_id`    | string | ❌       | If provided, updates the specified Notion page |

### Example request

```bash
curl -X POST https://api.yosquire.com/_x/gpt/publish_to_notion \
  -H "Content-Type: application/json" \
  -d '{
    "title": "MealMate - Product Requirements Document",
    "content": "This is a test PRD. It should land in Notion.",
    "user_email": "simon.morley@mac.com"
  }'
```

### Successful response

```json
{
  "status": "published",
  "notion_url": "https://www.notion.so/xxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "page_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

### Error response

```json
{
  "error": "Detailed error message"
}
```

## License

MIT
