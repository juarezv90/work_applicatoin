from app import app,db
from flaskwebgui import FlaskUI
import os
from pathlib import Path

def initialize_database():
    with app.app_context():
        db_dir = Path(os.getenv('APPDATA'))/'workapp'
        db_dir.mkdir(parents=True, exist_ok=True)
        
        db.create_all()


ui = FlaskUI(app=app,
             server="flask", 
             width=1200,
             height=800)

if __name__ == "__main__":
    initialize_database()
    ui.run()