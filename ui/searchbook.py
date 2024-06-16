# ------IMPORTS------------------------------------------
from PyQt6.QtWidgets import QTableWidgetItem, QTableWidget, QPushButton, QMessageBox, QComboBox, QLabel,QLineEdit,QSpinBox,QStackedWidget,QHeaderView,QDateEdit 
from PyQt6.QtCore import Qt,QDate
from PyQt6.QtGui import QFont, QColor, QIntValidator
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
    
    edit_btn                : QPushButton
    delete_btn              : QPushButton
    save_btn                : QPushButton
    cancel_btn              : QPushButton
    
    
    def __init__(self, ui, db_session: DBSession):
        
        # Connect to the database session
        self.ui         = ui
        self.db_session = db_session
        
        # Set up the page buttons
        self.buttons_edit = [
            self.ui.edit_btn,
            self.ui.delete_btn,
            self.ui.save_btn,
            self.ui.cancel_btn
        ]
        
        for button in self.buttons_edit:
            button.setDisabled(True)
            
        self.ui.save_btn.hide()
        self.ui.cancel_btn.hide()
        self.ui.delete_btn.hide()
            
        # Set up the input fields
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

        self.ui.input_yearEdit.setValidator(QIntValidator(1000, 9999))
        self.ui.input_quantityEdit.setMaximum(999999)  
        

        # Connect button signals and table interactions
        self.connectSignals()
        
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
                
    def connectSignals(self):
        self.ui.search_table.cellClicked.connect(self.displayBookDetails)
        self.ui.edit_btn.clicked.connect(self.editButtonClicked)
        self.ui.cancel_btn.clicked.connect(self.cancelButtonClicked)
        self.ui.save_btn.clicked.connect(self.saveButtonClicked)
        self.ui.delete_btn.clicked.connect(self.deleteButtonClicked)
        
    def searchBookInformation(self):
        try:
            print("Searching book information...")
            
            # Before searching, disable the edit buttons
            for button in self.buttons_edit:
                button.setEnabled(False)
            
            # Before searching, clear the table and detail fields
            self.ui.search_table.clearContents()
            self.ui.search_table.setRowCount(0)
            self.clearDetailFields()
            
            search_query = self.ui.input_findSearch.text().strip()
            
            if search_query == "":
                print("No search query entered.")
                
                QMessageBox.warning(self.ui, "Search", "Please enter a search query.")
                
                self.ui.input_filterSearch.setCurrentIndex(-1)
                
                return

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

            filter_criteria = self.ui.input_filterSearch.currentText()
            column_name     = column_mapping[filter_criteria]

            search_results = list(self.db_session.searchBook(column_name, search_query))

            print("Found", len(search_results), "results.")

            if search_results:
                
                # Set up the table to display the search results
                self.ui.search_table.setRowCount(len(search_results))
                column_count = len(search_results[0])
                self.ui.search_table.setColumnCount(column_count)

                if filter_criteria in ["Book ID", "Title", "ISBN", "Warehouse ID", ""]:
                    header_labels = ['Book ID', 'Title', 'ISBN', 'Warehouse ID']
                else:
                    header_labels = ['Book ID', 'Title', 'ISBN', 'Warehouse ID', filter_criteria]

                for col_idx, header in enumerate(header_labels):
                    item = QTableWidgetItem(header)
                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)
                    self.ui.search_table.setHorizontalHeaderItem(col_idx, item)

                for row_idx, row_data in enumerate(search_results):
                    for col_idx, value in enumerate(row_data):
                        item = QTableWidgetItem(str(value))
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter) 
                        self.ui.search_table.setItem(row_idx, col_idx, item)

                self.ui.search_table.resizeColumnsToContents()
                self.adjustColumnWidths(self.ui.search_table)
                
            else:
                print("No results found.")
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

            # Retrieve the warehouse ID from the selected row
            warehouse_id_item = self.ui.search_table.item(row, 3)  # Adjust column index as per your table setup

            if warehouse_id_item is None:
                print("Warehouse ID not found for the selected book.")
                QMessageBox.warning(self.ui, "Error", "Warehouse ID not found for the selected book.")
                return

            warehouse_id = int(warehouse_id_item.text())
            print("Selected warehouse ID:", warehouse_id)

            # Retrieve book details for the selected book ID and warehouse ID
            bookMarcData, bookData = self.db_session.getBookByIdAndWarehouseId(book_id, warehouse_id)
            
            if bookMarcData is None or bookData is None:
                print("Book details not found.")
                QMessageBox.warning(self.ui, "Error", "Book details not found.")
                return
            
            self.ui.input_titleEdit.setText(bookMarcData.title)
            self.ui.input_authorEdit.setText(bookMarcData.author)
            self.ui.input_isbnEdit.setText(bookMarcData.isbn)
            self.ui.input_yearEdit.setText(str(bookMarcData.public_year))
            self.ui.input_compEdit.setText(bookMarcData.public_comp)
            
            # Set the warehouse ID edit field
            self.ui.input_warehouse_idEdit.setText(str(warehouse_id))
            
            self.ui.input_quantityEdit.setValue(bookData.quantity)
            self.ui.input_stageEdit.setCurrentText(bookData.stage)
            
            print("Book details displayed successfully.")
            
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
            
            for button in self.buttons_edit:
                button.setEnabled(True)

        except Exception as e:
            QMessageBox.critical(self.ui, "Error", str(e))


    def editButtonClicked(self):
        try:
            print("Editing book details...")
            # Disable the search table and input fields
            self.ui.search_table.setDisabled(True)
            self.ui.input_findSearch.setDisabled(True)
            self.ui.input_filterSearch.setDisabled(True)
            self.ui.find_btn.setDisabled(True)
            # self.ui.edit_btn.setEnabled(False)
            
            # Clear previous selections
            self.ui.search_table.clearSelection()
            
            # Get the selected row
            selected_row = self.ui.search_table.currentRow()
            
            if selected_row == -1:
                return
            
            # Highlight all cells in the selected row
            column_count = self.ui.search_table.columnCount()
            
            for col_idx in range(column_count):
                
                item = self.ui.search_table.item(selected_row, col_idx)
                
                if item:
                    
                    item.setBackground(QColor("#FFFF00"))  # Set background color to yellow
            
            # Enable the input fields for editing
            for field_name, field_widget in self.input_fields.items():
                
                if isinstance(field_widget, QLineEdit) or isinstance(field_widget, QSpinBox):
                    
                    field_widget.setReadOnly(False)
                elif isinstance(field_widget, QComboBox):
                    field_widget.setEnabled(True)
                    
            # Show the save, cancel, and delete buttons
            self.ui.save_btn.show()
            self.ui.cancel_btn.show()
            self.ui.delete_btn.show()
            self.ui.edit_btn.hide()

            
            print("Book details are now editable.")
            
        except Exception as e:
            print("Error editing book details:", e)
            
            QMessageBox.critical(self.ui, "Error", str(e))

            
    def cancelButtonClicked(self):
        try:
            print("Cancelling changes...")
            
            # Store the current field values
            current_field_values = {
                'input_titleEdit'           : self.ui.input_titleEdit.text(),
                'input_authorEdit'          : self.ui.input_authorEdit.text(),
                'input_isbnEdit'            : self.ui.input_isbnEdit.text(),
                'input_yearEdit'            : self.ui.input_yearEdit.text(),  # No need for str() conversion
                'input_compEdit'            : self.ui.input_compEdit.text(),
                'input_warehouse_idEdit'    : self.ui.input_warehouse_idEdit.text(),  # No need for str() conversion
                'input_quantityEdit'        : self.ui.input_quantityEdit.value(),
                'input_stageEdit'           : self.ui.input_stageEdit.currentText()
            }

            # Check if any changes have been made
            changes_made = False
            
            for field_name, initial_value in self.initial_field_values.items():
                current_value = current_field_values[field_name]
                
                if isinstance(initial_value, int) and isinstance(current_value, str):
                    current_value = str(current_value)  # Ensure same type for comparison
                
                if current_value != initial_value:
                    changes_made = True
                    break

            print("Changes made:", changes_made)

            if not changes_made:
                print("No changes were made.")
                
                QMessageBox.information(self.ui, 'Message', "No changes were made.")
                
                # self.resetUIAfterCancel()
                
                return

            if QMessageBox.question(self.ui, 'Message', "Are you sure you want to cancel and discard changes?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
                
                self.resetUIAfterCancel()
                # self.ui.edit_btn.setEnabled(True)
                
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
                        
            print("Changes discarded successfully.")

        except Exception as e:
            print("Error cancelling changes:", e)
            
            QMessageBox.critical(self.ui, "Error", str(e))


    def resetUIAfterCancel(self):
        
        # self.ui.edit_btn.setEnabled(True)
        self.ui.edit_btn.show()
        self.ui.search_table.setDisabled(False)
        self.ui.input_findSearch.setDisabled(False)
        self.ui.input_filterSearch.setDisabled(False)
        self.ui.find_btn.setDisabled(False)

        # Clear the row selection and highlighting
        self.ui.search_table.clearSelection()

        # Iterate through all rows to clear any highlighted rows
        for row_idx in range(self.ui.search_table.rowCount()):
            for col_idx in range(self.ui.search_table.columnCount()):
                
                item = self.ui.search_table.item(row_idx, col_idx)
                
                if item:
                    item.setBackground(QColor(Qt.GlobalColor.white))  # Set background color back to white

        # Hide buttons
        self.ui.save_btn.hide()
        self.ui.cancel_btn.hide()
        self.ui.delete_btn.hide()
        # self.ui.edit_btn.setEnabled(False)

    def saveButtonClicked(self):
        try:
            print("Saving changes...")
            
            current_field_values = {
                'input_titleEdit'           : self.ui.input_titleEdit.text(),
                'input_authorEdit'          : self.ui.input_authorEdit.text(),
                'input_isbnEdit'            : self.ui.input_isbnEdit.text(),
                'input_yearEdit'            : str(self.ui.input_yearEdit.text()),
                'input_compEdit'            : self.ui.input_compEdit.text(),
                'input_warehouse_idEdit'    : str(self.ui.input_warehouse_idEdit.text()),
                'input_quantityEdit'        : self.ui.input_quantityEdit.value(),
                'input_stageEdit'           : self.ui.input_stageEdit.currentText()
            }

            # Check if any changes have been made
            changes_made = False
            for field_name, initial_value in self.initial_field_values.items():
                if current_field_values[field_name] != initial_value:
                    
                    changes_made = True
                    
                    break

            if not changes_made:
                print("No changes were made.")
                
                QMessageBox.information(self.ui, 'Message', "You need to edit the fields to make changes.")
                return

            updated_bookMarcData = BooksBookMarcData(
                title       =self.ui.input_titleEdit.text(),
                author      =self.ui.input_authorEdit.text(),
                isbn        =self.ui.input_isbnEdit.text(),
                public_year =int(self.ui.input_yearEdit.text()),
                public_comp =self.ui.input_compEdit.text(),
                book_id     =self.old_bookMarcData.book_id
            )

            updated_bookData = BooksBookData(
                warehouse_id=int(self.ui.input_warehouse_idEdit.text()),
                quantity    =self.ui.input_quantityEdit.value(),
                stage       =self.ui.input_stageEdit.currentText(),
                book_id     =self.old_bookData.book_id,
                isbn        =self.ui.input_isbnEdit.text()
            )

            # Ask for confirmation before saving
            confirm_save = QMessageBox.question(self.ui, "Save Changes", "Are you sure you want to save the changes?",
                                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                                QMessageBox.StandardButton.No)

            if confirm_save == QMessageBox.StandardButton.Yes:
                
                admin_id = self.ui.admin_id.text()                
                
                success, message = self.db_session.updateBook(admin_id,updated_bookMarcData, updated_bookData, self.old_bookMarcData, self.old_bookData)

                if not success:
                    print("Error saving changes:", message)
                    
                    QMessageBox.warning(self.ui, "Error", message)
                    
                    return

                # Disable the input fields after saving the changes
                for field_widget in self.input_fields.values():
                    
                    if isinstance(field_widget, QLineEdit) or isinstance(field_widget, QSpinBox):
                        field_widget.setReadOnly(True)
                        
                    elif isinstance(field_widget, QComboBox):
                        field_widget.setEnabled(False)

                # Disable the save and cancel buttons
                self.ui.save_btn.setEnabled(False)
                self.ui.cancel_btn.setEnabled(False)
                self.ui.edit_btn.setEnabled(True)

                QMessageBox.information(self.ui, "Save Changes", "Changes saved successfully.")

                # Enable search_table
                self.ui.search_table.setDisabled(False)
                self.ui.search_table.clearContents()
                self.ui.edit_btn.setEnabled(False)
                
                self.ui.save_btn.hide()
                self.ui.cancel_btn.hide()
                self.ui.delete_btn.hide()
                
                self.ui.input_findSearch.setDisabled(False)
                self.ui.input_filterSearch.setDisabled(False)
                self.ui.find_btn.setDisabled(False)
                
                
                self.searchBookInformation()
                

                from ui.showfile import ShowFile_UI
                showfile = ShowFile_UI(self.ui, self.db_session)
                showfile.updateBookMarcTable()
                showfile.updateBookTable()
                
                print("Changes saved successfully.")
                

        except Exception as e:
            print("Error saving changes:", e)
            
            QMessageBox.critical(self.ui, "Error", str(e))

    
    def deleteButtonClicked(self):
        try:
            print("Deleting book...")
            
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

            book_id     = int(book_id_item.text())
            admin_id    = self.ui.admin_id.text()

            confirmation = QMessageBox.question(self.ui, 'Message', "Are you sure you want to delete this book?",
                                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            
            if confirmation == QMessageBox.StandardButton.Yes:
                warehouse_id = self.ui.input_warehouse_idEdit.text()
                success, message = self.db_session.deleteBook(warehouse_id,book_id, admin_id)

                if not success:
                    
                    QMessageBox.warning(self.ui, "Error", message)
                    
                    return

                QMessageBox.information(self.ui, "Delete", "Book deleted successfully.")

                self.searchBookInformation()

                from ui.showfile import ShowFile_UI
                showfile = ShowFile_UI(self.ui, self.db_session)
                showfile.updateBookMarcTable()
                showfile.updateBookTable()
                
                self.ui.save_btn.hide()
                self.ui.cancel_btn.hide()
                self.ui.delete_btn.hide()
                
                self.ui.search_table.setDisabled(False)

                # Disable the input fields after deletion
                for field_widget in self.input_fields.values():
                    if isinstance(field_widget, QLineEdit) or isinstance(field_widget, QSpinBox):
                        field_widget.setReadOnly(True)
                        
                    elif isinstance(field_widget, QComboBox):
                        field_widget.setEnabled(False)
                        
                print("Book deleted successfully.")

            elif confirmation == QMessageBox.StandardButton.No:
                # Re-enable the delete button
                self.ui.edit_btn.setEnabled(True)
                
                print("Book deletion cancelled.")

        except Exception as e:
            print("Error deleting book:", e)
            
            QMessageBox.critical(self.ui, "Error", str(e))

    
    def adjustColumnWidths(self, table_widget: QTableWidget):
        # Set the header to resize to fill the available space
        header = table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Optionally, resize rows to fit content
        table_widget.resizeRowsToContents()
        
    def clearDetailFields(self):
        """Clear the book detail input fields."""
        for field in self.detail_fields:
            if isinstance(field, QLineEdit):
                field.clear()
            elif isinstance(field, QSpinBox):
                field.setValue(0)
            elif isinstance(field, QComboBox):
                field.setCurrentIndex(-1)