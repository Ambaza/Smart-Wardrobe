import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QLineEdit, QComboBox
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

import mysql.connector

# MySQL database configuration
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'wardrobe',
    'raise_on_warnings': True
}

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Wardrobe App')
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.setStyleSheet("background-color: #F2E8CF;")

        # Button 1: Import Image
        self.import_button = QPushButton('Import Image', self)
        self.import_button.clicked.connect(self.open_import_window)  # Connect to open_import_window method
        self.import_button.setStyleSheet("background-color: #F2E8CF; color: #101010;")
        self.layout.addWidget(self.import_button)

        # Button 2: Explore Photo
        self.explore_button = QPushButton('Explore Photo', self)
        self.explore_button.clicked.connect(self.open_explore_window)  # Connect to open_explore_window method
        self.explore_button.setStyleSheet("background-color: #F2E8CF; color: #101010;")
        self.layout.addWidget(self.explore_button)

        # Button 3: Special Function
        self.special_button = QPushButton('Special Function', self)
        self.special_button.clicked.connect(self.open_special_window)  # Connect to open_special_window method
        self.special_button.setStyleSheet("background-color: #F2E8CF; color: #101010;")
        self.layout.addWidget(self.special_button)

    def open_import_window(self):
        self.import_dialog = ImageImportDialog()
        self.import_dialog.show()

    def open_explore_window(self):
        self.explore_dialog = PhotoExplorerDialog(self)
        self.explore_dialog.show()


    def open_special_window(self):
        self.special_dialog = SpecialFunctionDialog()
        self.special_dialog.show()

class ImageImportDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Import Image')
        self.setGeometry(100, 100, 400, 200)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.setStyleSheet("background-color: #F2E8CF;")

        # Name input
        self.name_label = QLabel('Name:')
        self.name_label.setStyleSheet("color: #101010;")
        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)

        # Database selection
        self.db_label = QLabel('Database:')
        self.db_label.setStyleSheet("color: #101010;")
        self.db_combo = QComboBox()
        self.db_combo.addItems(['bottom', 'dresse', 'top'])
        self.layout.addWidget(self.db_label)
        self.layout.addWidget(self.db_combo)

        # Image selection
        self.image_label = QLabel('Image:')
        self.image_label.setStyleSheet("color: #101010;")
        self.image_button = QPushButton('Select Image')
        self.image_button.clicked.connect(self.select_image)
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.image_button)

        # Import button
        self.import_button = QPushButton('Import')
        self.import_button.clicked.connect(self.import_image)
        self.layout.addWidget(self.import_button)

    def select_image(self):
        file_dialog = QFileDialog()
        image_path, _ = file_dialog.getOpenFileName(self, 'Select Image', '', 'Images (*.png *.xpm *.jpg *.jpeg *.bmp)')
        self.image_path = image_path

    def import_image(self):
        name = self.name_input.text()
        db_name = self.db_combo.currentText()

        try:
            # Establish connection to MySQL database
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Read image file
            with open(self.image_path, 'rb') as image_file:
                image_blob = image_file.read()

            # Insert data into the specified table
            insert_query = f"INSERT INTO {db_name} (Name, Image) VALUES (%s, %s)"
            cursor.execute(insert_query, (name, image_blob))
            conn.commit()

            cursor.close()
            conn.close()

            self.close()

        except mysql.connector.Error as error:
            print("Failed to insert image into MySQL table:", error)



class PhotoExplorerDialog(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Explore Photo')
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.setStyleSheet("background-color: #F2E8CF;")

        # Database selection
        self.db_label = QLabel('Database:')
        self.db_label.setStyleSheet("color: #101010;")
        self.db_combo = QComboBox()
        self.db_combo.addItems(['bottom', 'dresse', 'top'])
        self.db_combo.currentIndexChanged.connect(self.update_images)
        self.layout.addWidget(self.db_label)
        self.layout.addWidget(self.db_combo)

        # Image display
        self.image_label = QLabel()
        self.layout.addWidget(self.image_label)

        # Next button
        self.next_button = QPushButton('Next')
        self.next_button.clicked.connect(self.display_next_image)
        self.layout.addWidget(self.next_button)

        self.current_index = 0
        self.image_data = None
        self.display_images()

    def display_images(self):
        db_name = self.db_combo.currentText()

        try:
            # Establish connection to MySQL database
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Retrieve images from the specified table
            select_query = f"SELECT Image FROM {db_name}"
            cursor.execute(select_query)
            images = cursor.fetchall()

            if images:
                self.image_data = images
                self.current_index = 0  # Reset the current index when changing the table
                self.display_image()

            cursor.close()
            conn.close()

        except mysql.connector.Error as error:
            print("Failed to retrieve images from MySQL table:", error)

    def display_image(self):
        if self.image_data:
            image_data = self.image_data[self.current_index][0]
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)

            # Adjust the image size to fit the window while maintaining aspect ratio
            scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio)
            self.image_label.setPixmap(scaled_pixmap)

    def update_images(self):
        self.display_images()

    def display_next_image(self):
        if self.image_data:
            self.current_index = (self.current_index + 1) % len(self.image_data)
            self.display_image()



class SpecialFunctionDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Special Function')
        self.setGeometry(100, 100, 400, 200)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.setStyleSheet("background-color: #F2E8CF;")

        # Special function implementation
        self.special_label = QLabel('Special Function Implementation')
        self.special_label.setStyleSheet("color: #101010;")
        self.layout.addWidget(self.special_label)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    # Set window size
    window_width = 1200
    window_height = 600
    window.setFixedSize(window_width, window_height)

    # Set title style
    title_font = QFont('Arial Rounded MT Bold', 16)
    window.setWindowTitle('Wardrobe App')
    window.setFont(title_font)

    # Set text style
    text_font = QFont('Arial', 14)
    app.setFont(text_font)

    window.show()
    sys.exit(app.exec_())
