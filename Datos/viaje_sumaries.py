import money as MD
import re

#------------------------------------------------------------------------------------------------------------------------------------
def UpdateSumaries(vj):
    """Actualiza todos los sumarios del viaje"""
    SumaryPresupuesto(vj)
    SumaryGastos(vj)
    SumaryCompras(vj)
    SumaryPagos(vj)
    SumaryVentas(vj)
#------------------------------------------------------------------------------------------------------------------------------------
def SumaryPresupuesto(vj):
    """Obtiene los datos generales sobre el presupuesto"""

    sumaUSD = sumaCUC = totalUSD = totalCUC = 0.0

    for row in vj.tbPresupesto.rows.values():
        cambio = row.cambio
        moneda = row.moneda
        value  = row.value

        if moneda == MD.Usd:
            sumaUSD  += value
            totalUSD += value
            totalCUC += ( value * cambio )
        else:
            sumaCUC  += value
            totalCUC += value
            totalUSD += ( value / cambio )

    vj.PresupCuc = totalCUC
    if totalUSD>0 and totalCUC>0: 
        vj.MD.SetChange( totalCUC/totalUSD, MD.Usd, MD.Cuc ) 
#------------------------------------------------------------------------------------------------------------------------------------
def UpdateRecupIdx(vj):
    """Actualiza el indice de recuperación según los datos actuales"""
    vj.MontoInvers  = vj.GastosCUC + vj.CompasCUC

    if vj.CompasCUC>0: vj.RecupIdx = vj.MontoInvers/vj.CompasCUC
    else:              vj.RecupIdx = vj.MontoInvers
#------------------------------------------------------------------------------------------------------------------------------------
def SumaryGastos(vj):
    """Obtiene los datos generales sobre los gastos"""

    vj.GastosCUC = 0.0
    for row in vj.tbGastos.rows.values():
        vj.GastosCUC += row.valCuc

    UpdateRecupIdx(vj)
#------------------------------------------------------------------------------------------------------------------------------------
def SumaryCompras(vj):
    """Obtiene los datos generales sobre las compras"""

    vj.CompasCUC = vj.MontoPrecios = vj.GanancPrecios = 0.0

    for row in vj.tbCompras.rows.values():
        prec = vj.MD.Convert( row.precio, row.moneda, MD.Cuc )              # Siempre lleva el precio a CUC

        vj.MontoPrecios += ( prec * row.count )
        vj.CompasCUC    += row.valCUC

    UpdateRecupIdx(vj)
    vj.GanancPrecios = vj.MontoPrecios - vj.MontoInvers

#------------------------------------------------------------------------------------------------------------------------------------
def SumaryPagos(vj):
    """Obtiene los datos generales sobre los pagos"""

    vj.PagosVenta = {}
    vj.MontoCobros = 0.0                                                    # Sumatoria de todos los pagos reallizados

    for idPago, row in vj.tbPagos.rows.items():                             # Recorre todos los pagos
        vj.MontoCobros += row.cuc                                           # Acumula los pago en cuc
        vj.MontoCobros +=vj.Cnv( row.cup, MD.Cup, MD.Cuc )                  # Acumula los pago en cup (convertido a cuc)

        idVent = row.idVent                                                 # Id de la venta a la que pertenece el pago
        if idVent not in vj.PagosVenta:                                     # Si no hay pago para la venta 
            vj.PagosVenta[idVent] = []                                      # Crea una lista vacia

        vj.PagosVenta[idVent].append(idPago)                                # Agrega el pago a la venta

#------------------------------------------------------------------------------------------------------------------------------------
reNDevuelto = re.compile(" Devolvio ([0-9]+)\}")                            # Parsea # de items devueltos 

