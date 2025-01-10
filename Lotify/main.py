import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QPushButton
from PyQt5 import uic

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uipath="Lotify/gui/mainView.ui"
        uic.loadUi(uipath,self)
        self.load_gui()
    
    def load_gui(self):
        """
        Conecta los elementos principales de la interfaz a su respectiva función.
        """
        self.stacked=self.findChild(QStackedWidget,"stackedWidget")
        self.stacked.setCurrentIndex(0)

        #Inicio
        self.findChild(QPushButton,"btnIniciar").clicked.connect(self.nextIndexStacked)
        self.findChild(QPushButton,"btnSalir1").clicked.connect(self.exit)

        #Configuraxion de tablas
        self.findChild(QPushButton,"btnContinuar1").clicked.connect(self.nextIndexStacked)
        self.findChild(QPushButton,"btnSalir2").clicked.connect(self.exit)

        #Seleccionar imagenes
        self.findChild(QPushButton,"btnContinuar2").clicked.connect(self.nextIndexStacked)
        self.findChild(QPushButton,"btnSalir3").clicked.connect(self.exit)

        #Configuracion de cartas
        self.findChild(QPushButton,"btnContinuar3").clicked.connect(self.nextIndexStacked)
        self.findChild(QPushButton,"btnSalir4").clicked.connect(self.exit)

        
    
    def nextIndexStacked(self):
        """
        Aumenta en 1 el index del stackedWidget principal.
        """
        indiceActual=self.stacked.currentIndex()
        self.stacked.setCurrentIndex(indiceActual+1)
    
    def exit(self):
        """
        Termina el programa.
        """
        self.close()



app=QApplication(sys.argv)
window=MainWindow()
window.show()

sys.exit(app.exec_())