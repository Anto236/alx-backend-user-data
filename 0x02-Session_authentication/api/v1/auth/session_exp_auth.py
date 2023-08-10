#!/usr/bin/env python3
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from models.user import User
from os import getenv


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class inherits from SessionAuth"""
    def __init__(self):
        """Initialize session duration based on environment variable"""
        session_duration_str = getenv("SESSION_DURATION", "0")
        try:
            self.session_duration = int(session_duration_str)
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a new session with an expiration date"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve the user ID based on session ID, considering expiration"""
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
