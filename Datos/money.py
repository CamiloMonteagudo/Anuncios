               
Cuc = 0             # Peso cubano convertible
Usd = 1             # Dolar de Estados Unidos
Cup = 2             # Peso cubano o Moneda nacional
Dop = 3             # Peso de Republica Dominicana
Eur = 4             # Euros
NA  =-1             # Tipo de moneda sin definir

class Change():
    """Maneja los cambios de monedas"""

    def __init__ (self, UsdCuc, CucCup, UsdDop, EurCuc, EruDop ):
        """Inicializa las tazas de conversión más importantes"""

        # Crea una matriz de conversión entre monedas con las tazas de conversion dadas
        self.tbConv = [#         Cuc,        Usd,        Cup,    Dop,       Eur
                        [        1.0, 1.0/UsdCuc,     CucCup,    1.0, 1.0/EurCuc ],  	# Cuc
                        [     UsdCuc,        1.0,        1.0, UsdDop,        1.0 ],  	# Usd
                        [ 1.0/CucCup,        1.0,        1.0,    1.0,        1.0 ],  	# Cup
                        [        1.0, 1.0/UsdDop,        1.0,    1.0, 1.0/EruDop ],  	# Dop
                        [     EurCuc,        1.0,        1.0, EruDop,        1.0 ]  	# Eur
                      ]

        self.SetIndirect()

    def Convert(self, val, oldMoney, newMoney):
        """Convierte un tipo de moneda en otro"""
        if newMoney == oldMoney: return val

        return val * self.tbConv[oldMoney][newMoney];       # Obtiene el valor de la taza de conversion y lo multiplica por el valor       

    def SetChange( self, val, md1, md2, invert=True ):
        """Cambia la taza de cambio ente USD y CUC"""
        self.tbConv[md1][md2] = val
        if invert: self.tbConv[md2][md1] = 1.0/val
        self.SetIndirect()

    def SetIndirect( self ):
        """Actualiza todas las tazas de conversión que se calculan indirectamente"""
        cv = self.tbConv;

        cv[Cuc][Dop] = cv[Usd][Dop]/cv[Usd][Cuc]            # Cuc <-> P.Dominicano
        cv[Dop][Cuc] = 1.0 / cv[Cuc][Dop]

        cv[Usd][Cup] = cv[Usd][Cuc]*cv[Cuc][Cup]            # Dolar <-> P.Cubano
        cv[Cup][Usd] = 1.0 / cv[Usd][Cup]

        cv[Usd][Eur] = cv[Usd][Cuc]/cv[Eur][Cuc]            # Dolar <-> Euro
        cv[Eur][Usd] = 1.0 / cv[Usd][Eur]
        
        cv[Eur][Cup] = cv[Eur][Cuc]*cv[Cuc][Cup]            # Euro <-> P.Dominicano
        cv[Cup][Eur] = 1.0 / cv[Eur][Cup]

        cv[Cup][Dop] = cv[Cuc][Dop]/cv[Cuc][Cup]            # P.Cubano <-> P.Dominicano
        cv[Dop][Cup] = 1.0 / cv[Cup][Dop]


def GetValue( str_value ):
    """Pasea una cadena con un valor en un tipo de moneda Ej:'20 cuc'"""

    partes = str_value.split()      # Obtiene las dos partes separadas por espacio
    if len(partes)!=2 : raise Exception("Error de sintaxis: '" + str_value + "' no es un valor de moneda");

    try:
        val = float( partes[0] )
    except:
        raise Exception("Error de sintaxis: '" + str_value + "' no es un valor de moneda");

    mnd  = iCode( partes[1] ) 
    if mnd==NA : raise Exception("El código: '" + partes[1] + "' no es de una moneda conocida");

    return val, mnd


def iCode( sCode ):
    """Obtiene el código numerico de una moneda a partir de su codigo en letras"""
    sMnd = sCode.upper()

    if sMnd=="CUC": return Cuc
    if sMnd=="USD": return Usd
    if sMnd=="MN" : return Cup
    if sMnd=="CUP": return Cup
    if sMnd=="DOP": return Dop
    if sMnd=="EUR": return Eur

    return NA

def sCode( iCode ):
    """Obtiene el código en letras de una moneda a partir de su código númerico"""

    if iCode==Cuc: return "cuc"
    if iCode==Usd: return "usd"
    if iCode==Cup: return "mn"
    if iCode==Dop: return "dop"
    if iCode==Eur: return "eur"

    return "???"

if __name__ == '__main__':
    sImp = input("Escriba 'Valor Moneda' :")
    val, mnd = GetValue( sImp ) 

    cnv = Change( 1.10, 25.0, 53.0, 1.14, 58.0 )

    valCuc = cnv.Convert( val, mnd, Cuc )
    valCup = cnv.Convert( val, mnd, Cup )
    valUsd = cnv.Convert( val, mnd, Usd )
    valDop = cnv.Convert( val, mnd, Dop )
    valEur = cnv.Convert( val, mnd, Eur )

    print( f"Valores {valCuc:.4f} Cuc, {valCup:.4f} Cup, {valUsd:.4f} Usd, {valDop:.4f} Dop, {valEur:.4f} Euro" ) 
