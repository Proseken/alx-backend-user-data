#!/usr/bin/env python3
"""Database module"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base
from user import User

from typing import (
    Dict, Any
)


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        # self._engine = create_engine("sqlite:///a.db", echo=True)
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Save new user to database, no validations required"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs: Dict[str, Any]) -> User:
        """Query database to find user using kwargs"""
        for k in kwargs.keys():
            if not hasattr(User, k):
                raise InvalidRequestError
        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int,
                    **kwargs: Dict[str, Any]) -> None:
        """Updates User in database with matching user_id"""
        user = self.find_user_by(id=user_id)
        for k in kwargs.keys():
            if not hasattr(User, k):
                raise ValueError
        for k, v in kwargs.items():
            setattr(user, k, v)
        return None
