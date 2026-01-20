from typing import List
from .Section import Section

class Document:
    def __init__(self, title: str = "Untitled Document"):
        self.__title: str = title
        self.__sections: List[Section] = []
        
    def get_sections(self) -> List[Section]:
        return self.__sections
    
    def add_section(self, new_section: Section):
        self.__sections.append(new_section)
        
    def add_sections(self, sections_lst: List[Section]):
        self.__sections.extend(sections_lst)
        
    def __repr__(self) -> str:
        text = f"Document({self.__title})"
        for section in self.__sections:
            text += f"\n\t{section}"
        return text