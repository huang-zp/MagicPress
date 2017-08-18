
from MagicPress import user_datastore, db
from flask_security import utils
from MagicPress.blog import blog


@blog.before_first_request
def before_first_request():

    user_datastore.find_or_create_role(name='admin', description='Administrator')

    encrypted_password = utils.hash_password('password')

    if not user_datastore.get_user('admin@example.com'):
        user_datastore.create_user(email='admin@example.com', password=encrypted_password)

    db.session.commit()

    user_datastore.add_role_to_user('admin@example.com', 'admin')
    db.session.commit()