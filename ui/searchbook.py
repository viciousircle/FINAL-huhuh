# ------IMPORTS------------------------------------------
from PyQt6.QtWidgets import QTableWidgetItem, QTableWidget, QPushButton, QMessageBox, QComboBox, QLabel,QLineEdit,QSpinBox,QStackedWidget,QHeaderView
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_session import DBSession
from lms_types import BooksBookMarcData, BooksBookData
# ---------------------------------------------------------

# ------SEARCHBOOK_UI CLASS---------------------------------
class SearchBook_UI:
    # List of objects in .ui file related to this module
    input_filterSearch      : QComboBox
    input_findSearch        : QLineEdit
    
    find_btn                : QPushButton
    search_table            : QTableWidget
    
    input_warehouse_idEdit  : QLineEdit
    input_titleEdit         : QLineEdit
    input_authorEdit        : QLineEdit
    input_isbnEdit          : QLineEdit
    input_compEdit          : QLineEdit
    input_yearEdit          : QLineEdit
    input_quantityEdit      : QSpinBox
    input_stageEdit         : QComboBox
    
    edit_stackedWidget      : QStackedWidget
    edit_btn                : QPushButton
    delete_btn              : QPushButton
    save_btn                : QPushButton
    cancel_btn              : QPushButton
    
    
    def __init__(self, ui, db_session: DBSession):
        self.ui         = ui
        self.db_session = db_session
        
        self.buttons_edit = [
            self.ui.edit_btn,
            self.ui.delete_btn,
            self.ui.save_btn,
            self.ui.cancel_btn
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
        
        self.initial_field_values = {}
                
        self.ui.search_table.cellClicked.connect(self.displayBookDetails)
        
        self.ui.edit_btn.clicked.connect(lambda: self.ui.edit_stackedWidget.setCurrentWidget(self.ui.save_page))
        self.ui.cancel_btn.clicked.connect(lambda: self.ui.edit_stackedWidget.setCurrentWidget(self.ui.delete_page))

        self.ui.edit_btn.clicked.connect(self.editButtonClicked)
        self.ui.cancel_btn.clicked.connect(self.cancelButtonClicked)
        self.ui.save_btn.clicked.connect(self.saveButtonClicked)
        self.ui.delete_btn.clicked.connect(self.deleteButtonClicked)
        
        
        
    def searchBookInformation(self):
        try:
            print("Searching book information...")
            # Clear previous search results from the table
            self.ui.search_table.clearContents()
            self.ui.search_table.setRowCount(0)

            column_mapping = {
                "Book ID": "book_id",
                "Warehouse ID": "warehouse_id",
                "Title": "title",
                "Author": "author",
                "Public Year": "public_year",
                "Public Company": "public_comp",
                "ISBN": "isbn",
                "Quantity": "quantity",
                "Stage": "stage",
                "All": None,
                "": None
            }

            filter_criteria = self.ui.input_filterSearch.currentText()
            column_name = column_mapping[filter_criteria]
            search_query = self.ui.input_findSearch.text().strip()

            search_results = list(self.db_session.searchBook(column_name, search_query))

            print("Found", len(search_results), "results.")

            if search_results:
                self.ui.search_table.setRowCount(len(search_results))
                column_count = len(search_results[0])
                self.ui.search_table.setColumnCount(column_count)

                # Set the header labels
                if filter_criteria in ["Book ID", "Title", "ISBN", "Warehouse ID", ""]:
                    header_labels = ['Book ID', 'Title', 'ISBN', 'Warehouse ID']
                else:
                    header_labels = ['Book ID', 'Title', 'ISBN', 'Warehouse ID', filter_criteria]

                # Set column headers and make them bold
                for col_idx, header in enumerate(header_labels):
                    item = QTableWidgetItem(header)
                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)
                    self.ui.search_table.setHorizontalHeaderItem(col_idx, item)

                for row_idx, row_data in enumerate(search_results):
                    for col_idx, value in enumerate(row_data):
                        item = QTableWidgetItem(str(value))
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Center align the text
                        self.ui.search_table.setItem(row_idx, col_idx, item)

                self.ui.search_table.resizeColumnsToContents()
                self.adjustColumnWidths(self.ui.search_table)
            else:
                QMessageBox.warning(self.ui, "Search", "No results found.")
        except Exception as e:
            print("Error searching book information:", e)
            QMessageBox.critical(self.ui, "Error", str(e))


    def displayBookDetails(self, row, column):
        try:
            print("Displaying book details...")
            book_id_item = self.ui.search_table.item(row, 0)  

            if book_id_item is None:
                return
            
            book_id = int(book_id_item.text())
            print("Selected book ID:", book_id)

            bookMarcData, bookData = self.db_session.getBookById(book_id)
            
            if bookMarcData is None or bookData is None:
                print("Book details not found.")
                QMessageBox.warning(self.ui, "Error", "Book details not found.")
                return
            
            self.ui.input_titleEdit.setText(bookMarcData.title)
            self.ui.input_authorEdit.setText(bookMarcData.author)
            self.ui.input_isbnEdit.setText(bookMarcData.isbn)
            self.ui.input_yearEdit.setText(str(bookMarcData.public_year))
            self.ui.input_compEdit.setText(bookMarcData.public_comp)
            self.ui.input_warehouse_idEdit.setText(str(bookData.warehouse_id))
            self.ui.input_quantityEdit.setValue(bookData.quantity)
            self.ui.input_stageEdit.setCurrentText(bookData.stage)
            
            print("Book details displayed successfully.")
            
            self.initial_field_values = {
                'input_titleEdit'       : bookMarcData.title,
                'input_authorEdit'      : bookMarcData.author,
                'input_isbnEdit'        : bookMarcData.isbn,
                'input_yearEdit'        : str(bookMarcData.public_year),
                'input_compEdit'        : bookMarcData.public_comp,
                'input_warehouse_idEdit': str(bookData.warehouse_id),
                'input_quantityEdit'    : bookData.quantity,
                'input_stageEdit'       : bookData.stage
            }
            
            self.old_bookMarcData   = bookMarcData
            self.old_bookData       = bookData

        except Exception as e:
            QMessageBox.critical(self.ui, "Error", str(e))

    def editButtonClicked(self):
        # Enable or disable input fields based on edit button state
        for field_name, field_widget in self.input_fields.items():
            if isinstance(field_widget, QLineEdit) or isinstance(field_widget, QSpinBox):
                field_widget.setReadOnly(False)
            elif isinstance(field_widget, QComboBox):
                field_widget.setEnabled(True)

        self.ui.save_btn.setEnabled(True)
        self.ui.cancel_btn.setEnabled(True)
        self.ui.edit_btn.setEnabled(False)
            
    def cancelButtonClicked(self):
        if QMessageBox.question(self.ui, 'Message', "Are you sure you want to cancel and discard changes?",
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            for field_name, field_widget in self.input_fields.items():
                if field_name in self.initial_field_values:
                    initial_value = self.initial_field_values[field_name]
                    if isinstance(field_widget, QLineEdit):
                        field_widget.setText(initial_value)
                    elif isinstance(field_widget, QSpinBox):
                        field_widget.setValue(int(initial_value))
                    elif isinstance(field_widget, QComboBox):
                        index = field_widget.findText(initial_value)
                        if index != -1:
                            field_widget.setCurrentIndex(index)

            for field_widget in self.input_fields.values():
                if isinstance(field_widget, QLineEdit) or isinstance(field_widget, QSpinBox):
                    field_widget.setReadOnly(True)
                elif isinstance(field_widget, QComboBox):
                    field_widget.setEnabled(False)

            self.ui.save_btn.setEnabled(False)
            self.ui.cancel_btn.setEnabled(False)
            self.ui.edit_btn.setEnabled(True)
      
    def saveButtonClicked(self):
        try:
            updated_bookMarcData = BooksBookMarcData(
                title=self.ui.input_titleEdit.text(),
                author=self.ui.input_authorEdit.text(),
                isbn=self.ui.input_isbnEdit.text(),
                public_year=int(self.ui.input_yearEdit.text()),
                public_comp=self.ui.input_compEdit.text(),
                book_id=self.old_bookMarcData.book_id
            )
            
            updated_bookData = BooksBookData(
                warehouse_id=int(self.ui.input_warehouse_idEdit.text()),
                quantity=self.ui.input_quantityEdit.value(),
                stage=self.ui.input_stageEdit.currentText(),
                book_id=self.old_bookData.book_id,
                isbn=self.ui.input_isbnEdit.text()
            )
            
            success, message = self.db_session.updateBook(updated_bookMarcData, updated_bookData, self.old_bookMarcData, self.old_bookData)
            
            if not success:
                QMessageBox.warning(self.ui, "Error", message)
                return
            
            # Disable the input fields after saving the changes
            for field_widget in self.input_fields.values():
                if isinstance(field_widget, QLineEdit) or isinstance(field_widget, QSpinBox):
                    field_widget.setReadOnly(True)
                elif isinstance(field_widget, QComboBox):
                    field_widget.setEnabled(False)

            self.ui.save_btn.setEnabled(False)
            self.ui.cancel_btn.setEnabled(False)
            self.ui.edit_btn.setEnabled(True)

            QMessageBox.information(self.ui, "Save", "Changes saved successfully.")
            
            self.ui.edit_stackedWidget.setCurrentWidget(self.ui.delete_page)
            
            self.searchBookInformation()
            
            from ui.showfile import ShowFile_UI
            showfile = ShowFile_UI(self.ui, self.db_session)
            showfile.updateBookMarcTable()
            showfile.updateBookTable()
            
            


        except Exception as e:
            QMessageBox.critical(self.ui, "Error", str(e))
            
            
    def deleteButtonClicked(self):
    
        try:
            # Get the index of the selected row
            selected_row = self.ui.search_table.currentRow()
            
            # Ensure a row is selected
            if selected_row == -1:
                QMessageBox.warning(self.ui, "Error", "No book selected for deletion.")
                return
            
            # Get the book ID from the selected row
            book_id_item = self.ui.search_table.item(selected_row, 0)
            if book_id_item is None:
                return
            
            book_id = int(book_id_item.text())
            admin_id = self.ui.admin_id.text()
            
            
            confirmation = QMessageBox.question(self.ui, 'Message', "Are you sure you want to delete this book?",
                                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirmation == QMessageBox.StandardButton.Yes:
                
                
                success, message = self.db_session.deleteBook(book_id, admin_id)
                
                if not success:
                    QMessageBox.warning(self.ui, "Error", message)
                    return
                
                QMessageBox.information(self.ui, "Delete", "Book deleted successfully.")
                
                self.searchBookInformation()
                
                from ui.showfile import ShowFile_UI
                showfile = ShowFile_UI(self.ui, self.db_session)
                showfile.updateBookMarcTable()
                showfile.updateBookTable()
                
                
                
            elif confirmation == QMessageBox.StandardButton.No:
            # Re-enable the delete button
                self.ui.delete_btn.setDisabled(False)
                
                # chuaw xong doan nafy
        except Exception as e:
            QMessageBox.critical(self.ui, "Error", str(e))


    def adjustColumnWidths(self, table_widget: QTableWidget):
        # Set the header to resize to fill the available space
        header = table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Optionally, resize rows to fit content
        table_widget.resizeRowsToContents()