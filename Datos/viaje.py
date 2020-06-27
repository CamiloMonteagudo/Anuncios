from viaje_load import LoadViajeData
from viaje_setting import LoadViajeSetting
from viaje_sumaries import UpdateSumaries, GetPagado
import money as MD
import re, os  

class Datos: pass                                   # Clase generica para guardar los datos

class Viaje:
    """ Maneja todos los datos y operaciones relacionadas con un viaje"""
    #-----------------------------------------------------------------------------------------------------------------------
    def __init__ (self, filesData):
        """ Crea un viaje con los datos almacenados en el fichero 'fileData'"""
        self.infoFiles = filesData                  # Información de los ficheros relacionados con el viaje

        LoadViajeSetting( self )                    # Carga los datos de configuración del viaje
        LoadViajeData( self )                       # Carga los datos del viaje

        self.PresupCuc        = 0.0                 # Presupuesto total en CUC
        self.GastosCUC        = 0.0                 # Total de dinero en gastos del viaje
        self.CompasCUC        = 0.0                 # Total de dinero en compras durante el viaje
        self.MontoInvers      = 0.0                 # Monto total de inversión
        self.RecupIdx         = 0.0                 # Indice de recuración de la inversión
        self.MontoPrecios     = 0.0                 # Monto total de todas las mercancias según los precios
        self.GanancPrecios    = 0.0                 # Ganacias total al los precios establecidos
        self.MontoVentas      = 0.0                 # Monto de todas las ventas
        self.GanacVentas      = 0.0                 # Ganancias de todas las ventas
        self.MontoConsumo     = 0.0                 # Monto de los items consumidos por el precio de costo
        self.GanacConsumo     = 0.0                 # Ganacia obtenida por concepto de consumo
        self.MontoConsumoRecp = 0.0                 # Monto de los items consumidos por el precio de recuperación
        self.NumChgPrecio     = 0.0                 # Número de productos que se le ha cambiado el precio al venderlo    
        self.MontoChgPrecio   = 0.0                 # Monto total de todos los cambios de precios
        self.NumDevoluc       = 0.0                 # Número total de objetos que se han devuelto
        self.MontoDevoluc     = 0.0                 # Monto total de todos los objetos devueltos
        self.NumSinPagar      = 0.0                 # Número total de objetos que estan en venta y no se han pagado
        self.MontoSinPagar    = 0.0                 # Monto de todos los objetos en venta y que no se han pagado
        self.MontoCobros      = 0.0                 # Monto de todos los pagos realizados

        self.PagosVenta = {}                        # Almacena una lista de pagos para cada venta

        UpdateSumaries( self )                      # Actualiza todos los sumarios del viaje

    #-----------------------------------------------------------------------------------------------------------------------
    def get_sumario ( self, idx_Vj, **options ):
        """ Obtiene los datos sumarios del viaje en función de las opciones dadas """

        no_consumo = options.get('no_consumo',False)
        vj = Datos()                                                                # crea un objeto vacio

        title = "<b>" + self.Title.replace(' (', '</b> (')

        vj.Title           = title                                                      # Viaje
        vj.GastosCUC       = self.GastosCUC                                             # Gastos
        vj.CompasCUC       = self.CompasCUC                                             # Compras
        vj.RecupIdx        = self.RecupIdx                                              # Indice de Gastos
        vj.MontoInvers     = self.MontoInvers                                           # Inversion
        vj.MontoConsumo    = self.MontoConsumo                                          # Consumo
        vj.MontoSinVender  = self.MontoSinVender                                        # XVender
        vj.MontoSinPagar   = self.MontoSinPagar                                         # XCobar
        vj.MontoCobros     = self.MontoCobros                                           # Cobrado

        Inversion = self.MontoInvers
        if no_consumo: Inversion -= self.MontoConsumo

        vj.Ganancia      = self.MontoCobros - Inversion                                 # Ganancia
        vj.GananciaIndex = self.MontoCobros/ Inversion if Inversion else 0              # Indice de Ganancia
        vj.PrecioIndex   = self.MontoPrecios / self.CompasCUC if self.CompasCUC else 0  # Indice de precios

        vj.Code  = self.infoFiles.Code
        vj.iVj   = idx_Vj                                                           # Pone el indice del viaje al que pertenece
        vj.VjAbr = self.TitleShort                                                  # Titulo del viaje en abreviatura 
        return vj

    #-----------------------------------------------------------------------------------------------------------------------
    def add_productos (self, lst, idx_Vj, **options):
        """ Adiciona los productos del vieje a la lista 'lst' teniendo en cuenta las opciones dadas """

        show_coment = options.get('coment',False)
        raw_gananc  = options.get('gananc_raw',False)
        item_Gananc = options.get('gananc_item',False)

        ratioRecp = 1.0 if raw_gananc else self.RecupIdx                            # Indice de recuperacion 

        for idProd in self.tbCompras.rows:                                          # Recorre todos los productos
            row = self.tbCompras.rows[idProd]                                       # Obtiene datos del producto

            pd = Datos()                                                            # crea un objeto vacio
            pd.idProd = idProd                                                      # Identificador del producto
            pd.iVj = idx_Vj                                                         # Pone el indice del viaje al que pertenece
            pd.viaje = self.TitleShort                                              # Nombre corto para el viaje

            pd.sItem  = row.item                                                     # Nombre del producto
            pd.coment = row.comentario.strip()                                       # Comentario sin los espacios
            if show_coment and len(pd.coment): 
                pd.sItem += f" | {pd.coment}"  

            pd.count  = row.count                                                   # Cantidad de items del producto
            pd.valCuc = row.valCucItem                                              # valor del producto en cuc
            pd.mond   = MD.sCode(row.moneda)                                        # Simbolo de la moneda para el precio
            pd.precio = row.precio                                                  # Precio del producto
            pd.monto  = pd.precio*pd.count                                          # Monto de la venta completa

            pd.precCuc  = self.Cnv( pd.precio, row.moneda, MD.Cuc )                 # Precio del producto en cuc
            pd.montoCuc = pd.precCuc * pd.count                                     # Monto de la venta completa (en cuc)

            pd.precRecp  = ratioRecp * pd.valCuc;                                   # Precio de recuperación del producto

            pd.rate = pd.precCuc/pd.precRecp if pd.precRecp else pd.precio          # Relación entre el precio y el precio de recuperación

            nItem     = 1 if item_Gananc else pd.count                              # Cantidad de iten a tener en cuenta
            pd.gananc = ( nItem*pd.precCuc ) - (nItem*pd.precRecp )                 # Ganancia neta

            pd.value = row.valItem if item_Gananc else row.value                    # Valor del producto

            lst.append( pd )                                                        # Adiciona el producto a la lista

            pd.num = len(lst)                                                       # Pone numero de orden del producto

    #-----------------------------------------------------------------------------------------------------------------------
    def add_ventas( self, lst, iVj ):
        """ Adiciona los productos del vieje a la lista 'lst' de ventas """

        for idVent in self.tbVentas.rows:                                           # Recorre todas las ventas
            row = self.tbVentas.rows[idVent]                                        # Obtiene datos del producto

            vt = Datos()                                                            # crea un objeto vacio
            vt.iVj    = iVj                                                         # Identificador del viaje
            vt.idVent = idVent                                                      # Identificador de la venta
            vt.idProd = row.idProd                                                  # Identificador del producto

            vt.Vend   = row.vendedor                                                # Nombre del vendedor
            vt.Cant   = row.count                                                   # Cantidad de porductos
            vt.Precio = row.precio                                                  # Precio del producto
            vt.Mnd    = row.moneda                                                  # Moneda del precio del producto

            vt.fecha = row.fecha                                                    # Fecha de la venta
            vt.comentario = row.comentario                                          # Comentarios sobre la venta

            vt.Viaje = self.Title                                                   # Titulo del viaje
            vt.VjAbr = self.TitleShort                                              # Titulo del viaje en abreviatura 

            rowCompra = self.tbCompras.rows.get( vt.idProd, False )                 # Obtiene la compra correspondiente
            vt.sItem = rowCompra.item if rowCompra else "Producto borrado"          # Nombre del producto vendido

            vt.Pagado = GetPagado( self, idVent, vt.Mnd )                           # Cantidad pagada

            lst.append( vt )                                                        # Agrega venta a la lista

    #-----------------------------------------------------------------------------------------------------------------------
    def add_pagos( self, lst, iVj ):
        """ Adiciona los pagos del vieje a la lista 'lst' de ventas """

        for idPago in self.tbPagos.rows:                                           # Recorre todos los pagos
            row = self.tbPagos.rows[idPago]                                        # Obtiene datos del pagos

            pg = Datos()                                                           # crea un objeto vacio
            pg.iVj    = iVj                                                        # Indice del viaje

            pg.IdPago = idPago                                                      # Copia todos los datos del pago
            pg.idVent = row.idVent
            pg.count  = row.count
            pg.cuc    = row.cuc
            pg.cup    = row.cup
            pg.fecha  = row.fecha
            pg.comentario = row.comentario

            pg.sVend  = "Desconicido"                                              # Toma valoler por defecto
            pg.precio = 0
            pg.Mnd    = MD.Cup
            pg.idProd = -1
            pg.sItem  = "Producto borrado" 
            pg.monto   = 0

            rowVent = self.tbVentas.rows.get( pg.idVent, False )                    # Obtiene datos de la venta asociada
            if rowVent :
                pg.sVend  = rowVent.vendedor                    
                pg.Mnd    = rowVent.moneda 
                pg.precio = rowVent.precio
                pg.nVent  = rowVent.count 

                pg.idProd = rowVent.idProd
                rowProd   = self.tbCompras.rows.get( pg.idProd, False )             # Obtiene nombre del producto
                if rowProd: pg.sItem = rowProd.item

            pg.VjAbr = self.TitleShort                                              # Titulo del viaje en abreviatura 

            lst.append( pg )                                                        # Agrega el pago a la lista


    #-----------------------------------------------------------------------------------------------------------------------
    def add_sinPagar( self, lst, iVj ):
        """ Adiciona los item sin pagar del viaje a la lista 'lst' """

        for idVent in self.tbVentas.rows:                                           # Recorre todas las ventas
            row = self.tbVentas.rows[idVent]                                        # Obtiene datos de la venta

            vt = Datos()                                                            # Crea un objeto vacio
            vt.pagado = GetPagado( self, idVent, row.moneda )                       # Cantidad pagada

            vt.precio = row.precio                                                  # Precio del producto
            vt.count  = row.count                                                   # Cantidad de porductos
            vt.monto  = vt.count * vt.precio
            if vt.pagado + 0.001 >= vt.monto: continue                              # Se suma 0.001 para compensar error de redondeo

            vt.iVj    = iVj                                                         # Identificador del viaje
            vt.idVent = idVent                                                      # Identificador de la venta
            vt.idProd = row.idProd                                                  # Identificador del producto

            vt.Vend = row.vendedor                                                  # Nombre del vendedor
            vt.Mnd  = row.moneda                                                    # Moneda del precio del producto
            vt.sMnd = MD.sCode(vt.Mnd)

            vt.fecha = row.fecha                                                    # Fecha de la venta
            vt.comentario = row.comentario                                          # Comentarios sobre la venta

            vt.VjAbr = self.TitleShort                                              # Titulo del viaje en abreviatura 

            rowCompra = self.tbCompras.rows.get( vt.idProd, False )                 # Obtiene la compra correspondiente
            vt.sItem = rowCompra.item if rowCompra else "Producto borrado"          # Nombre del producto vendido

            vt.nPagos = vt.pagado/vt.precio if vt.precio else 0
            vt.resto  = vt.count - vt.nPagos
            vt.xPagar = vt.resto * vt.precio
            vt.xPagarCuc = self.Cnv( vt.xPagar, vt.Mnd, MD.Cuc )

            lst.append( vt )                                                        # Agrega venta a la lista

    #-----------------------------------------------------------------------------------------------------------------------
    def CalculateCounts( self  ):
        """ Calcula las cantidades disponible de cada tipo de item """
        counts = {}

        for idVent in self.tbVentas.rows:                                           # Recorre todas las ventas
            row = self.tbVentas.rows[idVent]                                        # Obtiene datos de la venta

            idProd = row.idProd
            Cant   = row.count

            n = counts.get( idProd, False )
            if n: Cant += n
                
            counts[idProd] = Cant

        return counts

    #-----------------------------------------------------------------------------------------------------------------------
    def add_sinVender (self, lst, iVj):
        """ Adiciona los productos del vieje a la lista 'lst' teniendo en cuenta las opciones dadas """

        counts = self.CalculateCounts()

        ratioRecp = self.MontoInvers / self.CompasCUC if self.CompasCUC else 0
        ratioGanc = 1.5 * ratioRecp

        for idProd in self.tbCompras.rows:                                          # Recorre todos los productos
            row = self.tbCompras.rows[idProd]                                       # Obtiene datos del producto

            pd = Datos()                                                            # crea un objeto vacio

            pd.count  = row.count                                                   # Cantidad de items del producto
            pd.resto = pd.count - counts.get( idProd, 0 )
            if pd.resto <=0 : continue

            pd.idProd = idProd                                                      # Identificador del producto
            pd.iVj    = iVj                                                         # Pone el indice del viaje al que pertenece
            pd.VjAbr  = self.TitleShort                                             # Titulo del viaje en abreviatura 

            pd.sItem = row.item                                                     # Nombre del producto

            pd.mond   = row.moneda                                                  # Simbolo de la moneda para el precio
            pd.precio = row.precio                                                  # Precio del producto
            pd.sMnd   = MD.sCode(pd.mond)

            pd.precCosto  = self.Cnv( row.valCucItem, MD.Cuc, pd.mond )
            pd.precRecp   = ratioRecp * pd.precCosto
            pd.precGanc   = ratioGanc * pd.precCosto
            pd.monto      = pd.resto * pd.precio
            pd.montoCuc   = self.Cnv( pd.monto, pd.mond, MD.Cuc )
            pd.value      = pd.resto * row.valCucItem
            pd.comentario = row.comentario

            lst.append( pd )                                                        # Adiciona el producto a la lista

