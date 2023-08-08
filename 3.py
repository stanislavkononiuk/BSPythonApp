from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QProgressBar
from bs4 import BeautifulSoup
import requests

percent=0
class TableData:
    def __init__(self, num, url, count, sub_urls):
        self.num = num
        self.url = url
        self.count = count
        self.sub_urls = sub_urls


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.rows = []
        self.table_data = []

        # Create the main widget
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create a layout for the main widget
        self.layout = QtWidgets.QGridLayout(self.central_widget)

        # Create a table
        self.table = QtWidgets.QTableWidget(self)
        self.layout.addWidget(self.table, 0, 0, 1, 2)

        # Define the columns
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["No", "url", "count", "sub urls"])

        # Set the table properties
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setColumnWidth(0, 30)
        self.table.setColumnWidth(1, 250)
        self.table.setColumnWidth(2, 50)
        self.table.setColumnWidth(3, 200)

        self.pbar = QProgressBar(self)
        self.pbar.setValue(0)
        self.layout.addWidget(self.pbar, 3, 0)

        # Create a button to browse the text file
        self.get_txt_button = QtWidgets.QPushButton("Get Text File")
        self.layout.addWidget(self.get_txt_button, 1, 0)

        # Create a label to display the selected text file
        self.label_txt = QtWidgets.QLabel("Click the button to browse the Text File")
        self.layout.addWidget(self.label_txt, 1, 1)

        # Create a button to save the result
        self.save_button = QtWidgets.QPushButton("Save")
        self.layout.addWidget(self.save_button, 2, 0)
        self.save_button.setEnabled(False)
        self.save_path = QtWidgets.QLabel("Click the button to save the Text File")
        self.layout.addWidget(self.save_path, 2, 1)

        # Connect the signals to the slots
        self.get_txt_button.clicked.connect(self.get_txt_file)
        self.save_button.clicked.connect(self.save_txt_file)

    def get_all_links(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all('a')
            all_links = []
            for link in links:
                href = link.get('href')
                if href:
                    all_links.append(href)
            return all_links
        except Exception as e:
            print("Error:", e)

    def get_txt_file(self):
        global percent
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Select a File", "./", "Text File (*.txt)")
            with open(file_path, 'r') as f:
                txt = f.readlines()
                i = 1
                
                for row_data in txt:
                    links = self.get_all_links(row_data)
                    if links is not None:
                        row = [str(i), row_data.strip(), str(len(links)), str(links)]
                    else:
                        row = [str(i), row_data.strip(), '0', '']
                    self.table.insertRow(i - 1)
                    for j, item in enumerate(row):
                        self.table.setItem(i - 1, j, QtWidgets.QTableWidgetItem(item))
                    self.table_data.append(TableData(row[0], row[1], row[2], row[3]))
                    i += 1
                    percent+=100/len(self.table_data)
                    print(percent) 
                    self.pbar.setValue(percent)
                    self.update()
                self.label_txt.setText(file_path)
                               
                self.save_button.setEnabled(True)
                self.update()
        except Exception as e:
            print("Error:", e)

    def save_txt_file(self):
        try:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Result", "./", "Result (*.txt)")
            if file_path:
                with open(file_path, "w") as file:
                    for row in self.table_data:
                        file.write(row.url + row.count + row.sub_urls + '\n')
                self.save_path.setText(file_path)

        except Exception as e:
            print("Error:", e)


# Create the application instance
app = QtWidgets.QApplication([])

# Create the main window
window = MainWindow()
window.show()

# Execute the application
app.exec_()
