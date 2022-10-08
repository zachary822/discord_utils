from enum import Enum


class CommandType(str, Enum):
    CHAT_INPUT = 1
    USER = 2
    MESSAGE = 3
