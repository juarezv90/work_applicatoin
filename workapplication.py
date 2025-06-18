from app import app
from flaskwebgui import FlaskUI

ui = FlaskUI(app=app,
             server="flask", 
             width=1200,
             height=800)

if __name__ == "__main__":
    ui.run()