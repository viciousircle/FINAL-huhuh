# ------IMPORTS------------------------------------------
from PyQt6.QtWidgets import QTableWidgetItem, QTableWidget, QPushButton, QMessageBox, QComboBox, QLabel,QLineEdit,QSpinBox
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_session import DBSession
# ---------------------------------------------------------

# ------SEARCHBOOK_UI CLASS---------------------------------
class SearchBook_UI:
    # List of objects in .ui file related to this module
    input_filterSearch      : QComboBox
    input_findSearch        : QLineEdit
    
    find_btn                : QPushButton
    search_table            : QTableWidget
    
    input_warehouse_idEdit  : QLabel
    input_titleEdit         : QLineEdit
    input_authorEdit        : QLineEdit
    input_isbnEdit          : QLineEdit
    input_compEdit          : QLineEdit
    input_yearEdit          : QLineEdit
    input_quantityEdit      : QSpinBox
    input_stageEdit         :QComboBox
    
    edit_btn                : QPushButton
    delete_btn              : QPushButton
    save_btn                : QPushButton
    cancel_btn              : QPushButton
    
    
    def __init__(self, ui, db_session: DBSession):
        self.ui         = ui
        self.db_session = db_session
        
        self.ui.search_table.cellClicked.connect(self.displayBookDetails)
        
    def searchBookInformation(self):
        try:
            # Clear previous search results from the table
            self.ui.search_table.clearContents()
            self.ui.search_table.setRowCount(0)

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
            search_query    = self.ui.input_findSearch.text().strip()
    
            search_results = list(self.db_session.searchBook(column_name, search_query))
            
            if search_results:
                self.ui.search_table.setRowCount(len(search_results))
                column_count = len(search_results[0]) 
                self.ui.search_table.setColumnCount(column_count)
                
                # Set the header labels
                if filter_criteria in ["Book ID", "Title", "ISBN", "Warehouse ID", ""]:
                    header_labels = ['Book ID', 'Title', 'ISBN', 'Warehouse ID']
                else:
                    header_labels = ['Book ID', 'Title', 'ISBN', 'Warehouse ID', filter_criteria]
                    
                self.ui.search_table.setHorizontalHeaderLabels(header_labels)

                for row_idx, row_data in enumerate(search_results):
                    for col_idx, value in enumerate(row_data):
                        self.ui.search_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

                self.ui.search_table.resizeColumnsToContents()
            else:
                QMessageBox.warning(self.ui, "Search", "No results found.")
        except Exception as e:
            QMessageBox.critical(self.ui, "Error", str(e))

    def displayBookDetails(self, row, column):
        try:
            # Get the book ID from the selected row
            book_id_item = self.ui.search_table.item(row, 0)  
            # Assuming book_id is in the first column
            
            if book_id_item is None:
                return
            
            book_id = int(book_id_item.text())
            print(book_id)

            # Fetch the book details using the book ID
            bookMarcData, bookData = self.db_session.getBookById(book_id)
            
                        
            print(bookMarcData)
            print(bookData)
            if bookMarcData is None or bookData is None:
                QMessageBox.warning(self.ui, "Error", "Book details not found.")
                return
            


            # Update UI components with the book details

            self.ui.input_titleEdit.setText(bookMarcData.title)
            self.ui.input_authorEdit.setText(bookMarcData.author)
            self.ui.input_isbnEdit.setText(bookMarcData.isbn)
            self.ui.input_yearEdit.setText(str(bookMarcData.public_year))
            self.ui.input_compEdit.setText(bookMarcData.public_comp)
            self.ui.input_warehouse_idEdit.setText(str(bookData.warehouse_id))
            self.ui.input_quantityEdit.setValue(bookData.quantity)
            self.ui.input_stageEdit.setCurrentText(bookData.stage)

        except Exception as e:
            QMessageBox.critical(self.ui, "Error", str(e))
