from pydantic import BaseModel
from typing import Optional, List, Union

# /crawler에 대한 파라미터
class tdingModel(BaseModel):
    userMessages : list = []
    assistantMessages : list = []


class davinciModel(BaseModel):
    userMessages : str
    question: str

class gongowlModel(BaseModel):
    userMessages : str 
    id : str