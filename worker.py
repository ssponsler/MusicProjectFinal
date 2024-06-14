import sys
import clustering
import chartgen
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QLabel, QMessageBox, QTabWidget, QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal

class Worker(QThread):
    update_console = pyqtSignal(str)
    finished = pyqtSignal(bool)

    def __init__(self, func, *args):
        super().__init__()
        self.func = func
        self.args = args

    def run(self):
        try:
            self.func(*self.args)
            self.finished.emit(True)
        except Exception as e:
            self.update_console.emit(f"Error: {e}")
            self.finished.emit(False)
