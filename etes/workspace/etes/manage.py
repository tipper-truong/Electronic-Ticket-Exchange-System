# Set the path or starting point
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask.ext.script import Manager, Server
from etes import app

manager = Manager(app)

# Turn on debugger by default and reloader
# Runs the server -> command: python manage.py runserver
# Always run the MySQL Database  -> mysql-ctl cli
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = os.getenv('IP', '0.0.0.0'),
    port = int(os.getenv('PORT', 5000)))
)

if __name__ == "__main__":
    manager.run()