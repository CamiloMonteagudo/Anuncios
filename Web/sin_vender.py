from .funciones import *
from flask import current_app, render_template, request, make_response

#-------------------------------------------------------------------------------------------------------------
def show_sinVender_list():
    dt = obj()
    dt.tab = 2

    params = get_paremetros( request )
    
    app = current_app

    dt.filter = params.get( "filter"  , "" )                                  # Obtiene parametrso para mostrar

    # Obtiene la lista de ventas con las opciones dadas
    pagos = app.bd.sinVender_list( dt.filter )

    dt.sort_attr = params.get( "sort-attr5", "" )                               # Obtiene atributo de ordenamiento
    SortList( pagos, dt.sort_attr )                                             # Odena la lista de las ventas

    dt.attrs_col = header_fun( dt.sort_attr )                                   # Función para menejar el encabezamiento de la lista

    dt.foot = suma_attrs( pagos, ("resto","value", "montoCuc") )                # Suma las columnas dadas
    dt.foot.desc = foot_detalles( app.bd.viajes, pagos, dt.filter )

    page_now      = int(params.get( "page-now5", 1 ))                           # Obtiene atributos para el paginado
    dt.page_items = int(params.get( "page-items", 20 ))
    
    dt.page_now, dt.pages  = pages_data( page_now, 9, len(pagos), dt.page_items )   # Obtiene las paginas a mostrar

    item_ini = (dt.page_now-1)* dt.page_items                                   # Obtiene los items a mostrar
    item_fin = item_ini + dt.page_items  

    dt.prods = pagos[ item_ini: item_fin]                                       # Toma de la lista los items de la pagina actual

    resp = make_response( render_template( "sin_vender_list.html", dt=dt ) )

    resp.set_cookie( "filter"     , dt.filter        )
    resp.set_cookie( "sort-attr5" , dt.sort_attr     )
    resp.set_cookie( "page-now5"  , str(dt.page_now) )
    return resp

#-------------------------------------------------------------------------------------------------------------
