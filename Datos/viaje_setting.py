from os import path
from money import Change

def LoadViajeSetting(viaje):
    """ Carga la configuración del viaje"""

    # Valores por defecto para las tazas de cambio y atributos
    UsdCuc, CucCup, UsdDop, EurCuc, EruDop = 1.10, 25.0, 53.0, 1.1423, 58.0

    viaje.Vendedores = ['Consumo']
    viaje.Title      = "Sin Título"
    viaje.TitleShort = "N/D"

    fl = open( viaje.infoFiles.CFile, encoding='utf-8' )   # Abre el fichero de configuración

    while True:
        line  = fl.readline()                       # Lee linea por linea
        if not line: break                          # Termino de leer el fichero

        if not len(line.lstrip()): continue         # Salta las lineas vacias

        line = line.rstrip('\n')                    # Quita el \n del final de la línea
        Parts = line.split(':')                     # Divide la linea en dos partes (name:valor)
        if len(Parts) != 2: 
            raise Exception( "Formato incorrecto en la línea:\n"+line )

        name, value = Parts

        if   name=="Vededores": viaje.Vendedores = value.split(',')     # Lista de vendedores
        elif name=="UsdToCuc" : UsdCuc = float(value)                   # Taza de cambio Dolar a Cuc
        elif name=="CupToCuc" : CucCup = float(value)                   # Taza de cambio Cup a Cuc
        elif name=="UsdToDop" : UsdDop = float(value)                   # Taza de cambio Dolar a Dominicano
        elif name=="EurToCuc" : EurCuc = float(value)                   # Taza de cambio Euro a Cuc
        elif name=="EurToDop" : EurDop = float(value)                   # Taza de cambio Euro a Dominicano
        elif name=="Titulo"   : viaje.Title      = value                # Nombre del viaje
        elif name=="Titulo2"  : viaje.TitleShort = value                # Nombre del viaje reducido

    viaje.MD  = Change( UsdCuc, CucCup, UsdDop, EurCuc, EruDop )        # Objeto para relizar conversiones de monedas
    viaje.Cnv = viaje.MD.Convert                                        # Función para conversion de monedas

if __name__ == '__main__':
    import money as MD
    from viaje import checkFile

    class obj: pass

    file_dir = path.join( path.dirname(__file__), "Viajes" )

    vj = obj()
    vj.infoFiles = checkFile( file_dir, "01-Viaje Panamá Noviembre 2017.xml")
    LoadViajeSetting( vj )

    UsdCuc = vj.MD.tbConv[MD.Usd][MD.Cuc]
    CucCup = vj.MD.tbConv[MD.Cuc][MD.Cup] 
    UsdDop = vj.MD.tbConv[MD.Usd][MD.Dop] 
    EurCuc = vj.MD.tbConv[MD.Eur][MD.Cuc] 
    EurDop = vj.MD.tbConv[MD.Eur][MD.Dop]

    print( f"\nDatos Leidos:\n"
           f"Vededores    : {vj.Vendedores}\n"
           f"Título       : {vj.Title}\n"
           f"Título Corto : {vj.TitleShort}\n\n"
           f"1 Dolar = {UsdCuc:5.2f} Cuc          \n"
           f"1 Cuc   = {CucCup:5.2f} P.Cubano     \n"
           f"1 Dolar = {UsdDop:5.2f} P.Dominicano \n"
           f"1 Euro  = {EurCuc:5.2f} Cuc          \n"
           f"1 Euro  = {EurDop:5.2f} P.Dominicano \n" )

    sImp = input("Escriba 'Valor Moneda' :")
    val, mnd = MD.GetValue( sImp ) 

    valCuc = vj.Cnv( val, mnd, MD.Cuc )
    valCup = vj.Cnv( val, mnd, MD.Cup )
    valUsd = vj.Cnv( val, mnd, MD.Usd )
    valDop = vj.Cnv( val, mnd, MD.Dop )
    valEur = vj.Cnv( val, mnd, MD.Eur )

    print( f"Valores {valCuc:.4f} Cuc, {valCup:.4f} Cup, {valUsd:.4f} Usd, {valDop:.4f} Dop, {valEur:.4f} Euro" ) 
