#!/usr/bin/env python3
"""
Authentication systems: Basic authentication and Session authentication
"""
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from os import getenv
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from models.user import User


class SessionExpAuth(SessionAuth):
    """
    Session authentication class with session expiration.
    Inherits from SessionAuth.
    """

    def __init__(self):
        """Initialize SessionExpAuth instance with session duration."""
        session_duration_str = getenv("SESSION_DURATION", "0")
        try:
            self.session_duration = int(session_duration_str)
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Create a session with session expiration.

        Args:
            user_id (str): User ID.

        Returns:
            str: Session ID.
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Get user ID for a given session ID with session expiration.

        Args:
            session_id (str): Session ID.

        Returns:
            str: User ID if valid session, else None.
        """
        if session_id is None:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if not session_dict:
            return None
        if self.session_duration <= 0:
            return session_dict.get("user_id")
        created_at = session_dict.get("created_at")
        if not created_at:
            return None
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time <= datetime.now():
            return None
        return session_dict.get("user_id")
