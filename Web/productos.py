from .funciones import *
from flask import current_app, render_template, request, make_response

#-------------------------------------------------------------------------------------------------------------
def show_prods_list():
    dt = obj()
    dt.tab = 1

    params = get_paremetros( request )
    
    app = current_app

    dt.coment      = params.get( "coment"     , '' )=="on"                      # Obtiene parametros
    dt.gananc_raw  = params.get( "gananc-raw" , '' )=="on"
    dt.gananc_item = params.get( "gananc-item", '' )=="on"

    # Obtiene la lista de productos con las opciones dadas
    prods = app.bd.product_list( coment=dt.coment, gananc_raw=dt.gananc_raw, gananc_item=dt.gananc_item)  

    dt.filter = params.get( "filter", "" )                                      # Obtiene parametro para filtrar
    prods     = filter_items( prods, dt.filter, ("sItem", "viaje", "idProd") )  # Filtra la lista de porductos

    dt.sort_attr = params.get( "sort-attr2", "" )                               # Obtiene atributo de ordenamiento
    SortList( prods, dt.sort_attr )                                             # Odena la lista de productos

    dt.attrs_col = header_fun( dt.sort_attr )                                   # Css para los encabezamientos de las columnas

    dt.foot  = suma_attrs( prods, ("count", "montoCuc", "rate", "gananc") )     # Suma las columnas dadas
    promedia( dt.foot, len(prods), ("rate",)  )                                 # Promedia las columnas dadas
    dt.foot.desc = foot_detalles( app.bd.viajes, prods, dt.filter )

    page_now      = int(params.get( "page-now2", 1 ))                           # Obtiene atributos para el paginado
    dt.page_items = int(params.get( "page-items", 20 ))
    
    dt.page_now, dt.pages  = pages_data( page_now, 9, len(prods), dt.page_items )   # Obtiene las paginas a mostrar

    item_ini = (dt.page_now-1)* dt.page_items                                   # Obtiene los items a mostrar
    item_fin = item_ini + dt.page_items  

    dt.prods = prods[ item_ini: item_fin]                                       # Toma de la lista los items de la pagina actual

    resp = make_response( render_template( "productos_list.html", dt=dt ) )

    resp.set_cookie( "filter"     , dt.filter        )
    resp.set_cookie( "sort-attr2" , dt.sort_attr     )
    resp.set_cookie( "page-now2"  , str(dt.page_now) )
    resp.set_cookie( "coment"     , "on" if dt.coment      else "" )
    resp.set_cookie( "gananc-raw" , "on" if dt.gananc_raw  else "" )
    resp.set_cookie( "gananc-item", "on" if dt.gananc_item else "" )
    return resp

