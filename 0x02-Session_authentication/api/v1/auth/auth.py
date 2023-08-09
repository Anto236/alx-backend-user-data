#!/usr/bin/env python3
"""Auth class"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    a class to manage the API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Check if authentication is required for the given path """
        if path is None:
            return True

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        for excluded_path in excluded_paths:
            if excluded_path.endswith("*") and \
                    path.startswith(excluded_path[:-1]):
                return False
            if path.startswith(excluded_path) or \
                    path == excluded_path.rstrip('/'):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Retrieve the Authorization header from the request """
        if request is None or "Authorization" not in request.headers:
            return None

        return request.headers.get("Authorization")

    def current_user(self, request=None):
        """ Placeholder method for getting the current user """
        return None
