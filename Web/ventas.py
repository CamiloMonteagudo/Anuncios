from .funciones import *
from flask import current_app, render_template, request, make_response

#-------------------------------------------------------------------------------------------------------------
def show_ventas_list():
    dt = obj()
    dt.tab = 3

    params = get_paremetros( request )
    
    app = current_app

    dt.filter   = params.get( "filter"  , "" )                                # Obtiene parametrso para mostrar
    dt.vendedor = params.get( "vendedor", 'Todos' )                           # Vendedor actual
    dt.coment   = params.get( "coment"  , '' )=="on"                      
    dt.pagos    = params.get( "pagos"   , '' )=="on"

    # Obtiene la lista de ventas con las opciones dadas
    ventas = app.bd.ventas_list( dt.filter, dt.vendedor, dt.coment, dt.pagos )

    dt.sort_attr = params.get( "sort-attr3", "" )                             # Obtiene atributo de ordenamiento
    SortList( ventas, dt.sort_attr )                                          # Odena la lista de las ventas

    dt.attrs_col = header_fun( dt.sort_attr )                                 # Función para menejar el encabezamiento de la lista

    dt.foot       = suma_attrs( ventas, ("Cant", "Total") )                    # Suma las columnas dadas
    dt.foot.desc = foot_detalles( app.bd.viajes, ventas, dt.filter )

    page_now      = int(params.get( "page-now3", 1 ))                          # Obtiene atributos para el paginado
    dt.page_items = int(params.get( "page-items", 20 ))
    
    dt.page_now, dt.pages  = pages_data( page_now, 9, len(ventas), dt.page_items )   # Obtiene las paginas a mostrar

    item_ini = (dt.page_now-1)* dt.page_items                                   # Obtiene los items a mostrar
    item_fin = item_ini + dt.page_items  

    dt.prods = ventas[ item_ini: item_fin]                                      # Toma de la lista los items de la pagina actual

    dt.vendedores =  app.bd.get_vendedores()                                    # Lista de vendedores disponibles

    resp = make_response( render_template( "ventas_list.html", dt=dt ) )

    resp.set_cookie( "filter"    , dt.filter        )
    resp.set_cookie( "vendedor"  , dt.vendedor      )
    resp.set_cookie( "sort-attr3", dt.sort_attr     )
    resp.set_cookie( "page-now3" , str(dt.page_now) )
    resp.set_cookie( "coment"    , "on" if dt.coment else "" )
    resp.set_cookie( "pagos"     , "on" if dt.pagos  else "" )
    return resp

