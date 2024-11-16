#!/usr/bin/env python3
"""3. Auth class Definition"""
from typing import (
    List,
    TypeVar
)


class Auth:
    """Manages the API authentication"""

    def require_auth(self, path: str,
                     excluded_paths: List[str]) -> bool:
        """require_auth public method"""
        if any([path is None, excluded_paths is None]):
            return True
        if path[-1] != '/':
            path = path + '/'
        if any([path in excluded_paths, path[:-1] in excluded_paths]):
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorization_header public method"""
        if request is None:
            return None
        if request.authorization is None:
            return None
        return str(request.authorization)

    def current_user(self, request=None) -> TypeVar('User'):
        """current_user public method"""
        return None
