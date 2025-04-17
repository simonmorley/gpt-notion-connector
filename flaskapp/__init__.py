import os
from flask import Flask
from .external_bp import external_bp

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        NOTION_TOKEN=os.getenv('NOTION_TOKEN'),
        NOTION_PARENT_PAGE_ID=os.getenv('NOTION_PARENT_PAGE_ID'),
        TEST_MODE=os.getenv('TEST_MODE', 'false').lower() == 'true'
    )
    app.register_blueprint(external_bp, url_prefix='/gpt')
    return app

