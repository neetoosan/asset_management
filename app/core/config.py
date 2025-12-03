import os
from pathlib import Path
from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()
        
        # Database configuration
        self.DATABASE_URL = os.getenv(
            "DATABASE_URL",
            "postgresql://neetoosan_user:ENLbEYJqc7JwS00dyzsUWSkoVAmqhIbR@dpg-d4eobbbe5dus73fjv2tg-a.oregon-postgres.render.com/neetoosan"
        )
        
        # Application settings
        self.APP_NAME = "Asset Management System"
        self.APP_VERSION = "0.1.0"
        
        # Paths
        self.BASE_DIR = Path(__file__).parent.parent.parent
        self.UI_DIR = self.BASE_DIR / "app" / "gui" / "ui"