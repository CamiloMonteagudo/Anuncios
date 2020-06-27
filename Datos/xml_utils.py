import re
reTagName  = re.compile("^ *<(\?|/)?(\w+)")                 # Extrae el nombre de un tag definido en una cadena 
reTagValue = re.compile("^.*?>(.*?)<")                      # Extrae el valor del Tag definido en una cadena

def GetTagName( line ):
    """Obtine el nombre del tag en una linea que contiene un tag XML"""
    mth = reTagName.match(line)  
    if not mth: raise Exception("No es un Tag XML ->" + line)

    mrk,name = mth.groups()
    return name, (mrk=="/")

def GetTagValue( line ):
    """Obtine el valor de un tag XML definido en una linea de texto Ej:  <tagname>VALOR</tagname>"""
    mth = reTagValue.match(line)  
    if not mth: return ""                                   # No pudo extraer el texto (retorna cadena vacia)

    return mth.groups(1)[0]

if __name__ == '__main__':
    line = input("Escriba un Tag Xml:")

    name, end = GetTagName( line ) 
    value = GetTagValue( line ) 

    print( f"Nombre: '{name}'\nTag Final: {end}\nValor: {value}" ) 
