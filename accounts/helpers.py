from .models import User, Role
from .security import *
from sqlalchemy.orm import selectinload, Session

def get_user(username:str=None, user_id:int=None, db:Session=None):
    print('step 5', username)
    
    """Гирифтани корбар аз базаи додаҳо"""
    if not db:
        return None
    print('step 6')
    
    q = db.query(User).options(
        selectinload(User.permissions),
        selectinload(User.roles).selectinload(Role.permissions))
    print('step 7' , q)
    if username:
        print('step 8')
        user = q.filter(User.username==username).first()
        return user
    elif user_id:
        user = q.filter(User.id==user_id).first()
        return user
    print(user)
    return None


def authenticate(username:str, password:str=None, db:Session=None):
    """Аутентификатсияи корбар"""
    user = get_user(username=username, db=db)
    if user and password:
        is_password_correct = verify_password(password, user.password)
        if is_password_correct:
            return user
    return None


def _create_user_object(data):
    """Эҷоди объекти корбар аз додаҳо"""
    data["password"] = hash_password(data["password"])
    data.pop("confirm_password", None)  # Безопасно удаляем
    new_user = User(**data)
    return new_user


def _create_user(data, db):
    """Сохтани корбар дар базаи додаҳо"""
    try:
        user = _create_user_object(data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise e


def create_user(data, db):
    """Функсияи умумӣ барои сохтани корбар"""
    data = data.model_dump()
    user = _create_user(data, db)
    return user


def create_superuser(data, db):
    """Сохтани суперкорбар"""
    data = data.model_dump()
    data.update({
        "is_staff": True,
        "is_superuser": True
    })
    user = _create_user(data, db)
    return user