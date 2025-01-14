from cardModule import lotteryCard


carta=lotteryCard()

def pruebaCarta():
    carta=lotteryCard()

    #Comprobar tamaño
    assert carta.imagen.width==200
    assert carta.imagen.height==300 

pruebaCarta()