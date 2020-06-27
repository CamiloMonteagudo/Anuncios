import money as Mnd
class Table():
    """Clase base para todas las tables de la base de datos"""

    def __init__ (self):
        """Crea una tabla sin ninguna columna"""
        self.rows = {}
        self.nowId = 0

    def NRows(self):
        """Retorna el número de columnas de en la tabla"""
        return len(self.rows)

    def AddRow(self, key, row):
        """Adiciona un registro a la tabla"""
        if not key : 
            key = self.nowId
            self.nowId += 1
        self.rows[key] = row
        return key

    def DelRow( self, key ):
        """Borra un registro de la Tabla"""
        if( key not in self.rows): return False

        del(self.rows[key])
        return True

class RowPresupesto():
    """Datos de un presuspuesto para un viaje"""

    def __init__ (self, source, value, moneda=0, cambio=1.0):
        self.source = source
        self.value = value
        self.moneda = moneda
        self.cambio = cambio


class RowGasto():
    """Datos de un gasto durante un viaje"""

    def __init__ (self, descriccion, str_value, valCuc ):
        self.descric = descriccion
        self.value   = str_value                        # Cadena con el valor y la moneda Ej: '20 Usd'
        self.valCuc  = valCuc

    def Calculate (self, fn_Cnv):
        """Calcula los valores de los campos según la función de conversion"""

        val, mnd = Mnd.GetValue(self.value)
        self.cuc = fn_Cnv(val, mnd)             

class RowCompra():
    """Datos de una compra durante un viaje"""

    def __init__ (self, item, count, str_value, str_valueItem, valCUC, valCucItem, comentario="", precio=0, moneda=0):
        self.item    = item
        self.count   = count
        self.value   = str_value                          # Cadena con el valor y la moneda Ej: '20 Usd'
        self.valItem = str_valueItem
        self.valCUC  = valCUC             
        self.valCucItem = valCucItem
        self.precio = precio
        self.moneda = moneda
        self.comentario = comentario

    def Calculate (self, fn_Cnv):
        """Calcula los valores de los campos según la función de conversion"""

        val, mnd = Mnd.GetValue(self.value)
        valItem = val/count

        self.valItem = f"{valItem} {Mnd.sCode(mnd) }"
        self.valCUC     = fn_Cnv(val, mnd)             
        self.valCucItem = fn_Cnv(valItem, mnd)

class RowVenta():
    """Datos de una venta de un item"""

    def __init__ (self, idProd, vendedor, count, precio, moneda, fecha, comentario=""):
        self.idProd = idProd
        self.vendedor = vendedor
        self.count = count
        self.precio = precio
        self.moneda = moneda
        self.fecha = fecha
        self.comentario = comentario

class RowPago():
    """Datos de un pago a una venta realizada"""

    def __init__ (self, idVent, count, cuc, cup, fecha, comentario=""):
        self.idVent = idVent
        self.count = count
        self.cuc = cuc
        self.cup = cup
        self.fecha = fecha
        self.comentario = comentario

if __name__ == '__main__':
    tbPresupesto = Table()
    presupuesto = RowPresupesto("Reservas para compras", 100, 2, 1.1 )
    tbPresupesto.AddRow(None, presupuesto)

    print( f"Número de registros = {tbPresupesto.NRows()}" ) 

    row = tbPresupesto.rows[0]
    print( f"Descriccion = {row.source}" ) 
    print( f"Valor       = {row.value}"  ) 
    print( f"Moneda      = {row.moneda}" ) 
    print( f"Cambio      = {row.cambio}" ) 
