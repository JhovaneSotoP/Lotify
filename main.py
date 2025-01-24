import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QPushButton,QDoubleSpinBox,QSpinBox
from PyQt5 import uic
from tableModule import lotteryTable

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uipath="gui/mainView.ui"
        uic.loadUi(uipath,self)
        self.load_gui()
    
    def load_gui(self):
        """
        Conecta los elementos principales de la interfaz a su respectiva función.
        """
        self.stacked=self.findChild(QStackedWidget,"stackedWidget")
        self.stacked.setCurrentIndex(0)

        #Inicio
        self.findChild(QPushButton,"btnIniciar").clicked.connect(self.configuracionTabla)
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
    def configuracionTabla(self):
        self.nextIndexStacked()

        self.item_altoTabla=self.findChild(QDoubleSpinBox,"altoTabla")
        self.item_altoTabla.valueChanged.connect(self.actualizarComponentesTabla)

        self.item_anchoTabla=self.findChild(QDoubleSpinBox,"anchoTabla")
        self.item_anchoTabla.valueChanged.connect(self.actualizarComponentesTabla)

        self.item_elementosLado=self.findChild(QSpinBox,"elementosLado")
        self.item_elementosLado.valueChanged.connect(self.actualizarComponentesTabla)

        self.item_bordeImpresion=self.findChild(QDoubleSpinBox,"bordeImpresion")
        self.item_bordeImpresion.valueChanged.connect(self.actualizarComponentesTabla)

        self.item_espaciadoCartas=self.findChild(QDoubleSpinBox,"espaciadoCartas")
        self.item_espaciadoCartas.valueChanged.connect(self.actualizarComponentesTabla)

        self.item_encabezadoAltura=self.findChild(QDoubleSpinBox,"encabezadoAltura")
        self.item_encabezadoAltura.valueChanged.connect(self.actualizarComponentesTabla)

        self.miniatura=lotteryTable()

        self.actualizarComponentesTabla()

    def actualizarComponentesTabla(self):
        """
        Actualiza todos los compoenentes de los parametros iniciales de las tablas.
        """
        size=(self.item_anchoTabla.value(),self.item_altoTabla.value())
        self.miniatura.actualizarSize(size)
        self.miniatura.actualizarElementosLado(self.item_elementosLado.value())
        self.miniatura.imagen.show()


app=QApplication(sys.argv)
window=MainWindow()
window.show()

sys.exit(app.exec_())