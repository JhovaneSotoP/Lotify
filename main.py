import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QPushButton,QDoubleSpinBox,QSpinBox,QFileDialog,QLabel,QColorDialog,QLineEdit, QFontComboBox
from PyQt5 import uic
from PyQt5.QtCore import QThread,pyqtSignal,Qt
from PyQt5.QtGui import QPixmap
from tableModule import lotteryTable


#HILOS
class hiloMiniaturaTabla(QThread):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = None
        self.miniatura=lotteryTable()
    
    def setData(self,data):
        self.data=data

    def run(self):
        self.miniatura.actualizarSize(self.data['Size'])
        self.miniatura.actualizarElementosLado(self.data["elementosLado"])
        self.miniatura.actualizarBordeImpresion(self.data['bordeImpresion'])
        self.miniatura.actualizarEspaciadoCartas(self.data['espacioCartas'])
        self.miniatura.actualizarEspacioHeader(self.data["encabezadoAltura"])
        self.miniatura.actualizarLogo(self.data['pathLogo'])
        self.miniatura.actualizarFondo(self.data['pathFondo'])
        self.miniatura.actualizarEncabezado(self.data['titulo'])
        self.miniatura.actualizarLetraEncabezado(self.data["tipoLetra"])
        self.miniatura.actualizarTamanoLetraEncabezado(self.data["tamanoLetra"])
        self.miniatura.actualizarColorLetraEncabezado(self.data["colorLetra"])
        self.miniatura.imagen.save("data/Output/miniaturaTabla.png")


        

#CLASE PRINCIPAL
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


        #GUI DE CONFIGURACION BASICA DE TABLA

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

        self.item_logo=self.findChild(QPushButton,"seleccionarLogo")
        self.item_logo.clicked.connect(self.seleccionarLogoPath)

        self.item_pathLogo=self.findChild(QLabel,"pathLogo")
        self.logoPath=""

        self.item_fondo=self.findChild(QPushButton,"seleccionarFondo")
        self.item_fondo.clicked.connect(self.seleccionarFondoPath)

        self.item_pathFondo=self.findChild(QLabel,"fondoPath")
        self.fondoPath=""
        

        self.item_colorLetraTabla=self.findChild(QPushButton,"colorLetraTabla")
        self.item_colorLetraTabla.clicked.connect(self.seleccionarColorLetraTabla)

        self.colorDeLetraTabla="#000000"

        self.cambiarFondoBoton(self.item_colorLetraTabla,self.colorDeLetraTabla)


        self.item_tituloTabla=self.findChild(QLineEdit,"tituloLoteria")
        self.item_tituloTabla.textChanged.connect(self.actualizarComponentesTabla)

        self.item_letraTabla=self.findChild(QFontComboBox,"letraTabla")
        self.item_letraTabla.currentFontChanged.connect(self.actualizarComponentesTabla)

        self.item_tamanoLetraTabla=self.findChild(QSpinBox,"tamanoLetraTabla")
        self.item_tamanoLetraTabla.valueChanged.connect(self.actualizarComponentesTabla)

        self.item_labelTabla=self.findChild(QLabel,"previsualizacionTabla")
        
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

        self.tabla=lotteryTable()

        self.hiloMiniaturaTabla=hiloMiniaturaTabla()
        self.hiloMiniaturaTabla.finished.connect(self.actualizarMiniaturaTabla)

        self.actualizarComponentesTabla()

    def actualizarComponentesTabla(self):
        """
        Actualiza todos los compoenentes de los parametros iniciales de las tablas.
        """
        data={}
        size=(self.item_anchoTabla.value(),self.item_altoTabla.value())
        data.update({"Size":size})
        data.update({"elementosLado":self.item_elementosLado.value()})
        data.update({"bordeImpresion":self.item_bordeImpresion.value()})
        data.update({"espacioCartas":self.item_espaciadoCartas.value()})
        data.update({"encabezadoAltura":self.item_encabezadoAltura.value()})
        data.update({"pathLogo":self.logoPath})
        data.update({"pathFondo":self.fondoPath})
        data.update({"titulo":self.item_tituloTabla.text()})
        data.update({"tipoLetra":self.item_letraTabla.currentText()})
        data.update({"tamanoLetra":self.item_tamanoLetraTabla.value()})
        data.update({"colorLetra":self.colorDeLetraTabla})
        self.hiloMiniaturaTabla.setData(data)
        self.hiloMiniaturaTabla.start()
    
    def actualizarMiniaturaTabla(self):
        ruta="data/Output/miniaturaTabla.png"

        pixmap = QPixmap(ruta)  # Reemplaza con la ruta de tu imagen
        scaled_pixmap = pixmap.scaled(self.item_labelTabla.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.item_labelTabla.setPixmap(scaled_pixmap)
    
    def seleccionarLogoPath(self):
        temp=self.seleccionarImagen()
        if temp:
            self.logoPath=temp
        else:
            self.logoPath=""
        
        self.item_pathLogo.setText(self.logoPath)

        self.actualizarComponentesTabla()
    
    def seleccionarFondoPath(self):
        temp=self.seleccionarImagen()
        if temp:
            self.fondoPath=temp
        else:
            self.fondoPath=""
        
        self.item_pathFondo.setText(self.fondoPath)

        self.actualizarComponentesTabla()
        
    def seleccionarImagen(self):
        salida=QFileDialog.getOpenFileName(self,"Seleccionar imagen","","Imagenes (*.jpg *.png)")
        if salida==('', ''):
            return None
        else:
            return salida[0]
    
    def seleccionarColorLetraTabla(self):
        temp=self.seleccionarColor()
        if temp:
            self.colorDeLetraTabla=temp
        self.cambiarFondoBoton(self.item_colorLetraTabla,self.colorDeLetraTabla)
        self.actualizarComponentesTabla()
        
    
    def seleccionarColor(self):
        color=QColorDialog.getColor()
        if color.isValid():
            salida=color.name()
        else:
            salida=None
        return salida
    
    def cambiarFondoBoton(self,boton:QPushButton,color:str):
        boton.setStyleSheet(f"background:{color};")



app=QApplication(sys.argv)
window=MainWindow()
window.show()

sys.exit(app.exec_())