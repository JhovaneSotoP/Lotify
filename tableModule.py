from PIL import Image,ImageDraw, ImageOps, ImageFont
import reportlab
import random

class lotteryTable():
    def __init__(self):
        """
        Inicializa los parametros de las tablas de la loteria
        """
        self.ancho=8.5
        self.alto=11
        self.ppp=300

        self.elementosLado=4
        self.bordeImpresion=0.25
        self.espaciadoCartas=0.15

        self.espacioHeader=0.3


        self.anchoCartas=0
        self.altoCartas=0

        self.logo=""
        self.fondo=""
        self.encabezado="Loteria"

        self.tipoLetra="arial.ttf"
        self.tamanoLetra=90
        self.colorLetra="#000000"

        self.contadorTabla=1

        self.actualizarMiniatura()

    def actualizarMiniatura(self):
        """
        Actualiza la miniatura de la tabla.
        """
        #Crear imagen
        self.imagen=Image.new("RGBA",(int(self.ancho*self.ppp),int(self.alto*self.ppp)),self.colorLetra)

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
            



if __name__=="__main__":
    prueba=lotteryTable()
    prueba.actualizarLogo(r"C:\Users\adria\OneDrive\Imágenes\Capturas de pantalla\Captura de pantalla 2024-12-07 185929.png")
    prueba.actualizarFondo(r"C:\Users\adria\OneDrive\Imágenes\Capturas de pantalla\Captura de pantalla 2024-12-07 194413.png")
    prueba.imagen.show()