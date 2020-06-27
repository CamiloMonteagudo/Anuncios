from .funciones import *
from flask import current_app, render_template, request, make_response

#-------------------------------------------------------------------------------------------------------------
def show_sinPagar_list():
    dt = obj()
    dt.tab = 4

    params = get_paremetros( request )
    
    app = current_app

    dt.filter   = params.get( "filter"  , "" )                                  # Obtiene parametro para mostrar
    dt.vendedor = params.get( "vendedor", 'Todos' )                             # Vendedor actual

    # Obtiene la lista de ventas con las opciones dadas
    pagos = app.bd.sinPagar_list( dt.filter, dt.vendedor )

    dt.sort_attr6 = params.get( "sort-attr6", "" )                              # Obtiene atributo de ordenamiento
    SortList( pagos, dt.sort_attr6 )                                            # Odena la lista de las ventas

    dt.attrs_col = header_fun( dt.sort_attr6 )                                  # Función para menejar el encabezamiento de la lista

    dt.foot = suma_attrs( pagos, ("resto","xPagarCuc") )                        # Suma las columnas dadas
    dt.foot.desc = foot_detalles( app.bd.viajes, pagos, dt.filter )

    page_now      = int(params.get( "page-now6", 1 ))                            # Obtiene atributos para el paginado
    dt.page_items = int(params.get( "page-items", 20 ))
    
    dt.page_now, dt.pages  = pages_data( page_now, 9, len(pagos), dt.page_items )   # Obtiene las paginas a mostrar

    item_ini = (dt.page_now-1)* dt.page_items                                   # Obtiene los items a mostrar
    item_fin = item_ini + dt.page_items  

    dt.prods = pagos[ item_ini: item_fin]                                       # Toma de la lista los items de la pagina actual

    dt.vendedores =  app.bd.get_vendedores()                                    # Lista de vendedores disponibles

    resp = make_response( render_template( "sin_pagar_list.html", dt=dt ) )

    resp.set_cookie( "filter"     , dt.filter     )
    resp.set_cookie( "vendedor"   , dt.vendedor   )
    resp.set_cookie( "sort-attr6" , dt.sort_attr6 )
    resp.set_cookie( "page-now6"  , str(dt.page_now)   )
    return resp
