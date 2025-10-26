"""
MERCUR-E GitHub Bot
AI-powered GitHub automation with FastAPI and FastMCP
"""

__version__ = "1.0.0"
__author__ = "Claude Sonnet"
__license__ = "MIT"

from .config import settings
from .commands import CommandHandler, CommandParser

__all__ = [
    "settings",
    "CommandHandler",
    "CommandParser",
]
