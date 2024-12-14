#!/usr/bin/env python3
"""Auth Module, defining Auth class"""
from db import DB
from bcrypt import gensalt, hashpw, checkpw
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """4. Hash password with bcrypt"""
    return hashpw(password.encode('utf-8'), gensalt())


def _generate_uuid() -> str:
    """9. Generate UUIDs with uuid4"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Awesome Auth Class"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new User in database"""
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                raise ValueError('User {} already exists'.format(
                    email))
        except NoResultFound:
            return self._db.add_user(email,
                                     hashed_password=_hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """Validates login credentials"""
        try:
            user = self._db.find_user_by(email=email)
            return checkpw(password.encode('utf-8'),
                           user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """10. Get session ID"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Return User for Session_id"""
        if session_id is None:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, session_id: str) -> None:
        """Destroys User sesion from db"""
        try:
            user = self._db.find_user_by(session_id=session_id)
            self._db.update_user(user.id, session_id=None)
            return None
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Generates a reset_token for user"""
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates User password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(user.id,
                                 hashed_password=_hash_password(password),
                                 reset_token=None)
        except NoResultFound:
            raise ValueError
        return None
