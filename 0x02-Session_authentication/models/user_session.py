#!/usr/bin/env python3
"""
UserSession module for the API.
"""
from models.base import Base


class UserSession(Base):
    """
    UserSession class.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Constructor of UserSession class.
        """
        super().__init__(*args, **kwargs)
        self.user_id = ""
        self.session_id = ""
