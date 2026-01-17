from .models import User
from .security import verify_password

def get_user(username:str, user_id:int=None, db:None=None):
    if username:
        user = db.query(User).filter(User.username==username).first()
    elif user_id:
        user = db.query(User).filter(User.id==user_id).first()
    if user:
        return user
    return None


def authenticate(username:str, password:str=None, db:None=None):
    user = get_user(username=username, db=db)
    if user:
        is_password_correct = verify_password(password, user.password)
        if is_password_correct:
            return user
    return None