from flask_script import Server, Shell, Manager, Command
from flask_migrate import MigrateCommand
from surveys import create_app


manager = Manager(create_app)

manager.add_option("-c", "--config", dest="configfile", required=False)
manager.add_command("runserver", Server())
manager.add_command("shell", Shell())
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()