def SumaryVentas(vj):
    """Obtiene los datos generales sobre las compras"""

    vj.MontoVentas  = vj.GanacVentas = 0.0                                  # Inicializa sumarios de ventas
    vj.MontoConsumo = vj.GanacConsumo = vj.MontoConsumoRecp = 0.0           # Inicializa sumarios de items de consumo
    vj.NumChgPrecio = vj.MontoChgPrecio = 0.0                               # Inicializa sumarios de cambios de precio
    vj.NumDevoluc   = vj.MontoDevoluc = 0.0                                 # Inicializa sumarios de devoluciones
    vj.NumSinPagar  = vj.MontoSinPagar = 0.0                                # Inicializa sumarios de Items sin pagar 
    vj.NumSinVender = vj.MontoSinVender = 0.0                               # Inicializa sumarios de Items sin vender  

    GroupVentas = {}                                                        # Dicionario para contar las ventas por preductos

    for idVenta, row in vj.tbVentas.rows.items():
        Cant   = row.count
        idProd = row.idProd

        if idProd in GroupVentas: GroupVentas[idProd] += Cant               # Acumula la cantidad de ventas por producto
        else:                     GroupVentas[idProd]  = Cant

        rowProd = vj.tbCompras.rows.get(idProd)                             # Busca datos de item asociado a la venta
        if not rowProd: continue

        montoProd = vj.Cnv( Cant*rowProd.precio, rowProd.moneda, MD.Cuc )   # Monto al precio del item en CUC

        if row.vendedor == vj.Vendedores[0]:                                # Item para consumo
            costo    = Cant * rowProd.valCucItem
            costoRcp = costo * vj.RecupIdx

            vj.MontoConsumo     += costo                                    # Acumula costos de compra
            vj.MontoConsumoRecp += costoRcp                                 # Acumula costos de recuperación
            vj.GanacConsumo     += ( montoProd-costoRcp )
            continue                                                        # No hace más analisis para esa venta

        precioVenta = vj.Cnv( row.precio, row.moneda, MD.Cuc)               # Lleva precio de la venta a CUC
        montoVenta  = Cant * precioVenta                                    # Calcula el monto de la venta en CUC

        vj.MontoVentas += montoVenta                                        # Acumula todos los montos de las ventas

        if montoProd != montoVenta:                                         # Cambio el precio del producto en la venta
            vj.NumChgPrecio += Cant                                         # Acumula # de items que cambian de precio
            vj.MontoChgPrecio += (montoVenta-montoProd) * Cant              # Acumula las diferencias de precio

        if len(row.comentario):                                             # Si hay comentarios
            matches = reNDevuelto.findall( row.comentario )                 # Busca la cantidad de items devueltos
            for match in matches:                                           # Para cada devolución
                Num = int(match)                                            # Convierte a entero la cantidad de devoluciones

                vj.NumDevoluc   += Num                                      # Acumula de cantidad de devoluciones
                vj.MontoDevoluc += ( Num*precioVenta )                      # Acumula el precio de las devoluciones

        Pago = GetPagado( vj, idVenta, MD.Cuc )                             # Determina la cantidad de la venta pagada
        SinPagar = montoVenta - Pago                                        # Calcula lo que queda sin pagar

        if precioVenta!=0:                                                  # Si ya hay un precio establecido
            vj.NumSinPagar += SinPagar/precioVenta                          # Acumula el # de items sin pagar

        vj.MontoSinPagar += SinPagar                                        # Acumula el monto sin pagar

    vj.GanacVentas = vj.MontoVentas - vj.MontoInvers                        # Calcula las ganancias totales por ventas

    for idProd, row in vj.tbCompras.rows.items():                           # Recorre todos los productos
        Resto = row.count                                                   # Inicializa productos que quedan (todos)
        if idProd in GroupVentas: Resto -= GroupVentas[idProd]              # Quita la cantidad de productos vendidos

        if Resto <= 0: continue                                             # Si todos estan vendidos no hace mas nada

        Precio = vj.Cnv( row.precio, row.moneda, MD.Cuc )                   # Lleva el precio del producto a cuc

        vj.NumSinVender   += Resto                                          # Acumula la cantidad de productos sin vender
        vj.MontoSinVender += ( Resto*Precio )                               # Acumula el precio de los productos sin vender

