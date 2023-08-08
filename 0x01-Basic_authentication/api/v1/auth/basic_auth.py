#!/usr/bin/env python3
"""Basic authentication module for the API"""
import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import Tuple, TypeVar


class BasicAuth(Auth):
    """Basic authentication class.
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extracts the Base64 part of the Authorization
           header for Basic Authentication.
        """
        if authorization_header is None or not \
                isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        base64_part = authorization_header[len("Basic "):]
        return base64_part

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decodes a Base64 string and returns the decoded
           value as UTF-8 string.
        """
        if base64_authorization_header is None or not \
                isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_value = decoded_bytes.decode('utf-8')
            return decoded_value
        except base64.binascii.Error:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Extracts user email and password
           from the decoded Base64 value.
        """
        if decoded_base64_authorization_header is None \
                or not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ":" not in decoded_base64_authorization_header:
            return None, None

        email, password = decoded_base64_authorization_header.split(":", 1)
        return email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Retrieves a user based on the user's authentication credentials.
        """
        if type(user_email) == str and type(user_pwd) == str:
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the user from a request.
        """
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)
