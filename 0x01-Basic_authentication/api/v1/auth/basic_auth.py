#!/usr/bin/env python3
"""Basic authentication module for the API"""
import base64
from api.v1.auth.auth import Auth


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
