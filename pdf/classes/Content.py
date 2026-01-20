from typing import Optional

class Content:
    def __init__(self, raw_text: Optional[str]):
        if not raw_text:
            raise ValueError("Контент заполнения не может быть пустым!")
        
        self.__text = raw_text
    
    
    def get_text(self) -> str:
        return self.__text


    def set_text(self, new_text: str) -> None:
        self.__text = new_text
    
    
    def __repr__(self) -> str:
        return f"Content(Text Length: {len(self.__text)} characters. Prev: {self.__text[:20]}...)"