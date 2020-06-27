if __name__ == '__main__':
    import os, sys

    sep = os.path.sep                                       # Obtiene separador de directorios
    dir_root = sep.join( __file__.split(sep)[0:-2] )        # Obtiene el directorio raiz del proyecto
    dir_data = os.path.join(dir_root, "Datos")              # Obtiene el directorio del modulos de datos

    sys.path.insert( 0, dir_data )                          # Inserta el directorio en la busqueda de modulos

    from funciones import *
else:
    from .funciones import *

from viajes import Viajes, Mnd

class ViajesData:
    """ Maneja la base de datos a nivel del sitio web"""
    #-------------------------------------------------------------------------------------------------------------
    def __init__ (self, dirData):
        """ Crea un objeto con los datos de todos los viajes"""
        vjs  = Viajes(dirData)

        nVjs = len(vjs.items)
        nErr = len(vjs.avisos)

        print(f"\n----->Número de viajes cargados:{ len(vjs.items) }")

        if nErr>0:            
            print("Los siguientes viajes no se pudieron cargar:\n")
            for f, ms in vjs.avisos:
                print(f"Fichero:{f}\nMensaje:{ms}\n\n")

        self.viajes = vjs

    #-------------------------------------------------------------------------------------------------------------
    def get_viaje( self, idx ):
        """ Obtiene el viaje con indice idx"""
        return self.viajes.items[idx]

    #-------------------------------------------------------------------------------------------------------------
    def viajes_count( self ):
        """ Obtiene la cantidad de viajes cargados"""
        return len(self.viajes.items)

    #-------------------------------------------------------------------------------------------------------------
    def sumary_list( self, **options ):
        """ Retorna una lista con los datos de todos los viajes """
        return self.viajes.sumario_list( **options )

    #-------------------------------------------------------------------------------------------------------------
    def product_list( self, **options ):
        """ Retorna una lista con los datos de productos """

        return self.viajes.product_list( **options )

    #-------------------------------------------------------------------------------------------------------------
    def get_vendedores(self):
        """ Obtiene la lista de vendedores registradas en el sistema """
        return self.viajes.vendedores

    #-------------------------------------------------------------------------------------------------------------
    def ventas_list( self, sfilter, vendedor, coment, pagos ):
        """ Retorna una lista con todas los datos de las ventas, segun las opcones dadas """

        ventas = self.viajes.ventas_list()

        vals = parse_filter( sfilter  )
        vendedor = False if vendedor=="Todos" else vendedor.lower()

        flist = []
        for item in ventas:
            if coment and len(item.comentario):                                     # Hay que mostrar los comentarios
                item.sItem += " | " + item.comentario + ' '                         # Lo adiciona al final del nombre

            if not check_filter( item, ("sItem", "VjAbr","idProd","idVent"), vals ):                 # Filtra por una cadena
                continue

            if vendedor and vendedor!=item.Vend.lower(): continue                   # Filtra por el nombre del vendedor

            item.Monto = item.Cant * item.Precio                                    # Calcula el monto de la venta
            item.sMnd  = Mnd.sCode( item.Mnd )                                      # Obtiene codigo de la moneda

            if pagos:                                                               # Si hay pagos y hay que mostrarlos
                if item.Pagado >= item.Monto:                                       # Si el pago esta completo
                    if item.Cant: 
                        if item.Monto: item.sItem += " ⬅ PAGADO"                   # Si quedaban items
                        else         : item.sItem += " ⬅ CONSUMO"
                    else             : item.sItem += " ⬅ DEVUELTO"                 # Si no quedabab items
                else:
                    if item.Pagado > 0:
                        item.sItem += f" | {item.Pagado} {item.sMnd} "              # Pone el valor del pago

                    item.sItem = f"<b>{item.sItem}</b>"    

            item.Total = self.viajes.Change( item.iVj, item.Monto, item.Mnd, Mnd.Cuc )     # Total en cuc

            flist.append(item)                                                      # Adiciona el item a la lista
            item.num = len(flist)                                                   # Pone el número de orden

        return flist      

    #-------------------------------------------------------------------------------------------------------------
    def pagos_list( self, sfilter, vendedor ):
        """ Retorna una lista con todas los datos de los pagos, segun las opciones dadas """

        pagos = self.viajes.pagos_list()

        vals = parse_filter( sfilter  )
        vendedor = False if vendedor=="Todos" else vendedor.lower()

        flist = []
        for item in pagos:
            if len(item.comentario):                                                # Hay que mostrar los comentarios
                item.sItem += " | " + item.comentario + ' '                         # Lo adiciona al final del nombre

            if not check_filter( item, ("sItem", "VjAbr","idProd","idVent"), vals ):       # Filtra por una cadena
                continue

            if vendedor and vendedor!=item.sVend.lower(): continue                  # Filtra por el nombre del vendedor

            item.sMnd = Mnd.sCode( item.Mnd )                                       # Obtiene codigo de la moneda
            item.Total  = self.viajes.Change( item.iVj, item.cup, item.Mnd, Mnd.Cuc )     # Total en cuc
            item.Total += item.cuc

            flist.append(item)                                                      # Adiciona el item a la lista
            item.num = len(flist)                                                   # Pone el número de orden

        return flist      

    #-------------------------------------------------------------------------------------------------------------
    def sinVender_list( self, sfilter ):
        """ Retorna una lista con todos los items que quedan sin vender """

        pagos = self.viajes.sinVender_list()

        vals = parse_filter( sfilter  )

        flist = []
        for item in pagos:
            if len(item.comentario):                                                # Hay que mostrar los comentarios
                item.sItem += " | " + item.comentario + ' '                         # Lo adiciona al final del nombre

            if not check_filter( item, ("sItem", "VjAbr","idProd"), vals ):        # Filtra por una cadena
                continue

            flist.append(item)                                                      # Adiciona el item a la lista
            item.num = len(flist)                                                   # Pone el número de orden

        return flist      

    #-------------------------------------------------------------------------------------------------------------
    def sinPagar_list( self, sfilter, vendedor ):
        """ Retorna una lista con todos los item que no se han terminado de pagar """

        pagos = self.viajes.sinPagar_list()

        vals = parse_filter( sfilter  )
        vendedor = False if vendedor=="Todos" else vendedor.lower()

        flist = []
        for item in pagos:
            if len(item.comentario):                                                # Hay que mostrar los comentarios
                item.sItem += " | " + item.comentario + ' '                         # Lo adiciona al final del nombre

            if not check_filter( item, ("sItem", "VjAbr","idProd","idVent"), vals ):       # Filtra por una cadena
                continue

            if vendedor and vendedor!=item.Vend.lower(): continue                   # Filtra por el nombre del vendedor

            #item.sMnd = Mnd.sCode( item.Mnd )                                       # Obtiene codigo de la moneda
            #item.Total  = self.viajes.Change( item.iVj, item.cup, item.Mnd, Mnd.Cuc )     # Total en cuc
            #item.Total += item.cuc

            flist.append(item)                                                      # Adiciona el item a la lista
            item.num = len(flist)                                                   # Pone el número de orden

        return flist      


#=====================================================================================================================
if __name__ == '__main__':
    dir_viajes = os.path.join(dir_data, "Viajes")

    bd = ViajesData( dir_viajes )                               # Guarda los datos de los viajes en la aplicación

    bd.ventas_list( "/Abr19/22", "Todos", True, True )
    #  bd.pagos_list( "", "" )    
    #  bd.sinVender_list( "Abriguitos de botones" )
    # bd.sinPagar_list( "_Omeprazol 40 mg", "Todos" )

    