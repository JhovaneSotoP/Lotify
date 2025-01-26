import math
import random

from matplotlib import font_manager

def indextablas(cantTablas,NoCartas,cartasTabla):
    maxTablas=math.comb(NoCartas,cartasTabla)
    salida=[]

    for n in range(cantTablas):
        tabla=random.sample(range(NoCartas),cartasTabla)
        tabla.sort()
        while tabla in salida:
            tabla=random.sample(range(NoCartas),cartasTabla)
            tabla.sort()
        salida.append(tabla)
        print(tabla)
    return salida


def encontrar_archivo_fuente(nombre_fuente):
    lista=[]
    for fuente in font_manager.findSystemFonts(fontpaths=None, fontext='ttf'):
        if font_manager.FontProperties(fname=fuente).get_name() == nombre_fuente:
            lista.append(fuente)
    lista.sort(key=len)
    if lista==[]:
        return encontrar_archivo_fuente("Arial")
    else:
        return lista[0]

def hex_to_rgb(hex_color):
    """Convierte un color hexadecimal (#RRGGBB) a valores RGB normalizados (0.0 - 1.0)."""
    hex_color = hex_color.lstrip('#')  # Eliminar el prefijo #
    return tuple(int(hex_color[i:i + 2], 16) / 255.0 for i in (0, 2, 4))



    

if __name__=="__main__":
    
    #indextablas(20,20,16)
    nombre_fuente = "Arial"
    archivo_ttf = encontrar_archivo_fuente(nombre_fuente)
    if archivo_ttf:
        print(f"Archivo TTF encontrado: {archivo_ttf}")
    else:
        print("No se encontró el archivo TTF.")
    
    print(hex_to_rgb("#FA00FF"))