#===========================================================================================================================
def checkFile( dirData, name ):
    """ Procesa el nombre del fichero y decide los ficheros a cargar"""
    fName, fExt = os.path.splitext(name)
    if fExt.lower() != '.xml': return False                     # Si la extensión no es xml lo ignora

    ini = name.find("-")                                        # Busca un código inicial en el nombre del fichero
    if ini<0 or ini>6: return False                             # Si ni encuentre el código lo ignora

    obj = Datos()    
    obj.Code = name[:ini]                                       # Obtiene el código
    obj.DFile = os.path.join( dirData, name            )        # Obtiene el fichero de los datos
    obj.CFile = os.path.join( dirData, fName + ".ini"  )        # Obtiene el fichero de configuración

    return obj

#===========================================================================================================================
if __name__ == '__main__':
    def PrintChanges( tbCnv ):
        Cuc, Usd, Cup, Dop, Eur = tbCnv[MD.Cuc], tbCnv[MD.Usd], tbCnv[MD.Cup], tbCnv[MD.Dop], tbCnv[MD.Eur]  
        print( f"        Cuc    Usd    Cup    Dop    Eur\n"
               f"   -------------------------------------\n" 
               f"Cuc|{Cuc[MD.Cuc]:7.2f}{Cuc[MD.Usd]:7.2f}{Cuc[MD.Cup]:7.2f}{Cuc[MD.Dop]:7.2f}{Cuc[MD.Eur]:7.2f}\n"
               f"Usd|{Usd[MD.Cuc]:7.2f}{Usd[MD.Usd]:7.2f}{Usd[MD.Cup]:7.2f}{Usd[MD.Dop]:7.2f}{Usd[MD.Eur]:7.2f}\n"
               f"Cup|{Cup[MD.Cuc]:7.2f}{Cup[MD.Usd]:7.2f}{Cup[MD.Cup]:7.2f}{Cup[MD.Dop]:7.2f}{Cup[MD.Eur]:7.2f}\n"
               f"Dop|{Dop[MD.Cuc]:7.2f}{Dop[MD.Usd]:7.2f}{Dop[MD.Cup]:7.2f}{Dop[MD.Dop]:7.2f}{Dop[MD.Eur]:7.2f}\n"
               f"Eur|{Eur[MD.Cuc]:7.2f}{Eur[MD.Usd]:7.2f}{Eur[MD.Cup]:7.2f}{Eur[MD.Dop]:7.2f}{Eur[MD.Eur]:7.2f}\n\n" )

    from os import path

    file_dir = path.join( path.dirname(__file__), "Viajes" )
    infoFiles = checkFile( file_dir, "01-Viaje Panamá Noviembre 2017.xml")

    vj = Viaje(infoFiles)

    cnv = vj.MD.tbConv
    UsdCuc,CucCup,UsdDop = cnv[MD.Usd][MD.Cuc], cnv[MD.Cuc][MD.Cup], cnv[MD.Usd][MD.Dop] 
    EurCuc,EurDop        = cnv[MD.Eur][MD.Cuc], cnv[MD.Eur][MD.Dop]

    nPres = vj.tbPresupesto.NRows()
    nGast = vj.tbGastos.NRows()
    nComp = vj.tbCompras.NRows()
    nVent = vj.tbVentas.NRows()
    nPago = vj.tbPagos.NRows()

    print( f"\nDATOS CARGADOS:\n"
           f"Vededores    : {vj.Vendedores}\n"
           f"Título       : {vj.Title}\n"
           f"Título Corto : {vj.TitleShort}\n\n"

           f"1 Dolar = {UsdCuc:5.2f} Cuc  1 Cuc  = {CucCup:5.2f} P.Cubano     1 Dolar = {UsdDop:5.2f} P.Dominicano \n"
           f"1 Euro  = {EurCuc:5.2f} Cuc  1 Euro = {EurDop:5.2f} P.Dominicano \n\n"
           
           f"Presupuestos: {nPres:<3} regístros   Gastos: {nGast:<3} regístros   Compras: {nComp:<3} regístros\n"
           f"Ventas'     : {nVent:<3} regístros   Pagos : {nPago:<3} regístros\n" ) 

    compras = []
    vj.add_productos( compras, 10 )

    print( f"{'':2} {'':2} {'Viaje':5} {'Producto':34} {'Num':3} {'Costo':>9} {'C. Cuc':6} {'Precio':>10} {'Monto':>11} {'M. Cuc':>7} {'Rate':>6} {'Ganancia':5}" )
    for pd in compras:
      print( f"{pd.num:2} {pd.idProd:2} {pd.viaje:5} {pd.sItem:34} {pd.count:3} {pd.value:>9} {pd.valCuc:6.2f} {pd.precio:6.2f} {pd.mond:3} {pd.monto:7.2f} {pd.mond:3} {pd.montoCuc:7.2f} {pd.rate:6.2f} {pd.gananc:8.2f}" )

    print("\n")  

    #PrintChanges( cnv )
