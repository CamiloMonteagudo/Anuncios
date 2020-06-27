import os
from viaje import Viaje, Datos, checkFile
import money as Mnd

class Viajes:
    """ Maneja todos los viajes disponibles en el directorio de viajes"""
    #-------------------------------------------------------------------------------------------------------------
    def __init__ (self, dirData):
        """ Crea un objeto con los datos de todos los viajes"""

        self.items = []                                 # Lista con los datos de todos los viajes
        self.avisos = []                                # Avisos de incidencias durate la carga de los viajes
        self.vendedores = []                            # Lista de vendedores en todos los viajes
        self.dirData = dirData
        
        setVends = set()                                # Conjunto de vendedores ya adicionados a la lista                          
        for f in os.listdir(dirData):
            fInfo = checkFile( dirData, f)
            if not fInfo: continue
                
            try:
                vj = Viaje( fInfo )
                self.items.append(vj)
                self.getVendedores( vj.Vendedores, setVends)
            except Exception as exc:
                self.avisos.append( fInfo['fData'], exc.args )  

    #-------------------------------------------------------------------------------------------------------------
    def getVendedores(self, vendedores, setVends):
        """ Adiciona todos los vendedores a la lista sin que se repitan"""
        for vend in vendedores:
            if vend in setVends: continue
                
            self.vendedores.append(vend)
            setVends.add(vend)

    #-------------------------------------------------------------------------------------------------------------
    def Change(self, iVj, value, fromMnd, toMnd ):
        """ Obtiene le codigo en letras de la mondeda de indice iCode  """
        return self.items[iVj].Cnv( value, fromMnd, toMnd )

    #-------------------------------------------------------------------------------------------------------------
    def sumario_list(self, **options):
        """ Obtiene una lista con el sumario de todos los viajes """
        sumarios = []
        
        for iVj, vj in enumerate(self.items):
            sum = vj.get_sumario( iVj, **options )          # Obtiene los datos sumarios del viaje

            sumarios.append( sum )                          # Adiciona el producto a la lista

            sum.num = len(sumarios)                         # Pone numero de orden del producto

        return sumarios

    #-------------------------------------------------------------------------------------------------------------
    def product_list(self, **options):
        """ Obtiene una lista con todos los items de todos los viajes """
        prods = []
        
        for iVj, vj in enumerate(self.items):
            vj.add_productos( prods, iVj, **options)

        return prods

    #-------------------------------------------------------------------------------------------------------------
    def ventas_list(self):
        """ Obtiene una lista con todos los items de todos los viajes """
        ventas = []

        for iVj, vj in enumerate(self.items):
            vj.add_ventas( ventas, iVj )

        return ventas

    #-------------------------------------------------------------------------------------------------------------
    def pagos_list(self):
        """ Obtiene una lista con todos los pagos de todos los viajes """
        pagos = []

        for iVj, vj in enumerate(self.items):
            vj.add_pagos( pagos, iVj )

        return pagos

    #-------------------------------------------------------------------------------------------------------------
    def sinVender_list(self):
        """ Obtiene obtiene todos los items por vender de todos los viajes """
        ventas = []

        for iVj, vj in enumerate(self.items):
            vj.add_sinVender( ventas, iVj )

        return ventas

    #-------------------------------------------------------------------------------------------------------------
    def sinPagar_list(self):
        """ Obtiene obtiene todas las ventas que no se han pagado completamente de todos los viajes """
        pagos = []

        for iVj, vj in enumerate(self.items):
            vj.add_sinPagar( pagos, iVj )

        return pagos

    #-------------------------------------------------------------------------------------------------------------
    def find_prod(self, iVj, idProd ):
        """ Busca un producto en el viaje dado y retorna sus datos """
        vj = self.items[iVj]
        pd = vj.tbCompras.rows[idProd]

        pd.monto  = pd.precio*pd.count                                          # Monto de la venta completa
        return pd

    #-------------------------------------------------------------------------------------------------------------
    def find_venta(self, iVj, idVent ):
        """ Busca una venta en el viaje dado y retorna sus datos """
        vj = self.items[iVj]
        vt = vj.tbVentas.rows[idVent]

        monto = vt.precio * vt.count                                           # Monto de la venta completa

        vt.monto  = vj.Cnv( monto, vt.moneda, Mnd.Cuc )
        return vt

#=====================================================================================================================
if __name__ == '__main__':
    dir = os.path.dirname(__file__)
    dirData = os.path.join(dir, "Viajes")

    vjs  = Viajes(dirData)
    nVjs = len(vjs.items)
    nErr = len(vjs.avisos)

    print(f"\nNúmero de viajes cargados:{ len(vjs.items) }")
    if nVjs>0: print(f"VENDEDORES:\n{vjs.vendedores}")
    print("\n")

    if nErr>0:            
        print("Los siguientes viajes no se pudieron cargar:\n")
        for f, ms in vjs.avisos:
            print(f"Fichero:{f}\nMensaje:{ms}\n\n")

                
    #lstSum = sorted( vjs.Sumary_list(""), key=lambda x:x[11] )
    #for item in lstSum:
    #    print( f"{item[11]:.2f} {item[0]:3} {item[1]}")
        
    

 