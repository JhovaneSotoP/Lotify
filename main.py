import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QPushButton,QDoubleSpinBox,QSpinBox,QFileDialog,QLabel,QColorDialog,QLineEdit, QFontComboBox,QTableWidget,QTableWidgetItem, QProgressBar,QCheckBox
from PyQt5 import uic
from PyQt5.QtCore import QThread,pyqtSignal,Qt
from PyQt5.QtGui import QPixmap
from tableModule import lotteryTable
from cardModule import lotteryCard
import os
import random
import math
from generalFuntions_module import indextablas

loteria=lotteryTable()
dataBrutaCartas=[]
carta=lotteryCard()
pathCartas=[]
pathSalida=""

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


class hiloMiniaturaCarta(QThread):
    """
    Hilo secundario que actualiza las caracteristicas de la carta, ademas que genera y guarda una miniatura.
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
        card=random.choice(dataBrutaCartas)
        carta.actualizarImagen(card["path"])
        carta.actualizarTextoSuperior(card["numero"])
        carta.actualizarTextoInferior(card["titulo"])
        
        carta.actualizarDimensiones(self.data["size"])
        carta.actualizarTipoLetra(self.data["tipoLetraCarta"])
        carta.actualizarTamanoLetra(self.data["tamanoLetraCarta"])
        carta.actualizarColorTextoSuperior(self.data["colorLetraCartaArriba"])
        carta.actualizarColorTextoInferior(self.data["colorLetraCartaAbajo"])

        carta.actualizarColorBordePrincipal(self.data["colorBordeGeneral"])
        carta.actualizarColorBordeSuperior(self.data["colorBordeArriba"])
        carta.actualizarColorBordeInferior(self.data["colorBordeAbajo"])

        carta.actualizarGrosorBordePrincipal(self.data["anchoBordeGeneral"])
        carta.actualizarGrosorBordeSuperior(self.data["anchoBordeArriba"])
        carta.actualizarGrosorBordeInferior(self.data["anchoBordeArriba_2"])

        carta.actualizarOrientacionSuperior(self.data["orientacionArriba"])
        carta.actualizarOrientacionInferior(self.data["orientacionAbajo"])

        carta.actualizarEspaciadoHSuperior(self.data["horizontalArriba"])
        carta.actualizarEspaciadoHInferior(self.data["horizontalAbajo"])

        carta.actualizarEspaciadoVSuperior(self.data["verticalArriba"])
        carta.actualizarEspaciadoVInferior(self.data["verticalAbajo"])

        carta.imagen.save("data/Output/miniaturaCarta.png")

class generarCartas(QThread):
    progresoText=pyqtSignal(str)
    progresoInt=pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        global pathCartas
        pathCartas=[]
        max=len(dataBrutaCartas)
        self.progresoText.emit("Iniciando la generacion de cartas")
        for index,card in enumerate(dataBrutaCartas):
            carta.actualizarImagen(card["path"])
            carta.actualizarTextoSuperior(card["numero"])
            carta.actualizarTextoInferior(card["titulo"])
            pathCartas.append(carta.guardar())
            self.progresoText.emit(f"{index+1}/{max} cartas generadas.")
            self.progresoInt.emit(int((index+1)*100/max))

class hiloGenerarLoteria(QThread):
    progresoText=pyqtSignal(str)
    progresoInt=pyqtSignal(int)

    def __init__(self, parent=None, demoBool=False,insBool=True):
        super().__init__(parent)
        self.demoBool=demoBool
        self.insBool=insBool
    
    def run(self):
        self.progresoInt.emit(0)
        self.progresoText.emit("Comenzando...")
        loteria.generarLoteria(pathSalida)
        if self.insBool:
            loteria.colocarInstrucciones()
        self.progresoText.emit("Colocando cartas...")
        loteria.colocarCartas()
        self.progresoText.emit("Generando tablas")
        
        index=indextablas(loteria.noTablas,len(pathCartas),(loteria.elementosLado*loteria.elementosLado))
        for index,n in enumerate(index):
            loteria.agregarTabla(n)
            self.progresoInt.emit(int((index+1)*100/loteria.noTablas))
            self.progresoText.emit(f"{index+1}/{loteria.noTablas} tablas colocadas.")
        
        if self.demoBool:
            loteria.demo.save()
        loteria.contadorTabla=1
        loteria.archivo.save()



        

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
        self.findChild(QPushButton,"btnContinuar3").clicked.connect(self.procesarImagenes)
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

        #GUI de configuracion de cartas
        self.item_tipoLetraCarta=self.findChild(QFontComboBox,"tipoLetraCarta")
        self.item_tamanoLetraCarta=self.findChild(QSpinBox,"tamanoLetraCarta")

        self.item_colorLetraCartaArriba=self.findChild(QPushButton,"colorLetraCartaArriba")
        self.item_colorLetraCartaAbajo=self.findChild(QPushButton,"colorLetraCartaAbajo")

        self.item_colorBordeGeneral=self.findChild(QPushButton,"colorBordeGeneral")
        self.item_colorBordeArriba=self.findChild(QPushButton,"colorBordeArriba")
        self.item_colorBordeAbajo=self.findChild(QPushButton,"colorBordeAbajo")

        self.item_anchoBordeGeneral=self.findChild(QSpinBox,"anchoBordeGeneral")
        self.item_anchoBordeArriba=self.findChild(QSpinBox,"anchoBordeArriba")
        self.item_anchoBordeArriba_2=self.findChild(QSpinBox,"anchoBordeArriba_2")

        self.item_izquierdaArriba=self.findChild(QPushButton,"izquierdaArriba")
        self.item_centroArriba=self.findChild(QPushButton,"centroArriba")
        self.item_derechaArriba=self.findChild(QPushButton,"derechaArriba")

        self.item_horizontalArriba=self.findChild(QDoubleSpinBox,"horizontalArriba")
        self.item_verticalArriba=self.findChild(QDoubleSpinBox,"verticalArriba")

        self.item_izquierdaAbajo=self.findChild(QPushButton,"izquierdaAbajo")
        self.item_centroAbajo=self.findChild(QPushButton,"centroAbajo")
        self.item_derechaAbajo=self.findChild(QPushButton,"derechaAbajo")

        self.item_horizontalAbajo=self.findChild(QDoubleSpinBox,"horizontalAbajo")
        self.item_verticalAbajo=self.findChild(QDoubleSpinBox,"verticalAbajo")

        self.item_tipoLetraCarta.currentFontChanged.connect(self.actualizarComponentesCarta)

        self.item_tamanoLetraCarta.valueChanged.connect(self.actualizarComponentesCarta)

        self.item_anchoBordeGeneral.valueChanged.connect(self.actualizarComponentesCarta)
        self.item_anchoBordeArriba.valueChanged.connect(self.actualizarComponentesCarta)
        self.item_anchoBordeArriba_2.valueChanged.connect(self.actualizarComponentesCarta)

        self.item_horizontalArriba.valueChanged.connect(self.actualizarComponentesCarta)
        self.item_verticalArriba.valueChanged.connect(self.actualizarComponentesCarta)

        self.item_horizontalAbajo.valueChanged.connect(self.actualizarComponentesCarta)
        self.item_verticalAbajo.valueChanged.connect(self.actualizarComponentesCarta)


        self.value_colorLetraCartaArriba="#000000"
        self.value_colorLetraCartaAbajo="#000000"

        self.value_colorBordeGeneral="#000000"
        self.value_colorBordeArriba="#FFFFFF"
        self.value_colorBordeAbajo="#FFFFFF"



        self.item_colorLetraCartaArriba.clicked.connect(self.actualizar_colorLetraCartaArriba)
        self.item_colorLetraCartaAbajo.clicked.connect(self.actualizar_colorLetraCartaAbajo)

        self.item_colorBordeGeneral.clicked.connect(self.actualizar_colorBordeGeneral)
        self.item_colorBordeArriba.clicked.connect(self.actualizar_colorBordeArriba)
        self.item_colorBordeAbajo.clicked.connect(self.actualizar_colorBordeAbajo)

        self.item_izquierdaArriba.clicked.connect(self.actualizar_izquierdaArriba)
        self.item_centroArriba.clicked.connect(self.actualizar_centroArriba)
        self.item_derechaArriba.clicked.connect(self.actualizar_derechaArriba)

        self.item_izquierdaAbajo.clicked.connect(self.actualizar_izquierdaAbajo)
        self.item_centroAbajo.clicked.connect(self.actualizar_centroAbajo)
        self.item_derechaAbajo.clicked.connect(self.actualizar_derechaAbajo)

        self.cambiarFondoBoton(self.item_colorLetraCartaArriba,self.value_colorLetraCartaArriba)
        self.cambiarFondoBoton(self.item_colorLetraCartaAbajo,self.value_colorLetraCartaAbajo)

        self.cambiarFondoBoton(self.item_colorBordeGeneral,self.value_colorBordeGeneral)
        self.cambiarFondoBoton(self.item_colorBordeArriba,self.value_colorBordeArriba)
        self.cambiarFondoBoton(self.item_colorBordeAbajo,self.value_colorBordeAbajo)

        self.value_orientacionArriba="R"
        self.value_orientacionAbajo="C"

        self.orientacionTextoCartas(self.value_orientacionArriba,self.item_izquierdaArriba,self.item_centroArriba,self.item_derechaArriba)
        self.orientacionTextoCartas(self.value_orientacionAbajo,self.item_izquierdaAbajo,self.item_centroAbajo,self.item_derechaAbajo)
        
        self.item_miniaturaCarta=self.findChild(QLabel,"previsualizacionCarta")

        #GUI PROCESAR CARTAS

        self.item_progresoCarta=self.findChild(QLabel,"labelCargaCarta")
        self.item_barraProgresoCarta=self.findChild(QProgressBar,"barraCargaCarta")
        
        #GUI CONFIGURACION FINAL
        self.item_noTablas=self.findChild(QSpinBox,"numeroTablas")
        self.item_bordeCartas=self.findChild(QDoubleSpinBox,"bordeCartas")
        self.item_escalaCartas=self.findChild(QDoubleSpinBox,"escalaCartas")
        self.item_salida=self.findChild(QPushButton,"seleccionarSalida")
        self.item_pathSalida=self.findChild(QLabel,"pathSalida")
        self.item_salida.clicked.connect(self.seleccionarPathSalida)

        self.item_demo=self.findChild(QCheckBox,"demo")
        self.item_instrucciones=self.findChild(QCheckBox,"instrucciones")

        self.item_btnTerminar=self.findChild(QPushButton,"terminar")
        self.item_btnTerminar.clicked.connect(self.generarLoteria)
        
        self.item_btnTerminar.setEnabled(False)

        #GUI carga final

        self.item_progresoTabla=self.findChild(QLabel,"labelCargaArchivo")
        self.item_barraProgresoTabla=self.findChild(QProgressBar,"barraCargaArchivo")

        
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
        global dataBrutaCartas
        dataBrutaCartas=[]

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
        if data:
            for n in data:
                count=self.item_tablaImagenes.rowCount()
                self.item_tablaImagenes.insertRow(count)
                temp=os.path.splitext(os.path.basename(n))[0]
                temp=temp.split("_")

                self.item_tablaImagenes.setItem(count,0,QTableWidgetItem(temp[0].upper()))

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
        print(salida)
        if salida==([], ''):
            return None
        else:
            return salida[0]
    
    def tablaActualizada(self):
        max=self.item_elementosLado.value()*self.item_elementosLado.value()
        if self.item_tablaImagenes.rowCount()>max:
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
            
            dataBrutaCartas.append(dic)
        self.nextIndexStacked()

        
        self.hiloMiniaturaCarta=hiloMiniaturaCarta()
        self.hiloMiniaturaCarta.finished.connect(self.actualizarMiniaturaCarta)
        self.actualizarComponentesCarta()
    
    def actualizarComponentesCarta(self):
        data={}
        
        data.update({"size":loteria.sizeCartas()})
        data.update({"tipoLetraCarta":self.item_tipoLetraCarta.currentText()})
        data.update({"tamanoLetraCarta":self.item_tamanoLetraCarta.value()})

        data.update({"colorLetraCartaArriba":self.value_colorLetraCartaArriba})
        data.update({"colorLetraCartaAbajo":self.value_colorLetraCartaAbajo})

        data.update({"colorBordeGeneral":self.value_colorBordeGeneral})
        data.update({"colorBordeArriba":self.value_colorBordeArriba})
        data.update({"colorBordeAbajo":self.value_colorBordeAbajo})

        data.update({"anchoBordeGeneral":self.item_anchoBordeGeneral.value()})
        data.update({"anchoBordeArriba":self.item_anchoBordeArriba.value()})
        data.update({"anchoBordeArriba_2":self.item_anchoBordeArriba_2.value()})

        data.update({"orientacionArriba":self.value_orientacionArriba})

        data.update({"horizontalArriba":self.item_horizontalArriba.value()})
        data.update({"verticalArriba":self.item_verticalArriba.value()})

        data.update({"orientacionAbajo":self.value_orientacionAbajo})

        data.update({"horizontalAbajo":self.item_horizontalAbajo.value()})
        data.update({"verticalAbajo":self.item_verticalAbajo.value()})

        self.hiloMiniaturaCarta.setData(data)
        self.hiloMiniaturaCarta.start()




    
    
    def actualizar_colorLetraCartaArriba(self):
        temp=self.seleccionarColor()
        if temp:
            self.value_colorLetraCartaArriba=temp
        self.cambiarFondoBoton(self.item_colorLetraCartaArriba,self.value_colorLetraCartaArriba)
        self.actualizarComponentesCarta()

    def actualizar_colorLetraCartaAbajo(self):
        temp=self.seleccionarColor()
        if temp:
            self.value_colorLetraCartaAbajo=temp
        self.cambiarFondoBoton(self.item_colorLetraCartaAbajo,self.value_colorLetraCartaAbajo)
        self.actualizarComponentesCarta()
        
    def actualizar_colorBordeGeneral(self):
        temp=self.seleccionarColor()
        if temp:
            self.value_colorBordeGeneral=temp
        self.cambiarFondoBoton(self.item_colorBordeGeneral,self.value_colorBordeGeneral)
        self.actualizarComponentesCarta()
        
    def actualizar_colorBordeArriba(self):
        temp=self.seleccionarColor()
        if temp:
            self.value_colorBordeArriba=temp
        self.cambiarFondoBoton(self.item_colorBordeArriba,self.value_colorBordeArriba)
        self.actualizarComponentesCarta()
        
    def actualizar_colorBordeAbajo(self):
        temp=self.seleccionarColor()
        if temp:
            self.value_colorBordeAbajo=temp
        self.cambiarFondoBoton(self.item_colorBordeAbajo,self.value_colorBordeAbajo)
        self.actualizarComponentesCarta()
        





    def actualizar_izquierdaArriba(self):

        self.value_orientacionArriba="L"
        self.orientacionTextoCartas(self.value_orientacionArriba,self.item_izquierdaArriba,self.item_centroArriba,self.item_derechaArriba)
        self.actualizarComponentesCarta()
        
    def actualizar_centroArriba(self):
        self.value_orientacionArriba="C"
        self.orientacionTextoCartas(self.value_orientacionArriba,self.item_izquierdaArriba,self.item_centroArriba,self.item_derechaArriba)
        self.actualizarComponentesCarta()
        
    def actualizar_derechaArriba(self):
        self.value_orientacionArriba="R"
        self.orientacionTextoCartas(self.value_orientacionArriba,self.item_izquierdaArriba,self.item_centroArriba,self.item_derechaArriba)
        self.actualizarComponentesCarta()
        




    def actualizar_izquierdaAbajo(self):
        self.value_orientacionAbajo="L"
        self.orientacionTextoCartas(self.value_orientacionAbajo,self.item_izquierdaAbajo,self.item_centroAbajo,self.item_derechaAbajo)
        self.actualizarComponentesCarta()
        
    def actualizar_centroAbajo(self):
        self.value_orientacionAbajo="C"
        self.orientacionTextoCartas(self.value_orientacionAbajo,self.item_izquierdaAbajo,self.item_centroAbajo,self.item_derechaAbajo)
        self.actualizarComponentesCarta()
        
    def actualizar_derechaAbajo(self):
        
        self.value_orientacionAbajo="R"
        self.orientacionTextoCartas(self.value_orientacionAbajo,self.item_izquierdaAbajo,self.item_centroAbajo,self.item_derechaAbajo)
        self.actualizarComponentesCarta()
        
    def orientacionTextoCartas(self,valor:str,itemL:QPushButton,itemC:QPushButton,itemR:QPushButton):
        colorResalte="#DCDCDC"
        color="#FFFFFF"

        if valor=="L":
            self.cambiarFondoBoton(itemL,colorResalte)
            self.cambiarFondoBoton(itemC,color)
            self.cambiarFondoBoton(itemR,color)
        elif valor=="C":
            self.cambiarFondoBoton(itemL,color)
            self.cambiarFondoBoton(itemC,colorResalte)
            self.cambiarFondoBoton(itemR,color)
        elif valor=="R":
            self.cambiarFondoBoton(itemL,color)
            self.cambiarFondoBoton(itemC,color)
            self.cambiarFondoBoton(itemR,colorResalte)
    
    def actualizarMiniaturaCarta(self):
        """
        Actualzia en la seccion configuracionde tabla su miniatura.
        """
        ruta="data/Output/miniaturaCarta.png"

        pixmap = QPixmap(ruta)  # Reemplaza con la ruta de tu imagen
        scaled_pixmap = pixmap.scaled(self.item_miniaturaCarta.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.item_miniaturaCarta.setPixmap(scaled_pixmap)


    def procesarImagenes(self):
        self.nextIndexStacked()
        self.hiloP=generarCartas()
        self.hiloP.finished.connect(self.configuracionFinal)
        self.hiloP.progresoText.connect(self.actualizarEtiquetaCargaCarta)
        self.hiloP.progresoInt.connect(self.actualizarBarraCargaCarta)
        self.hiloP.start()

    def actualizarEtiquetaCargaCarta(self,cad:str):
        self.item_progresoCarta.setText(cad)
    def actualizarBarraCargaCarta(self,num:int):
        self.item_barraProgresoCarta.setValue(num)

    def configuracionFinal(self):
        self.nextIndexStacked()
        cartasMax=math.comb(len(pathCartas),loteria.elementosLado*loteria.elementosLado)
        if cartasMax>2147483646:
            cartasMax=2147483646
        self.item_noTablas.setMaximum(cartasMax)
        if cartasMax>250:
            self.item_noTablas.setValue(200)
        else:
            self.item_noTablas.setValue(cartasMax)

        loteria.actualizarCartas(pathCartas)

    def seleccionarPathSalida(self):
        path=QFileDialog.getSaveFileName(self,"Guardar como","","Archivos PDF (*.pdf)")
        global pathSalida
        if path==('', ''):
            pathSalida=""
            self.item_btnTerminar.setEnabled(False)
        else:
            pathSalida=path[0]
            self.item_btnTerminar.setEnabled(True)

        self.item_pathSalida.setText(pathSalida)    

    def generarLoteria(self):
        loteria.noTablas=self.item_noTablas.value()
        loteria.escalaCarta=self.item_escalaCartas.value()
        loteria.espaciadoCartas=self.item_espaciadoCartas.value()
        #print("Estoy dentro")
        self.nextIndexStacked()
        self.hiloL=hiloGenerarLoteria(demoBool=self.item_demo.isChecked(),insBool=self.item_instrucciones.isChecked())
        self.hiloL.finished.connect(self.terminado)
        self.hiloL.progresoText.connect(self.actualizarCadProgresoTabla)
        self.hiloL.progresoInt.connect(self.actualizarIntProgresoTabla)
        self.hiloL.start()
        for n in range(self.item_tablaImagenes.rowCount()):
            self.item_tablaImagenes.removeRow(0)

    def actualizarCadProgresoTabla(self,cad:str):
        self.item_progresoTabla.setText(cad)
    def actualizarIntProgresoTabla(self,num:int):
        self.item_barraProgresoTabla.setValue(num)

    def terminado(self):
        global pathCartas
        for n in pathCartas:
            os.remove(n)
        pathCartas=[]
        self.stacked.setCurrentIndex(0)

app=QApplication(sys.argv)
window=MainWindow()
window.show()

sys.exit(app.exec_())