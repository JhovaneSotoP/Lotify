from PIL import Image, ImageDraw, ImageOps, ImageFont
from generalFuntions_module import encontrar_archivo_fuente

class lotteryCard():
    def __init__(self):
        """
        Inicializar clase que definira los parametros de la tarjeta de loteria.
        """
        self.contador=0
        #datos que se deberan de actualizar
        self.ancho=400
        self.alto=600
        
        self.fondo=""

        self.colorBordePrincipal="#000000"
        self.grosorBordePrincipal=5

        
        self.tipoLetra="arial.ttf"
        self.tamanoLetra=15

        self.orientacionInferior="C"
        self.espaciadoHInferior=10
        self.espaciadoVInferior=15
        self.grosorBordeInferior=2
        self.colorBordeInferior="#000000"

        self.textoInferior="DRAGON"
        self.colorTextoInferior="#FFFFFF"


        self.orientacionSuperior="R"
        self.espaciadoHSuperior=10
        self.espaciadoVSuperior=10
        self.grosorBordeSuperior=3
        self.colorBordeSuperior="#FFFFFF"

        self.textoSuperior="69"
        self.colorTextoSuperior="#000000"

        #actualizar
        self.actualizarImagenSalida()

    def actualizarImagenSalida(self):
        """
        Esta funcion simplemente vuelve a generar el mapa de pixeles con los datos de la clase.
        """
        self.imagen=Image.new("RGBA",(self.ancho,self.alto),(256,256,256))

        if self.fondo!="":
            self.colocarFondo()
        
        self.colocarTextoInferior()
        self.colocarTextoSuperior()
        self.colocarBordePrincipal()


    
    def actualizarImagen(self,path):
        """
        Actualiza el path de la imagen de fondo y llama a actualizar la imagen final.
        """
        self.fondo=path
        self.actualizarImagenSalida()
    
    
    def actualizarDimensiones(self,size):
        """
        Actualiza las dimenciones de ancho y alto y llama a actualizar la imagen final.
        """
        self.ancho=int(size[0]*200)
        self.alto=int(size[1]*200)
        self.actualizarImagenSalida()
    
    def actualizarColorBordePrincipal(self,color):
        """
        Actualiza el color del borde principal y llama a actualizar la imagen final.
        """
        self.colorBordePrincipal=color
        self.actualizarImagenSalida()
    
    def actualizarGrosorBordePrincipal(self,grosor):
        """
        Actualiza el color del borde principal y llama a actualizar la imagen final.
        """
        self.grosoeBordePrincipal=grosor
        self.actualizarImagenSalida()

    def actualizarTipoLetra(self,letra):
        """
        Actualiza el tipo de letra y llama a actualizar la imagen final.
        """
        self.tipoLetra=encontrar_archivo_fuente(letra)
        self.actualizarImagenSalida()
    
    def actualizarTamanoLetra(self,tamano):
        """
        Actualiza el tipo de letra y llama a actualizar la imagen final.
        """
        self.tamanoLetra=tamano
        self.actualizarImagenSalida()
    
    def actualizarOrientacionInferior(self,orientacion):
        """
        Actualiza la orientacion del texto inferior y llama a actualizar la imagen final.
        """
        self.orientacionInferior=orientacion
        self.actualizarImagenSalida()
    
    def actualizarEspaciadoHInferior(self,espaciado):
        """
        Actualiza el espaciado horizontal del texto inferior y llama a actualizar la imagen final.
        """
        self.espaciadoHInferior=espaciado
        self.actualizarImagenSalida()
    
    def actualizarEspaciadoVInferior(self,espaciado):
        """
        Actualiza el espaciado vertical del texto inferior y llama a actualizar la imagen final.
        """
        self.espaciadoVInferior=espaciado
        self.actualizarImagenSalida()
    
    def actualizarGrosorBordeInferior(self,grosor):
        """
        Actualiza el grosor del borde del texto inferior y llama a actualizar la imagen final.
        """
        self.grosorBordeInferior=grosor
        self.actualizarImagenSalida()
    
    def actualizarColorBordeInferior(self,color):
        """
        Actualiza el color del borde del texto inferior y llama a actualizar la imagen final.
        """
        self.colorBordeInferior=color
        self.actualizarImagenSalida()

    def actualizarColorTextoInferior(self,color):
        """
        Actualiza el color del texto inferior y llama a actualizar la imagen final.
        """
        self.colorTextoInferior=color
        self.actualizarImagenSalida()

    def actualizarTextoInferior(self,texto):
        """
        Actualiza el texto inferior y llama a actualizar la imagen final.
        """
        self.textoInferior=texto
        self.actualizarImagenSalida()

    def actualizarOrientacionSuperior(self,orientacion):
        """
        Actualiza la orientacion del texto Superior y llama a actualizar la imagen final.
        """
        self.orientacionSuperior=orientacion
        self.actualizarImagenSalida()
    
    def actualizarEspaciadoHSuperior(self,espaciado):
        """
        Actualiza el espaciado horizontal del texto Superior y llama a actualizar la imagen final.
        """
        self.espaciadoHSuperior=espaciado
        self.actualizarImagenSalida()
    
    def actualizarEspaciadoVSuperior(self,espaciado):
        """
        Actualiza el espaciado vertical del texto Superior y llama a actualizar la imagen final.
        """
        self.espaciadoVSuperior=espaciado
        self.actualizarImagenSalida()
    
    def actualizarGrosorBordeSuperior(self,grosor):
        """
        Actualiza el grosor del borde del texto Superior y llama a actualizar la imagen final.
        """
        self.grosorBordeSuperior=grosor
        self.actualizarImagenSalida()
    
    def actualizarColorBordeSuperior(self,color):
        """
        Actualiza el color del borde del texto Superior y llama a actualizar la imagen final.
        """
        self.colorBordeSuperior=color
        self.actualizarImagenSalida()

    def actualizarColorTextoSuperior(self,color):
        """
        Actualiza el color del texto Superior y llama a actualizar la imagen final.
        """
        self.colorTextoSuperior=color
        self.actualizarImagenSalida()

    def actualizarTextoSuperior(self,texto):
        """
        Actualiza el texto Superior y llama a actualizar la imagen final.
        """
        self.textoSuperior=texto
        self.actualizarImagenSalida()

    def colocarFondo(self):
        """
        Coloca la imagen de fondo en la imagen principal bajo los siguientes parametros:
        1. La imagen debe estar centrada.
        2. La imagen debe mantener su proporción.
        2. La imagen debe cubrir toda la pantalla y si hay exedentes de deben elimar.
        """
        try:
            fondo=Image.open(self.fondo)
            
            fondo=ImageOps.fit(fondo,(self.ancho,self.alto))


            self.imagen.paste(fondo,(0,0),fondo if fondo.mode=="RGBA" else None)

        except Exception as e:
            print(e)
    
    def colocarBordePrincipal(self):
        """
        Agregar el borde la carta a la imagen principal
        """
        draw=ImageDraw.Draw(self.imagen)
        draw.rectangle((0,0,self.ancho,self.alto),None,self.colorBordePrincipal,self.grosorBordePrincipal)

    def colocarTextoInferior(self):
        """
        Coloca el texto inferior respetando lo siguiente:
        1. Cadena enviada
        2. Tipo y tamaño de letra elegido
        3. Orientación
        4. Espaciado
        """
        draw=ImageDraw.Draw(self.imagen)
        font=ImageFont.truetype(self.tipoLetra,self.tamanoLetra)

        tam=font.getbbox(self.textoInferior)
        tamX=tam[2]-tam[0]
        tamY=tam[3]-tam[1]

        posY=self.alto-tamY-self.espaciadoVInferior

        if self.orientacionInferior=="L":
            posX=self.espaciadoHInferior
        elif self.orientacionInferior=="C":
            posX=(self.ancho-tamX)//2
        elif self.orientacionInferior=="R":
            posX=self.ancho-tamX-self.espaciadoHInferior
        
        grosor=self.grosorBordeInferior

        for dx in range(-grosor,grosor+1):
            for dy in range(-grosor,grosor+1):
                draw.text((posX + dx, posY + dy), self.textoInferior, font=font, fill=self.colorBordeInferior)

        draw.text((posX,posY),self.textoInferior,fill=self.colorTextoInferior,font=font)
    

    def colocarTextoSuperior(self):
        """
        Coloca el texto superior respetando lo siguiente:
        1. Cadena enviada
        2. Tipo y tamaño de letra elegido
        3. Orientación
        4. Espaciado
        """
        draw=ImageDraw.Draw(self.imagen)
        font=ImageFont.truetype(self.tipoLetra,self.tamanoLetra)

        tam=font.getbbox(self.textoSuperior)
        tamX=tam[2]-tam[0]
        tamY=tam[3]-tam[1]

        posY=self.espaciadoVSuperior

        if self.orientacionSuperior=="L":
            posX=self.espaciadoHSuperior
        elif self.orientacionSuperior=="C":
            posX=(self.ancho-tamX)//2
        elif self.orientacionSuperior=="R":
            posX=self.ancho-tamX-self.espaciadoHSuperior
        
        grosor=self.grosorBordeSuperior

        for dx in range(-grosor,grosor+1):
            for dy in range(-grosor,grosor+1):
                draw.text((posX + dx, posY + dy), self.textoSuperior, font=font, fill=self.colorBordeSuperior)

        draw.text((posX,posY),self.textoSuperior,fill=self.colorTextoSuperior,font=font)
    
    def guardar(self):
        ruta="data/Output/"+str(self.contador)+".png"
        self.imagen.save(ruta)
        self.contador+=1
        return ruta



if __name__=="__main__":
    prueba=lotteryCard()
    prueba.actualizarImagen(r"C:\Users\adria\Downloads\Designer.jpeg")
    prueba.imagen.show()
    prueba.guardar()

