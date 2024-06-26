# FULL NAME: Vũ Thị Minh Quý
# MSSV: 20227257
# CLASS: 150328
# PROJECT: 04 - Library Management System
# DATE: 20/06/2024 
# ------IMPORTS------------------------------------------
from PyQt6.QtWidgets import QTableWidgetItem, QTableWidget, QPushButton, QMessageBox, QComboBox, QLabel, QLineEdit, QSpinBox, QStackedWidget, QHeaderView, QFrame
from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtGui import QFont, QIntValidator, QRegularExpressionValidator
import sys
import os

# Ensure the project root is in the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import necessary modules from the project
from db.db_session import DBSession
from db.lms_types import BooksBookMarcData, BooksBookData

# ------SEARCHBOOK_UI CLASS (Continued)--------------------
class SearchBook_UI:

    # List of objects in .ui file related to this module
    input_filterSearch      : QComboBox
    input_findSearch        : QLineEdit
    
    find_btn                : QPushButton
    edit_btn                : QPushButton
    search_table            : QTableWidget
    
    detail_box              : QFrame

    input_warehouse_idEdit  : QLineEdit
    input_titleEdit         : QLineEdit
    input_authorEdit        : QLineEdit
    input_isbnEdit          : QLineEdit
    input_compEdit          : QLineEdit
    input_yearEdit          : QLineEdit
    input_quantityEdit      : QSpinBox
    input_stageEdit         : QComboBox
    
    def __init__(self, ui, db_session: DBSession):
        """
        Initialize the SearchBook_UI instance.

        Args:
        - ui: The UI instance containing necessary widgets.
        - db_session: Database session object for querying data.
        """
        # Connect to the database session
        self.ui         = ui
        self.db_session = db_session

        # Connect signals and set up initial state
        self.connectSignals()
        self.initialize()

    def connectSignals(self):
        """
        Connect signals from UI components to their respective functions.
        """
        self.ui.find_btn.pressed.connect(self.findButtonClicked)
        self.ui.search_table.cellClicked.connect(self.displayBookDetails)

    def initialize(self):
        """
        Initialize UI components and state.
        """
        self.hideButtons(all=True)
        self.ui.detail_box.hide()

        self.setupFields()
        self.initial_field_values = {}
        self.initial_find_values = {}

    def hideButtons(self, all: bool):
        """
        Hide or show buttons based on 'all' flag.

        Args:
        - all: Boolean flag to determine if all buttons should be hidden.
        """
        self.ui.delete_btn.hide()
        self.ui.save_btn.hide()
        self.ui.cancel_btn.hide()
        if all:
            self.ui.edit_btn.hide()
        else:
            self.ui.edit_btn.show()

    def setupFields(self):
        """
        Set up input fields with validators and maximum lengths.
        """
        self.detail_fields = [
            self.ui.input_warehouse_idEdit,
            self.ui.input_titleEdit,
            self.ui.input_authorEdit,
            self.ui.input_isbnEdit,
            self.ui.input_compEdit,
            self.ui.input_yearEdit,
            self.ui.input_quantityEdit,
            self.ui.input_stageEdit
        ]

        self.input_fields = {
            "input_titleEdit": self.ui.input_titleEdit,
            "input_authorEdit": self.ui.input_authorEdit,
            "input_isbnEdit": self.ui.input_isbnEdit,
            "input_compEdit": self.ui.input_compEdit,
            "input_yearEdit": self.ui.input_yearEdit,
            "input_quantityEdit": self.ui.input_quantityEdit,
            "input_stageEdit": self.ui.input_stageEdit
        }

        self.ui.input_isbnEdit.setMaxLength(13)
        isbn_validator = QRegularExpressionValidator(QRegularExpression(r'^\d{1,13}$'), self.ui.input_isbnEdit)
        self.ui.input_isbnEdit.setValidator(isbn_validator)
        self.ui.input_titleEdit.setMaxLength(100)
        self.ui.input_authorEdit.setMaxLength(100)
        self.ui.input_compEdit.setMaxLength(100)
        self.ui.input_yearEdit.setValidator(QIntValidator(1000, 9999))
        self.ui.input_quantityEdit.setMaximum(999999)  

    def findButtonClicked(self, clear: bool = True):
        """
        Handle the click event of the Find button.

        Args:
        - clear: Boolean flag to determine if table and detail fields should be cleared.
        """
        try:
            if clear:
                self.clearTableAndDetailFields()

            self.ui.detail_box.hide()
            self.ui.check_btn.hide()
            
            search_query = self.ui.input_findSearch.text().strip()
            
            if not search_query:
                self.showMessageBox("Search", "Please enter a search query.", QMessageBox.Icon.Warning)
                self.ui.input_filterSearch.setCurrentIndex(-1)
                self.hideButtons(all=True)
                return

            filter_criteria = self.ui.input_filterSearch.currentText()
            column_name     = self.getColumnFromFilter(filter_criteria)
            search_results = list(self.db_session.searchBook(column_name, search_query))

            if search_results:
                self.populateTableWithResults(search_results, filter_criteria)
                self.initial_find_values = {
                    'input_findSearch': search_query,
                    'input_filterSearch': filter_criteria
                }
            else:
                self.showMessageBox("Search", "No results found.", QMessageBox.Icon.Warning)
                
        except Exception as e:
            print("Error searching book information:", e)
            self.showMessageBox("Error", str(e), QMessageBox.Icon.Critical)

    def populateTableWithResults(self, search_results, filter_criteria):
        """
        Populate the search_table with search results.

        Args:
        - search_results: List of tuples containing search results.
        - filter_criteria: Current filter criteria selected.
        """
        self.ui.search_table.setRowCount(len(search_results))
        column_count = len(search_results[0]) if search_results else 0
        self.ui.search_table.setColumnCount(column_count)
        header_labels = self.getHeaderLabels(filter_criteria)
        self.setTableHeaders(header_labels)
        self.fillTableWithData(search_results)
        self.adjustColumnWidths(self.ui.search_table)

    def getHeaderLabels(self, filter_criteria: str) -> list[str]:
        """
        Determine header labels based on filter criteria.

        Args:
        - filter_criteria: Current filter criteria selected.

        Returns:
        - List of header labels.
        """
        if filter_criteria in ["Book ID", "Title", "ISBN", "Warehouse ID", ""]:
            return ['Book ID', 'Title', 'ISBN', 'Warehouse ID']
        else:
            return ['Book ID', 'Title', 'ISBN', 'Warehouse ID', filter_criteria]
        
    def setTableHeaders(self, header_labels: list[str]):
        """
        Set headers for the search_table.

        Args:
        - header_labels: List of header labels.
        """
        for col_idx, header in enumerate(header_labels):
            item = QTableWidgetItem(header)
            font = item.font()
            font.setBold(True)
            item.setFont(font)
            self.ui.search_table.setHorizontalHeaderItem(col_idx, item)

    def fillTableWithData(self, search_results: list[tuple]):
        """
        Fill search_table with data.

        Args:
        - search_results: List of tuples containing search results.
        """
        for row_idx, row_data in enumerate(search_results):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.ui.search_table.setItem(row_idx, col_idx, item)

    def getColumnFromFilter(self, filter_criteria: str) -> str:
        """
        Map filter criteria to database column name.

        Args:
        - filter_criteria: Current filter criteria selected.

        Returns:
        - Corresponding database column name.
        """
        column_mapping = {
            "Book ID"       : "book_id",
            "Warehouse ID"  : "warehouse_id",
            "Title"         : "title",
            "Author"        : "author",
            "Public Year"   : "public_year",
            "Public Company": "public_comp",
            "ISBN"          : "isbn",
            "Quantity"      : "quantity",
            "Stage"         : "stage",
            "All"           : None,
            ""              : None
        }

        return column_mapping.get(filter_criteria, None)

    def clearTableAndDetailFields(self):
        """
        Clear contents of search_table and detail input fields.
        """
        self.ui.search_table.clearContents()
        self.ui.search_table.setRowCount(0)
        self.clearDetailFields()

    def showMessageBox(self, title: str, message: str, icon: QMessageBox.Icon):
        """
        Display a message box with specified title, message, and icon.

        Args:
        - title: Title of the message box.
        - message: Content of the message.
        - icon: Icon type for the message box.
        """
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.exec()

    def displayBookDetails(self, row, column):
        """
        Display details of the selected book in the detail_box.

        Args:
        - row: Row index of the selected cell.
        - column: Column index of the selected cell.
        """
        try:
            self.ui.message_edit.clear()
            self.ui.check_btn.hide()
            book_id_item = self.ui.search_table.item(row, 0)  

            if book_id_item is None:
                return
            
            book_id = int(book_id_item.text())
            warehouse_id_item = self.ui.search_table.item(row             , 3)  # Assuming warehouse_id is in column 3

            if warehouse_id_item is None:
                self.showMessageBox("Error", "Warehouse ID not found.", QMessageBox.Icon.Warning)
                return

            warehouse_id = int(warehouse_id_item.text())

            bookMarcData, bookData = self.db_session.getBookByIdAndWarehouseId(book_id, warehouse_id)
            
            if bookMarcData is None or bookData is None:
                self.showMessageBox("Error", "Book not found.", QMessageBox.Icon.Warning)
                return
            
            self.setDataFields(bookMarcData, bookData, warehouse_id)

            if self.ui.admin_id.text() == "Guest":
                self.hideButtons(all=True)
            else:
                self.hideButtons(all=False)
            self.ui.detail_box.show()
            self.disableEditFields()

        except Exception as e:
            self.showMessageBox("Error", str(e), QMessageBox.Icon.Critical)

    def disableEditFields(self):
        """
        Disable editing for all detail input fields.
        """
        for field in self.detail_fields:
            field.setDisabled(True)
            field.setStyleSheet("""
                background-color: lightgrey;
                color: black;
                border: 2px solid black;
            """)

    def setDataFields(self, bookMarcData: BooksBookMarcData, bookData: BooksBookData, warehouse_id: int):
        """
        Set data fields with values retrieved from database.

        Args:
        - bookMarcData: Object containing book MARC data.
        - bookData: Object containing book data.
        - warehouse_id: ID of the warehouse where the book is located.
        """
        self.ui.input_titleEdit.setText(bookMarcData.title)
        self.ui.input_authorEdit.setText(bookMarcData.author)
        self.ui.input_isbnEdit.setText(bookMarcData.isbn)
        self.ui.input_yearEdit.setText(str(bookMarcData.public_year))
        self.ui.input_compEdit.setText(bookMarcData.public_comp)
        self.ui.input_warehouse_idEdit.setText(str(warehouse_id))
        self.ui.input_quantityEdit.setValue(bookData.quantity)
        self.ui.input_stageEdit.setCurrentText(bookData.stage)
    
        self.initial_field_values = {
            'input_titleEdit': bookMarcData.title,
            'input_authorEdit': bookMarcData.author,
            'input_isbnEdit': bookMarcData.isbn,
            'input_yearEdit': str(bookMarcData.public_year),
            'input_compEdit': bookMarcData.public_comp,
            'input_warehouse_idEdit': str(warehouse_id),
            'input_quantityEdit': bookData.quantity,
            'input_stageEdit': bookData.stage
        }

        self.old_bookMarcData = bookMarcData
        self.old_bookData = bookData

    def adjustColumnWidths(self, table):
        """
        Adjust column widths of the specified table.

        Args:
        - table: TableWidget object to adjust column widths for.
        """
        table.resizeColumnsToContents()
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
    def clearDetailFields(self):
        """
        Clear all input fields in the detail_box.
        """
        for field in self.detail_fields:
            if isinstance(field, QLineEdit):
                field.clear()
            elif isinstance(field, QSpinBox):
                field.setValue(0)
            elif isinstance(field, QComboBox):
                field.setCurrentIndex(-1)


