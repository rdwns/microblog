from app import create_app, db
from app.models import User, Post

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}





# from app import create_app, db
# from app.models import User, Post

# app = create_app()

# @app.shell_context_processor
# def make_shell_context():
#     users = User.query.all()


#     # # listusers = inspect(model)
#     # # for column in listusers.c

#     # # listusers = Table('user', meta)

#     # listusers = []

#     # for user in users:
#     #     listusers.append(user.id)
#     #     listusers.append(user.username)
#     #     listusers.append(user.email)
#     #     listusers.append(user.avatar(32))




#     return {'db' : db, 'User' : User, 'Post' : Post, 'users' : users }

