from flask import current_app, render_template, request, make_response, redirect
from .funciones import *

#-------------------------------------------------------------------------------------------------------------
def ShowSumario( num ):
    app = current_app
    if 0 < num >= app.bd.viajes_count():
        return redirect('/sumarios')

    vj = app.bd.get_viaje(num)

    vj.Sobrante = vj.PresupCuc-vj.MontoInvers

    vj.IdxGastos = vj.GastosCUC/vj.CompasCUC      if vj.CompasCUC   else 0
    vj.IdxPrec   = vj.MontoPrecios/vj.CompasCUC   if vj.CompasCUC   else 0
    vj.IdxGananc = vj.MontoPrecios/vj.MontoInvers if vj.MontoInvers else 0

    vj.ConsumoMonto  = vj.MontoConsumoRecp + vj.GanacConsumo
    vj.GananciaVenta = vj.GanacVentas + vj.GanacConsumo

    vj.GanancPagada     = vj.MontoCobros - vj.MontoInvers
    vj.GanancSinConsumo = vj.MontoCobros - (vj.MontoInvers - vj.MontoConsumo)
    vj.GanancConConsumo = vj.GanancPagada + vj.GanacConsumo

    return render_template("sumario.html", vj=vj)
    
#-------------------------------------------------------------------------------------------------------------
def ShowSumario_list():
    dt = obj()                                                                  # Crea objeto para los datos
    dt.tab = 0                                                                  # Pone el primer tab como el actual

    params = get_paremetros( request )                                          # Obtiene todos los paramentros de la solicitud
    dt.no_consumo = params.get( "no-consumo", '' )=="on"                        # Opcion para no tener en cuenta los items de consumo

    app = current_app
    sumarios = app.bd.sumary_list( no_consumo=dt.no_consumo )                   # Obtiene la lista de sumarios

    dt.filter = get_filter( params )                                            # Obtiene parametro para filtrar
    sumarios  = filter_items( sumarios, dt.filter, ("Title", "VjAbr") )         # Filtra la lista de porductos

    dt.sort_attr = params.get( "sort-attr1", "" )                               # Obtiene atributo de ordenamiento
    SortList( sumarios, dt.sort_attr )                                          # Odena la lista de productos

    dt.attrs_col = header_fun( dt.sort_attr )                                   # Css para los encabezamientos de las columnas

    # Suma las columnas dadas
    dt.sums  = suma_attrs( sumarios, ("GastosCUC", "CompasCUC", "RecupIdx", "MontoInvers", "MontoConsumo", "PrecioIndex", "MontoSinVender", "MontoSinPagar", "MontoCobros", "Ganancia", "GananciaIndex" ) )     
    promedia( dt.sums, len(sumarios), ("RecupIdx", "PrecioIndex", "GananciaIndex")  )  

    dt.sumarios = sumarios
    resp = make_response( render_template( "sumarios_list.html", dt=dt ) )

    set_filter( resp, dt.filter )
    resp.set_cookie( "sort-attr1", dt.sort_attr     )
    resp.set_cookie( "no-consumo", "on" if dt.no_consumo else "" )
    return resp

#-------------------------------------------------------------------------------------------------------------
def get_filter( params ):
    """ Obtiene el filtro a aplicar teniendo en cuenta si de definio el viaje en los filtros anterires """

    filter = params.get( "filter1", "" )                            # Obtiene filtro de la ultima visita

    segms  = parse_filter( params.get( "filter", "" ) )             # Separa el filtro de las otras vistas
    if len(segms)>1 and segms[1]:                                   # Definio el viaja
        filter = "/" + segms[1]                                     # Pone filtro para mostrar el viaje

    return filter

#-------------------------------------------------------------------------------------------------------------
def set_filter( resp, sFilter ):
    """ Pone el filtro para la vista y para otras vistas, si se define el viaje """

    resp.set_cookie( "filter1", sFilter )

    segms  = parse_filter( sFilter )                                # Separa el filtro en sus partes
    if len(segms)>1 and segms[1]:                                   # Definio el viaja
        resp.set_cookie( "filter", "/" + segms[1] )                 # La otras vistas deben mostrar el viaje

    return filter


