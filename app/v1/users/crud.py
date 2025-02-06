from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from .models import User
from .schemas import UserSchema
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    
    :param plain_password: The plain text password to verify.
    :param hashed_password: The hashed password to verify against.
    :return: True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hash a plain password.
    
    :param password: The plain text password to hash.
    :return: The hashed password.
    """
    return pwd_context.hash(password)

def get_user(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of User records with pagination.
    
    :param db: The database session.
    :param skip: The number of records to skip.
    :param limit: The maximum number of records to return.
    :return: A list of User records.
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return jsonable_encoder(users)

def get_user_by_id(db: Session, user_id: int) -> User:
    """
    Retrieve a single User record by ID.
    
    :param db: The database session.
    :param user_id: The ID of the user to retrieve.
    :return: The User record, or None if not found.
    """
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> User:
    """
    Retrieve a single User record by username.
    
    :param db: The database session.
    :param username: The username of the user to retrieve.
    :return: The User record, or None if not found.
    """
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserSchema) -> User:
    """
    Create a new User record in the database.
    
    :param db: The database session.
    :param user: The UserSchema object containing user details.
    :return: The created User record.
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

def authenticate_user(db: Session, username: str, password: str) -> User:
    """
    Authenticate a user by username and password.
    
    :param db: The database session.
    :param username: The username of the user to authenticate.
    :param password: The plain text password of the user to authenticate.
    :return: The authenticated User record, or None if authentication fails.
    """
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user