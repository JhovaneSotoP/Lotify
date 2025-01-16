from PIL import Image

class lotteryTable():
    def __init__(self):
        self.ancho=8.5
        self.alto=11
        self.ppp=300

        self.actualizarMiniatura()
    def actualizarMiniatura(self):
        self.imagen=Image.new("RGBA",(int(self.ancho*self.ppp),int(self.alto*self.ppp)),"#FFFFFF")

if __name__=="__main__":
    prueba=lotteryTable()
    prueba.imagen.show()