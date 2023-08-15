#!/usr/bin/env python3
""" Authentication helper class
"""
from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> bytes:
    """
       Hashes the input password with a salt using bcrypt
    """
    return hashpw(password.encode('utf-8'), gensalt())
