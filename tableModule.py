from PIL import Image,ImageDraw, ImageOps, ImageFont
import random
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from generalFuntions_module import encontrar_archivo_fuente,hex_to_rgb

class lotteryTable():
    def __init__(self):
        """
        Inicializa los parametros de las tablas de la loteria
        """
        self.ancho=8.5
        self.alto=11
        self.ppp=96

        self.elementosLado=4
        self.bordeImpresion=0.25
        self.espaciadoCartas=0.15

        self.espacioHeader=0.3


        self.anchoCartas=0
        self.altoCartas=0

        self.logo=""
        self.fondo=""
        self.encabezado="Loteria"

        self.tipoLetra=encontrar_archivo_fuente("Arial")
        self.tamanoLetra=24
        self.colorLetra="#000000"

        self.contadorTabla=1

        self.bordeCartas=0.2
        self.escalaCarta=1.3
        self.cartas=[]

        self.noTablas=1
        self.instrucciones=True
        self.demo=True
        self.salida="data/output/"

        self.actualizarMiniatura()

    def actualizarMiniatura(self):
        """
        Actualiza la miniatura de la tabla.
        """
        #Crear imagen
        self.imagen=Image.new("RGBA",(int(self.ancho*self.ppp),int(self.alto*self.ppp)),"#FFFFFF")

        #Crear dibujante y generar las coordenadas de las cartas
        dibujo=ImageDraw.Draw(self.imagen)
        self.generarCoordenadas()

        #colocar fondo
        if(self.fondo!=""):
            try:
                fondo = Image.open(self.fondo)
                fondo=ImageOps.fit(fondo,self.imagen.size)
                x = 0
                y = 0
                self.imagen.paste(fondo,(x,y))
            except FileNotFoundError:
                print(f"El archivo '{self.logo}' no se encuentra.")
            except PermissionError:
                print(f"Permiso denegado al intentar acceder al archivo '{self.logo}'.")
            except Exception as e:
                print(f"Error inesperado: {e}")

        #colocar encabezado
        font=ImageFont.truetype(self.tipoLetra,self.tamanoLetra)

        tam=font.getbbox(self.encabezado)
        tamX=tam[2]-tam[0]
        tamY=tam[3]-tam[1]
        
        x=self.bordeImpresion*self.ppp
        y=(((self.espacioHeader*self.ppp)-tamY)//2)+(self.bordeImpresion*self.ppp)
        dibujo.text((x,y),self.encabezado,fill=self.colorLetra,font=font)

        cad="Tabla #"+str(self.contadorTabla)
        tam=font.getbbox(cad)
        tamX=tam[2]-tam[0]
        tamY=tam[3]-tam[1]
        
        x=self.imagen.width-(self.bordeImpresion*self.ppp)-tamX
        y=(((self.espacioHeader*self.ppp)-tamY)//2)+(self.bordeImpresion*self.ppp)
        dibujo.text((x,y),cad,fill=self.colorLetra,font=font)

        #Modificar coordenadas a lienzo actual
        coordsPX=[]
        for n in self.coords:
            coordsPX.append((n[0]*self.ppp,n[1]*self.ppp))
        
        #colocar imagenes
        for n in coordsPX:
            color=(random.randint(50,200),random.randint(50,200),random.randint(50,200))
            dibujo.rectangle((n[0],n[1],n[0]+(self.anchoCartas*self.ppp),n[1]+(self.altoCartas*self.ppp)),fill=color)
        
        #Colocar logo
        if(self.logo!=""):
            try:
                logo = Image.open(self.logo)
                logo=logo.convert("RGBA")
                logo.thumbnail((int(self.ancho * self.ppp/3), int(self.espacioHeader * self.ppp)))
                x = ((self.imagen.width) - logo.width) // 2
                y = int(self.bordeImpresion * self.ppp)
                self.imagen.paste(logo,(x,y),logo)
            except FileNotFoundError:
                print(f"El archivo '{self.logo}' no se encuentra.")
            except PermissionError:
                print(f"Permiso denegado al intentar acceder al archivo '{self.logo}'.")
            except Exception as e:
                print(f"Error inesperado: {e}")

        

    def generarCoordenadas(self):
        """
        Genera las coordenadas en las que cada tarjeta estara.
        """

        #Definir ancho de la carta
        self.anchoCartas=(self.ancho-(2*self.bordeImpresion)-(self.espaciadoCartas*(self.elementosLado-1)))/self.elementosLado

        #definir alto
        self.altoCartas=(self.alto-(self.bordeImpresion*2)-(self.espaciadoCartas*(self.elementosLado))-self.espacioHeader)/self.elementosLado

        self.coords=[]

        y=-self.altoCartas+self.espacioHeader
        for n in range(self.elementosLado):
            x=-self.anchoCartas-self.espaciadoCartas
            y+=self.altoCartas+self.espaciadoCartas
            for j in range(self.elementosLado):
                x+=self.anchoCartas+self.espaciadoCartas
                self.coords.append((x+self.bordeImpresion,y+self.bordeImpresion))
    
    def actualizarLogo(self, path):
        """
        Actualiza la ruta del logo que se colocará.

        Args:
            path(str):Ruta de archivo.
        """
        self.logo=path
        self.actualizarMiniatura()
    
    def actualizarFondo(self, path):
        """
        Actualiza la ruta del fondo que se colocará.

        Args:
            path(str):Ruta de archivo.
        """
        self.fondo=path
        self.actualizarMiniatura()
    
    def actualizarSize(self, size):
        """
        Actualiza el tamaño de la hoja.

        Args:
            size(tuple):tupla con ancho y alto.
        """
        self.ancho=size[0]
        self.alto=size[1]
        self.actualizarMiniatura()
    
    def actualizarElementosLado(self, cant):
        """
        Actualiza el numero de elementos por lado que tendra la cudricula de cada tabla.

        Args:
            cant(int): cantidad de elementos por lado.
        """
        self.elementosLado=cant
        self.actualizarMiniatura()
    
    def actualizarBordeImpresion(self, borde):
        """
        Actualiza el tamaño del borde de impresion.

        Args:
            borde(float): Tamaño en pulgadas del borde de impresion.
        """
        self.bordeImpresion=borde
        self.actualizarMiniatura()
    
    def actualizarEspaciadoCartas(self, borde):
        """
        Actualiza el tamaño del espaciado entre cartas.

        Args:
            borde(float): Tamaño en pulgadas del espaciado entre cartas.
        """
        self.espaciadoCartas=borde
        self.actualizarMiniatura()
    
    def actualizarEspacioHeader(self, espacio):
        """
        Actualiza el tamaño del espaciado del encabezado.

        Args:
            espacio(float): Tamaño en pulgadas del espaciado del encabezado.
        """
        self.espacioHeader=espacio
        self.actualizarMiniatura()
    
    def actualizarEncabezado(self, texto):
        """
        Actualiza la cadena del encabezado.

        Args:
            texto(string): Cadena que reemplaza lo contenido en el encabezado.
        """
        self.encabezado=texto
        self.actualizarMiniatura()
    
    def actualizarLetraEncabezado(self, letra):
        """
        Actualiza la cadena que almacena el tipo de letra TrueType del encabezado.

        Args:
            letra(string): Tipo de letra del encabezado.
        """
        path=encontrar_archivo_fuente(letra)
        if(path):
            self.tipoLetra=path
        self.actualizarMiniatura()
    
    def actualizarTamanoLetraEncabezado(self, tam):
        """
        Actualiza el tamaño de la letra del encabezado.

        Args:
            tam(int): Tamaño de letra del encabezado.
        """
        self.tamanoLetra=tam
        self.actualizarMiniatura()
    
    def actualizarColorLetraEncabezado(self, color):
        """
        Actualiza el color de la letra del encabezado.

        Args:
            color(string): Color de letra del encabezado.
        """
        self.colorLetra=color
        self.actualizarMiniatura()
    
    def actualizarBordeCartas(self, borde):
        """
        Actualiza el borde entre cartas.

        Args:
            borde(float): Espaciado entre cartas.
        """
        self.espaciadoCartas=borde
    
    def actualizarCartas(self, cartas):
        """
        Actualiza las cartas.

        Args:
            cartas(list): Cartas de loteria.
        """
        self.cartas=cartas
    

    def realY(self,num):
        return (self.alto*72)-num
    
    def generarLoteria(self):
        """
        Genera la loteria con los parametros definidos.
        """
        path=self.salida+"archivo.pdf"
        ancho=self.ancho*72
        alto=self.alto*72
        self.archivo=canvas.Canvas(path,pagesize=(ancho,alto))
        self.colocarCartas()
        
    
    def colocarCartas(self):
        """
        Coloca las cartas en hojas con el formato requerido para imprimir
        """
        bordeCartas=self.bordeCartas*72
        ancho=self.anchoCartas*self.escalaCarta*72
        alto=self.altoCartas*self.escalaCarta*72

        bordeImpresion=self.bordeImpresion*72

        x=bordeImpresion-(ancho+(2*bordeCartas))
        y=self.realY(bordeImpresion)-alto

        #colocar cartas
        for n in self.cartas:
            
            x+=ancho+(bordeCartas*2)

            if(x+(bordeCartas*2)+(bordeImpresion*2))+ancho>(self.ancho*72):
                x=bordeImpresion
                y-=(alto+(bordeCartas*2))
            
            if(y-bordeImpresion)<0:
                x=bordeImpresion
                y=self.realY(bordeImpresion)-alto
                self.archivo.showPage()
            self.archivo.drawImage(n,x+bordeCartas,y-bordeCartas,ancho,alto)

            #colocae punteado
            x1=x
            x2=ancho+x+(2*bordeCartas)
            
            y1=y-(bordeCartas*2)
            y2=y1+(2*bordeCartas)+alto

            self.archivo.setDash(3,3)

            #linea inferior
            self.archivo.line(x1,y1,x2,y1)
            #linea superior
            self.archivo.line(x1,y2,x2,y2)
            #linea lateral izquierda
            self.archivo.line(x1,y1,x1,y2)
            #linea lateral derecha
            self.archivo.line(x2,y1,x2,y2)
    
    def agregarTabla(self,indices):
        ppp=72
        self.archivo.showPage()
        random.shuffle(indices)
        
        #colocar fondo
        if(self.fondo!=""):
            try:
                fondo = Image.open(self.fondo)
                fondo=ImageOps.fit(fondo,(int(self.ancho*ppp),int(self.alto*ppp)))
                path="data/Output/fondo.png"
                fondo.save(path)
                x = 0
                y = self.realY(0)
                self.archivo.drawImage(path,0,0,self.ancho*ppp,self.alto*ppp)
            except FileNotFoundError:
                print(f"El archivo '{self.logo}' no se encuentra.")
            except PermissionError:
                print(f"Permiso denegado al intentar acceder al archivo '{self.logo}'.")
            except Exception as e:
                print(f"Error inesperado: {e}")
        
         #colocar encabezado
        pdfmetrics.registerFont(TTFont("Fuente", self.tipoLetra))

        self.archivo.setFont("Fuente", self.tamanoLetra)
        rgb=hex_to_rgb(self.colorLetra)
        self.archivo.setFillColorRGB(*rgb)

        y=(self.alto*ppp)-(self.bordeImpresion*ppp)-(self.espacioHeader*ppp)+(((self.espacioHeader*ppp)-(self.tamanoLetra*0.8))/2)
        self.archivo.drawString(self.bordeImpresion*ppp, y, self.encabezado)
        
        cad="Tabla #"+str(self.contadorTabla)
        
        ancho=pdfmetrics.stringWidth(cad,"Fuente",self.tamanoLetra)
        x=(self.ancho*ppp)-ancho-(self.bordeImpresion*ppp)
        
        self.archivo.drawString(x, y, cad)

        #modificar al lienzo las coordenadas
        coordsPX=[]
        for n in self.coords:
            coordsPX.append((n[0]*ppp,(n[1]*ppp)-(self.espacioHeader*ppp)-(self.espaciadoCartas*ppp)))
        
        #colocar imagenes
        for indice,k in enumerate(coordsPX):
            self.archivo.drawImage(self.cartas[indices[indice]],k[0],k[1],self.anchoCartas*ppp,self.altoCartas*ppp)
        

        #Colocar logo
        if(self.logo!=""):
            try:
                logo = Image.open(self.logo)
                logo.thumbnail((int(self.ancho * ppp/3), int(self.espacioHeader * ppp)))
                path="data/Output/logo.png"
                logo.save(path)
                x = ((self.ancho*ppp)-(logo.width))//2
                y = (self.alto*ppp)-(self.bordeImpresion*ppp)-(self.espacioHeader*ppp)+(((self.espacioHeader*ppp)-logo.height)/2)
                self.archivo.drawImage(path,x,y,logo.width,logo.height)
            except FileNotFoundError:
                print(f"El archivo '{self.logo}' no se encuentra.")
            except PermissionError:
                print(f"Permiso denegado al intentar acceder al archivo '{self.logo}'.")
            except Exception as e:
                print(f"Error inesperado: {e}")
        #marcar borde de impresion
        """ x1=0
        x2=self.ancho*ppp
        y1=(self.alto*ppp)-(self.bordeImpresion*ppp)
        y2=y1-(self.espacioHeader*ppp)

        self.archivo.line(x1,y1,x2,y1)
        self.archivo.line(x1,y2,x2,y2) """
        
        self.contadorTabla+=1

    def sizeCartas(self):
        data=(self.anchoCartas,self.altoCartas)
        return data
    


            



if __name__=="__main__":
    prueba=lotteryTable()
    prueba.actualizarLogo(r"C:\Users\adria\Downloads\WhatsApp Image 2024-12-03 at 9.41.54 PM.jpeg")
    prueba.imagen.show()

    listaT=[]
    for n in range(20):
        listaT.append(r"C:\Users\adria\Documents\Desarrollo\Python\Lotify\data\Output\0.png")
    
    

    prueba.actualizarCartas(listaT)
    prueba.generarLoteria()
    prueba.agregarTabla([0, 1, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 15, 17, 18, 19])
    prueba.archivo.save()