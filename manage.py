
from flask_script import Manager, Server, Shell
from MagicPress import create_app, db
from MagicPress.blog.models import Article, Tag, Category, Comment
from MagicPress.auth.models import User
from flask_migrate import MigrateCommand



app = create_app()
manager = Manager(app)




def make_shell_context():
    return dict(app=app, db=db, User=User, Article=Article, Tag=Tag, Category=Category, Comment=Comment)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
if __name__ == '__main__':
    app.run()
