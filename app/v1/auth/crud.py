from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from .models import User
from .schemas import UserSchema
from .utils import verify_password, get_password_hash

def get_user(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of User records with pagination.
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return jsonable_encoder(users)

def get_user_by_id(db: Session, user_id: int):
    """
    Retrieve a single User record by ID.
    """
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    """
    Retrieve a single User record by username.
    """
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserSchema):
    """
    Create a new User record in the database.
    """
    hashed_password = get_password_hash(user.password)
    db_user = User(
        name=user.name,
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return jsonable_encoder(db_user)

def update_user(db: Session, user_id: int, name: str = None, description: str = None, image: str = None):
    """
    Update an existing User record in the database.
    """
    _user = db.query(User).filter(User.id == user_id).first()
    if not _user:
        raise ValueError(f"User with id {user_id} does not exist")

    if name is not None:
        _user.name = name
    if description is not None:
        _user.description = description
    if image is not None:
        _user.image = image

    db.commit()
    db.refresh(_user)
    return jsonable_encoder(_user)

def remove_user(db: Session, user_id: int):
    """
    Delete a User record by ID.
    """
    _user = get_user_by_id(db=db, user_id=user_id)
    if not _user:
        raise ValueError(f"User with id {user_id} does not exist")

    db.delete(_user)
    db.commit()
    return jsonable_encoder(_user)

def authenticate_user(db: Session, username: str, password: str):
    """
    Authenticate a user by username and password.
    """
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user