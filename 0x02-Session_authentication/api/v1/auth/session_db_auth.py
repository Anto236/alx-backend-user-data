#!/usr/bin/env python3
"""
SessionDBAuth module for the API.
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class.
    """
    def create_session(self, user_id=None):
        """
        Create a new UserSession instance and return the Session ID.
        """
        if user_id is None:
            return None

        session_id = super().create_session(user_id)
        if session_id:
            user_session = UserSession()
            user_session.user_id = user_id
            user_session.session_id = session_id
            user_session.save()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve User ID based on the provided Session ID.
        """
        if session_id is None:
            return None

        user_sessions = UserSession.search({'session_id': session_id})
        if user_sessions:
            return user_sessions[0].user_id

    def destroy_session(self, request=None):
        """
        Destroy the UserSession based on the
        Session ID from the request cookie.
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id:
            user_sessions = UserSession.search({'session_id': session_id})
            for user_session in user_sessions:
                user_session.remove()
                return True
        return False
