# FULL NAME: Vũ Thị Minh Quý
# MSSV: 20227257
# CLASS: 150328
# PROJECT: 04 - Library Management System
# DATE: 20/06/2024 

from dataclasses import dataclass, field
from typing import TypeVar, Union, Optional, Literal

# Type variable for generic typing
T = TypeVar('T')

@dataclass
class UsersAccountData:
    """
    Data class representing the user account information.
    """
    admin_id: Optional[str]
    admin_name: Optional[str]
    password: Optional[str]

# Type alias for execution results, which can be a success or failure tuple
ExecuteResult = Union[
    tuple[Literal[True], T],
    tuple[Literal[False], str]
]

@dataclass
class BooksBookMarcData:
    """
    Data class representing the book bibliographic information.
    """
    title: Optional[str]
    author: Optional[str]
    public_year: Optional[int]
    public_comp: Optional[str]
    isbn: Optional[str]
    book_id: Optional[int] = field(default=None)
    
@dataclass
class BooksBookData:
    """
    Data class representing the book inventory information.
    """
    quantity: Optional[int]
    stage: Optional[str]
    isbn: Optional[str]
    book_id: Optional[int] = field(default=None)
    warehouse_id: Optional[int] = field(default=None)
