from xml_utils import *
from table import *
from datetime import datetime, date

def LoadViajeData(viaje):
    """ Carga todos los datos del viaje"""

    viaje.tbPresupesto = Table()
    viaje.tbGastos     = Table()
    viaje.tbCompras    = Table()
    viaje.tbVentas     = Table()
    viaje.tbPagos      = Table()

    fl = open( viaje.infoFiles.DFile, encoding='utf-8'  )

    while True:
        line  = fl.readline()                  # Lee una línea
        if not line: break 

        name, end = GetTagName( line ) 
        if name=="xml" or name=="DataBase": continue 

        Datos = GetRecord( fl, name)   
        
        if   name == "Presupuesto" : AddPresupesto( viaje.tbPresupesto, Datos ) 
        elif name == "Gastos"      : AddGastos( viaje.tbGastos, Datos ) 
        elif name == "Compras"     : AddCompras( viaje.tbCompras, Datos ) 
        elif name == "Ventas"      : AddVentas( viaje.tbVentas, Datos ) 
        elif name == "Pagos"       : AddPagos( viaje.tbPagos, Datos ) 
        else: raise Exception("La tabla '{name}' es desconocida")   

def GetRecord( file, rec_name ):
    """ Obtiene todos los datos del registro 'rec_name' """
    Datos = {}

    while True:
        line  = file.readline()                  # Lee una línea
        if not line: raise Exception(f"Se termino de leer el fichero, sin llegar al final del registro '{rec_name}'")  

        name, end = GetTagName( line ) 
        if name==rec_name and end: return Datos 

        if end: raise Exception(f"No se llego al final del registro '{rec_name}'")

        Datos[name] = GetTagValue( line )

def AddPresupesto( table, Datos ):
    """ Agrega un Presupuesto a la base de datos """

    id = int (Datos["id"])

    source = Datos["source"]
    value  = float(Datos["value"] )
    moneda = int  (Datos["moneda"])
    cambio = float(Datos["cambio"])

    row = RowPresupesto( source, value, moneda, cambio )
    table.AddRow( id, row)

def AddGastos( table, Datos ):
    """ Agrega un Gasto a la base de datos """
    
    id = int (Datos["id"])

    descriccion = Datos["descric"]  
    str_value   = Datos["value"  ]    
    valCuc      = float(Datos["cuc"] )

    row = RowGasto( descriccion, str_value, valCuc )
    table.AddRow( id, row )

def AddCompras( table, Datos ):
    """ Agrega una Compra a la base de datos """
    
    id = int (Datos["id"])

    item          = Datos["item"]        
    count         = int(Datos["count"])       
    str_value     = Datos["value"]    
    str_valueItem = Datos["valItem"]     
    valCUC        = float(Datos["valCUC"])
    valCucItem    = float(Datos["valCucItem"])
    precio        = float(Datos["precio"])
    moneda        = int(Datos["moneda"])
    comentario    = Datos.get("comentario", "")

    row = RowCompra(item, count, str_value, str_valueItem, valCUC, valCucItem, comentario, precio, moneda)
    table.AddRow( id, row )

def AddVentas( table, Datos ):
    """ Agrega una venta a la base de datos """
    
    id = int (Datos["id"])

    idProd     = int(Datos["idProd"])
    vendedor   = Datos["vendedor"]
    count      = int(Datos["count"])
    precio     = float(Datos["precio"])
    moneda     = int(Datos["moneda"])
    fecha      = datetime.fromisoformat(Datos["fecha"])
    comentario = Datos.get("comentario", "")

    row = RowVenta( idProd, vendedor, count, precio, moneda, fecha, comentario )
    table.AddRow( id, row )

def AddPagos( table, Datos ):
    """ Agrega un pago a la base de datos """
    
    id = int (Datos["id"])

    idVent     = int(Datos["idVent"])
    count      = float(Datos["count"])
    cuc        = float(Datos["cuc"])
    cup        = float(Datos["cup"])
    fecha      = datetime.fromisoformat(Datos["fecha"])
    comentario = Datos["comentario"]

    row = RowPago(idVent, count, cuc, cup, fecha, comentario)
    table.AddRow( id, row )

if __name__ == '__main__':
    from viaje import checkFile
    class obj: pass
    from os import path

    file_dir = path.join( path.dirname(__file__), "Viajes" )

    vj = obj()
    vj.infoFiles = checkFile( file_dir, "01-Viaje Panamá Noviembre 2017.xml")
    LoadViajeData( vj )

    #nPres = vj.tbPresupesto.NRows()
    #nGast = vj.tbGastos.NRows()
    #nComp = vj.tbCompras.NRows()
    #nVent = vj.tbVentas.NRows()
    #nPago = vj.tbPagos.NRows()

    #print( f"\nDatos Leidos:\n"
    #       f"{'Presupuestos':13}: {nPres:3} regístros\n"
    #       f"{'Gastos'      :13}: {nGast:3} regístros\n"
    #       f"{'Compras'     :13}: {nComp:3} regístros\n"
    #       f"{'Ventas'      :13}: {nVent:3} regístros\n"
    #       f"{'Pagos'       :13}: {nPago:3} regístros\n" ) 

    import locale
    locale.setlocale(locale.LC_ALL, 'es_ES')

    print("\n")  

    print(   f"{'idProd' :7} {'Cant'  :4} {'Vendedor' :10} {'Precio'    :6} {'Mnd'    :3} {'Comentario':40} {'fecha'} " )
    for idVent in vj.tbVentas.rows:
      vt = vj.tbVentas.rows[idVent]  
      print( f"{vt.idProd:7} {vt.count:4} {vt.vendedor:10} {vt.precio:6.2f} {vt.moneda:3} {vt.comentario:40} {vt.fecha:%d de %B} " )

    print("\n")  

