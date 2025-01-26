import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QPushButton,QDoubleSpinBox,QSpinBox,QFileDialog,QLabel,QColorDialog,QLineEdit, QFontComboBox,QTableWidget,QTableWidgetItem
from PyQt5 import uic
from PyQt5.QtCore import QThread,pyqtSignal,Qt
from PyQt5.QtGui import QPixmap
from tableModule import lotteryTable
import os
import random

loteria=lotteryTable()
#HILOS
class hiloMiniaturaTabla(QThread):
    """
    Hilo secundario que actualiza las caracteristicas de la loteria, ademas que genera y guarda una miniatura.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = None
    
    def setData(self,data):
        self.data=data

    def run(self):
        """
        Inicio de la funcion para actualizar parametros de la loteria.
        """
        global loteria
        loteria.actualizarSize(self.data['Size'])
        loteria.actualizarElementosLado(self.data["elementosLado"])
        loteria.actualizarBordeImpresion(self.data['bordeImpresion'])
        loteria.actualizarEspaciadoCartas(self.data['espacioCartas'])
        loteria.actualizarEspacioHeader(self.data["encabezadoAltura"])
        loteria.actualizarLogo(self.data['pathLogo'])
        loteria.actualizarFondo(self.data['pathFondo'])
        loteria.actualizarEncabezado(self.data['titulo'])
        loteria.actualizarLetraEncabezado(self.data["tipoLetra"])
        loteria.actualizarTamanoLetraEncabezado(self.data["tamanoLetra"])
        loteria.actualizarColorLetraEncabezado(self.data["colorLetra"])
        loteria.imagen.save("data/Output/miniaturaTabla.png")


        

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

        #GUI importar imagenes
        self.item_tablaImagenes=self.findChild(QTableWidget,"tablaImagenes")
        self.item_tablaImagenes.model().rowsInserted.connect(self.tablaActualizada)
        self.item_tablaImagenes.model().rowsRemoved.connect(self.tablaActualizada)

        self.item_importarImagen=self.findChild(QPushButton,"importarImagen")
        self.item_importarImagen.clicked.connect(self.importarImagenes)

        self.item_eliminarImagen=self.findChild(QPushButton,"eliminarImagen")
        self.item_eliminarImagen.clicked.connect(self.remove_row)

        self.item_continuarImportacion=self.findChild(QPushButton,"btnContinuar2")
        self.item_continuarImportacion.clicked.connect(self.continuarImportacion)
        self.item_continuarImportacion.setEnabled(False)
        
        
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


        self.hiloMiniaturaTabla=hiloMiniaturaTabla()
        self.hiloMiniaturaTabla.finished.connect(self.actualizarMiniaturaTabla)

        self.actualizarComponentesTabla()

        self.dataBrutaCartas=[]

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
        """
        Actualzia en la seccion configuracionde tabla su miniatura.
        """
        ruta="data/Output/miniaturaTabla.png"

        pixmap = QPixmap(ruta)  # Reemplaza con la ruta de tu imagen
        scaled_pixmap = pixmap.scaled(self.item_labelTabla.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.item_labelTabla.setPixmap(scaled_pixmap)
    
    def seleccionarLogoPath(self):
        """
        Selecciona el logo de la tabla
        """
        temp=self.seleccionarImagen()
        if temp:
            self.logoPath=temp
        else:
            self.logoPath=""
        
        self.item_pathLogo.setText(self.logoPath)

        self.actualizarComponentesTabla()
    
    def seleccionarFondoPath(self):
        """
        Selecciona el fondo de cada tabla
        """
        temp=self.seleccionarImagen()
        if temp:
            self.fondoPath=temp
        else:
            self.fondoPath=""
        
        self.item_pathFondo.setText(self.fondoPath)

        self.actualizarComponentesTabla()
        
    def seleccionarImagen(self):
        """
        Funcion que abre un dialogo para seleccionar imagenes (JPG y PNG) y retorna su path.

        Return:
        salida(str): path que dirige a la imagen seleccionada.
        """
        salida=QFileDialog.getOpenFileName(self,"Seleccionar imagen","","Imagenes (*.jpg *.png)")
        if salida==('', ''):
            return None
        else:
            return salida[0]
    
    def seleccionarColorLetraTabla(self):
        """
        Actualiza el color de la letra de la tabla.
        """
        temp=self.seleccionarColor()
        if temp:
            self.colorDeLetraTabla=temp
        self.cambiarFondoBoton(self.item_colorLetraTabla,self.colorDeLetraTabla)
        self.actualizarComponentesTabla()
        
    
    def seleccionarColor(self):
        """
        Funcion que abre un dialogo para seleccionar colores y retorna su hexadecimal.

        Return:
        salida(str): Hexadecimal del color seleccionado.
        """
        color=QColorDialog.getColor()
        if color.isValid():
            salida=color.name()
        else:
            salida=None
        return salida
    
    def cambiarFondoBoton(self,boton:QPushButton,color:str):
        """
        Cambia el color del fondo del boton enviado.
        """
        boton.setStyleSheet(f"background:{color};")
    
    def importarImagenes(self):
        data=self.seleccionarImagenesPath()
        for n in data:
            count=self.item_tablaImagenes.rowCount()
            self.item_tablaImagenes.insertRow(count)
            temp=os.path.splitext(os.path.basename(n))[0]
            temp=temp.split("_")

            self.item_tablaImagenes.setItem(count,0,QTableWidgetItem(temp[0]))

            if len(temp)>1:
                try:
                    datoPrueba=int(temp[1])
                    dato2=temp[1]

                except:
                    dato2=""
            else: 
                dato2=""
            
            self.item_tablaImagenes.setItem(count,1,QTableWidgetItem(dato2))
            self.item_tablaImagenes.setItem(count,2,QTableWidgetItem(n))
        self.item_tablaImagenes.resizeColumnsToContents()
    
    def seleccionarImagenesPath(self):
        """
        Funcion que abre un dialogo para seleccionar imagenes (JPG y PNG) y retorna su path.

        Return:
        salida(list): lista de path que dirige a las imagenes seleccionadas.
        """
        salida=QFileDialog.getOpenFileNames(self,"Seleccionar imagen","","Imagenes (*.jpg *.png)")
        if salida==([], ''):
            return None
        else:
            return salida[0]
    
    def tablaActualizada(self):
        if self.item_tablaImagenes.rowCount()>0:
            self.item_continuarImportacion.setEnabled(True)
        else:
            self.item_continuarImportacion.setEnabled(False)
    
    def remove_row(self):
        selected_rows = self.item_tablaImagenes.selectionModel().selectedRows()
        for index in sorted(selected_rows, reverse=True):  # Eliminar de abajo hacia arriba
            self.item_tablaImagenes.removeRow(index.row())
    
    def continuarImportacion(self):
        num=[]
        for n in range(self.item_tablaImagenes.rowCount()):
            num.append(n)


        for n in range(self.item_tablaImagenes.rowCount()):
            dic={}

            item=self.item_tablaImagenes.item(n,0)
            data=item.text() if item else ""
            dic.update({"titulo":data})

            item=self.item_tablaImagenes.item(n,1)
            data=item.text() if item else ""
            if data=="":
                numero=random.choice(num)
                num.remove(numero)
                data=str(numero)
            dic.update({"numero":data})

            item=self.item_tablaImagenes.item(n,2)
            data=item.text() if item else ""

            if os.path.exists(data):
                dic.update({"path":data})
            else:
                print(data)
                continue
            
            self.dataBrutaCartas.append(dic)
        print(self.dataBrutaCartas)
        self.nextIndexStacked()



app=QApplication(sys.argv)
window=MainWindow()
window.show()

sys.exit(app.exec_())