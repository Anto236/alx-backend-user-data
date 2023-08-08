#!/usr/bin/env python3
"""Auth class"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    a class to manage the API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Placeholder method for authentication requirement """
        return False

    def authorization_header(self, request=None) -> str:
        """ Placeholder method for retrieving authorization header """
        return None

    def current_user(self, request=None):
        """ Placeholder method for getting the current user """
        return None
