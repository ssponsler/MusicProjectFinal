import sys
import clustering
import chartgen
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QLabel, QMessageBox, \
    QTabWidget


class FileSelectorTab(QWidget):
    def __init__(self):
        super().__init__()
        self.generate_button = None
        self.label = None
        self.select_button = None
        self.selected_file = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # error label if no file is currently selected
        self.label = QLabel('No file selected', self)
        layout.addWidget(self.label)

        # button to initiate file dialog
        self.select_button = QPushButton('Select File', self)
        self.select_button.clicked.connect(self.showFileDialog)
        layout.addWidget(self.select_button)

        # button to generate chart
        self.generate_button = QPushButton('Generate Chart', self)
        self.generate_button.clicked.connect(self.generateChart)
        layout.addWidget(self.generate_button)

        # main window layout
        self.setLayout(layout)

        self.selected_file = None

    def showFileDialog(self):
        # somehow this variable is being retained throughout execution
        self.selected_file = None
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*);;Audio Files (*.wav *.mp3)",
                                                   options=options)
        if file_path:
            self.selected_file = file_path
            # Update label
            self.label.setText(f'Selected File: {file_path}')

    def generateChart(self):
        if self.selected_file:
            try:
                chartgen.generate_chart(self.selected_file)
                QMessageBox.information(self, 'Success', 'Chart generated successfully!')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to generate chart: {e}')
        else:
            QMessageBox.warning(self, 'No File Selected', 'Please select a file first.')


class FolderSelectorTab(QWidget):
    def __init__(self):
        super().__init__()
        self.label = None
        self.select_button = None
        self.cluster_button = None
        self.selected_folder = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel('No folder selected', self)
        layout.addWidget(self.label)

        # button to initiate folder dialog
        self.select_button = QPushButton('Select Folder', self)
        self.select_button.clicked.connect(self.showFolderDialog)
        layout.addWidget(self.select_button)

        # button to cluster the files in the selected folder
        self.cluster_button = QPushButton('Cluster Folder', self)
        self.cluster_button.clicked.connect(self.clusterFolder)
        layout.addWidget(self.cluster_button)

        # main window layout
        self.setLayout(layout)

        self.selected_folder = None

    def showFolderDialog(self):
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", "", options=options)
        if folder_path:
            self.selected_folder = folder_path
            # update label
            self.label.setText(f'Selected Folder: {folder_path}')

    def clusterFolder(self):
        if self.selected_folder:
            try:
                # call the cluster function with the selected folder
                clustering.cluster_folder(self.selected_folder)
                QMessageBox.information(self, 'Success', 'Clustering completed successfully!')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to cluster folder: {e}')
        else:
            # show an error message if no folder is selected
            QMessageBox.warning(self, 'No Folder Selected', 'Please select a folder first.')


class App(QTabWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Song Decomposition')
        self.setGeometry(100, 100, 400, 200)

        # create tabs
        self.file_selector_tab = FileSelectorTab()
        self.folder_selector_tab = FolderSelectorTab()

        # add tabs
        self.addTab(self.file_selector_tab, "Song Profiler")
        self.addTab(self.folder_selector_tab, "Feature Clustering")

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
