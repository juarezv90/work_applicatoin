import os
from pathlib import Path
base = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    db_path = Path(os.getenv('APPDATA'))/'workapp'/'workstation.db'
    db_path.parent.mkdir(parents=True, exist_ok=True)
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
    TEMPLATE_AUTO_RELOAD = True