from typing import List, Any
from .Content import Content

class Section:
    def __init__(self, title: str, level: int = 1):
        self.__level: int = level
        self.__title: str = title
        self.__contents: List[Any[Section, Content]] = list()
        
    def add_content(self, new_block: Content):
        self.__contents.append(new_block)
        
    def __repr__(self) -> str:
        text = f"Section(Level: {self.__level}, Title: {self.__title})"
        for content in self.__contents:
            text += "\n" + "\t" * (1 + self.__level) + f"{content}"
        return text