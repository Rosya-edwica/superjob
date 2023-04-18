from typing import NamedTuple


class Salary(NamedTuple):
    From: int
    To: int
    
class Vacancy(NamedTuple):
    Id: int
    Title: str
    Skills: list[str]
    DateUpdate: str
    Url:str
    City:int
    PositionId: int
    Experience: str
    Specialization: str
    Salary: Salary
    
    
class City(NamedTuple):
    IdEdwica: int
    Abbr: str
    Name: str
    

class Position(NamedTuple):
    Id: int
    Title: str
    OtherNames: str