#------------------------------------------------------------------------------------------------------------------------------------
def GetPagado(vj, idVenta, Mnd):
    """Obtiene todos los pagos realizados para la venta dada, los retorna en la moneda 'Mnd'"""

    pagado = 0.0
    for idPago in vj.PagosVenta.get(idVenta,[]):                            # Recorre todos los pagos para la venta
        rowPago = vj.tbPagos.rows[idPago]

        pagado += vj.Cnv( rowPago.cuc, MD.Cuc, Mnd )
        pagado += vj.Cnv( rowPago.cup, MD.Cup, Mnd )
    return pagado
    
#============================================================================================
if __name__ == '__main__':
    from viaje_load import LoadViajeData
    from viaje_setting import LoadViajeSetting
    from viaje import checkFile
    from os import path

    file_dir = path.join( path.dirname(__file__), "Viajes" )

    class obj: pass
    vj = obj()
    vj.infoFiles = checkFile( file_dir, "01-Viaje Panamá Noviembre 2017.xml")

    LoadViajeSetting( vj )                              # Carga los paramentros del viaje
    LoadViajeData( vj )                                 # Carga los datos del viaje

    vj.GastosCUC = vj.CompasCUC = 0.0
    UpdateSumaries( vj )                                # Analiza los datos y crea sumarios

    Sobrante = vj.PresupCuc-vj.MontoInvers

    IdxGastos = vj.GastosCUC/vj.CompasCUC      if vj.GastosCUC   else 0
    IdxPrec   = vj.MontoPrecios/vj.CompasCUC   if vj.CompasCUC   else 0
    IdxGananc = vj.MontoPrecios/vj.MontoInvers if vj.MontoInvers else 0

    ConsumoMonto  = vj.MontoConsumoRecp + vj.GanacConsumo
    GananciaVenta = vj.GanacVentas + vj.GanacConsumo

    GanancPagada     = vj.MontoCobros - vj.MontoInvers
    GanancSinConsumo = vj.MontoCobros - (vj.MontoInvers - vj.MontoConsumo)
    GanancConConsumo = GanancPagada + vj.GanacConsumo

    print( f"\n" 
        f"INVERSIÓN: Presupuesto:{vj.PresupCuc:8.2f} CUC   Utilizado:{vj.MontoInvers:8.2f} CUC    Sobrante:{Sobrante :6.2f} \n"
        f"                Gastos:{vj.GastosCUC:8.2f} CUC     Compras:{vj.CompasCUC  :8.2f} CUC  Idx Gastos:{IdxGastos:6.2f} \n\n"

        f"PRECIOS  : Monto:{vj.MontoPrecios:8.2f} CUC   Ganancia:{vj.GanancPrecios:8.2f} CUC   Idx Ganancia: {IdxGananc          :<6.2f}  Idx Precio: {IdxPrec     :<6.2f} \n"
        f"CONSUMO  : Costo:{vj.MontoConsumo:8.2f} CUC   Ganancia:{vj.GanacConsumo :8.2f} CUC   Costo Recup.: {vj.MontoConsumoRecp:<6.2f}       Monto: {ConsumoMonto:<6.2f} \n\n"

        f"VENTAS   : Monto:{vj.MontoVentas :8.2f} CUC   Ganancia:{vj.GanacVentas  :8.2f} CUC   Items x Vender:{int(vj.NumSinVender):3} => {vj.MontoSinVender:6.2f} CUC \n"
        f"                 {' '               :8}     Gan. Total:{GananciaVenta   :8.2f} CUC   Cambio/Precios:{int(vj.NumChgPrecio):3} => {vj.MontoChgPrecio:6.2f} CUC \n"
        f"                 {' '               :8}                {' '                :8}       # Devoluciones:{int(vj.NumDevoluc)  :3} => {vj.MontoDevoluc  :6.2f} CUC \n\n"

        f"COBROS   : Ganancia:{GanancPagada  :8.2f} CUC  Sin consumo:{GanancSinConsumo:8.2f}    Items x Cobar: {vj.NumSinPagar:.1f} => {vj.MontoSinPagar:<6.2f} CUC  \n"
        f"                    {' '              :8}      Con consumo:{GanancConConsumo:8.2f} \n"
        f"            Cobrado:{vj.MontoCobros:8.2f} CUC              {' '                :8} \n"
        )
