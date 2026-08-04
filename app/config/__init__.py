"""
Configuration package for Summify.
Exports commonly used settings and constants.
"""
from app.config.settings import settings
from app.config.constants import *
from app.config.prompts import *
from app.config.logging import setup_logging

__all__ = ["settings", "setup_logging"]