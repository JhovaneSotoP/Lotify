from PIL import Image, ImageDraw, ImageOps, ImageFont

class lotteryCard():
    def __init__(self):
        """
        Inicializar clase que definira los parametros de la tarjeta de loteria.
        """

        #datos que se deberan de actualizar
        self.ancho=200
        self.alto=300
        
        self.fondo=""

        self.colorBordePrincipal="#000000"
        self.grosorBordePrincipal=5

        
        self.tipoLetra="arial.ttf"
        self.tamanoLetra=15

        self.orientacionInferior="L"
        self.espaciadoHInferior=10
        self.espaciadoVInferior=10

        self.textoInferior="Jhovane"

        #actualizar
        self.actualizarImagenSalida()

    def actualizarImagenSalida(self):
        """
        Esta funcion simplemente vuelve a generar el mapa de pixeles con los datos de la clase.
        """
        self.imagen=Image.new("RGBA",(self.ancho,self.alto),(256,256,256))

        if self.fondo!="":
            self.colocarFondo()
        
        self.colocarBordePrincipal()
        self.colocarTextoInferior()

    
    def actualizarImagen(self,path):
        """
        Actualiza el path de la imagen de fondo y llama a actualizar la imagen final.
        """
        self.fondo=path
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


        if self.orientacionInferior=="L":
            pass
        elif self.orientacionInferior=="C":
            pass
        elif self.orientacionInferior=="R":
            pass


        draw.text((0,0),self.textoInferior,fill="Black",font=font)

if __name__=="__main__":
    prueba=lotteryCard()
    prueba.actualizarImagen(r"C:\Users\adria\OneDrive\Escritorio\WhatsApp Image 2024-09-10 at 6.35.09 PM.jpeg")
    prueba.imagen.show()
