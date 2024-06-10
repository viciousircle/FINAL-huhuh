from dataclasses import dataclass, field
from datetime import datetime
from typing import TypeVar, Union, Optional, Literal


T = TypeVar('T')

@dataclass
class UsersAccountData:
    admin_id: Optional[int]
    password: Optional[str]
    admin_name: Optional[str]

@dataclass
class UsersHistoryData:
    edit_id: Optional[int]
    admin_id: Optional[int]
    book_id: Optional[int]
    timestamp: Optional[datetime]

@dataclass
class UsersGuestData:
    guest_id: Optional[int]
    guest_name: Optional[str]
    timestamp: Optional[datetime]

ExecuteResult = Union[
    tuple[Literal[True], T],
    tuple[Literal[False], str]
]

@dataclass
class BooksBookMarcData:
    title: Optional[str]
    author: Optional[str]
    public_year: Optional[int]
    public_comp: Optional[str]
    isbn: Optional[str]
    book_id: Optional[int] = field(default=None)
    
@dataclass
class BooksBookData:
    quantity: Optional[int]
    stage: Optional[str]
    book_id: Optional[int] = field(default=None)
    warehouse_id: Optional[int] = field(default=None)


