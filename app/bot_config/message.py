from app.handlers2 import left_chat_member
from telegram.ext import Filters


messages = [(Filters.status_update.left_chat_member, left_chat_member)]
