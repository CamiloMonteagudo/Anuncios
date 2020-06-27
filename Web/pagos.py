from .funciones import *
from flask import current_app, render_template, request, make_response

#-------------------------------------------------------------------------------------------------------------
def show_pagos_list():
    dt = obj()
    dt.tab = 5

    params = get_paremetros( request )
    
    app = current_app

    dt.filter   = params.get( "filter"  , "" )                                  # Obtiene parametrso para mostrar
    dt.vendedor = params.get( "vendedor", 'Todos' )                             # Vendedor actual

    # Obtiene la lista de ventas con las opciones dadas
    pagos = app.bd.pagos_list( dt.filter, dt.vendedor )

    dt.sort_attr = params.get( "sort-attr4", "" )                               # Obtiene atributo de ordenamiento
    SortList( pagos, dt.sort_attr )                                             # Odena la lista de las ventas

    dt.attrs_col = header_fun( dt.sort_attr )                                   # Función para menejar el encabezamiento de la lista

    dt.foot = suma_attrs( pagos, ("count","cuc", "cup", "Total") )             # Suma las columnas dadas
    dt.foot.desc = foot_detalles( app.bd.viajes, pagos, dt.filter )

    page_now      = int(params.get( "page-now4", 1 ))                           # Obtiene atributos para el paginado
    dt.page_items = int(params.get( "page-items", 20 ))
    
    dt.page_now, dt.pages  = pages_data( page_now, 9, len(pagos), dt.page_items )   # Obtiene las paginas a mostrar

    item_ini = (dt.page_now-1)* dt.page_items                                   # Obtiene los items a mostrar
    item_fin = item_ini + dt.page_items  

    dt.prods = pagos[ item_ini: item_fin]                                       # Toma de la lista los items de la pagina actual

    dt.vendedores =  app.bd.get_vendedores()                                    # Lista de vendedores disponibles

    resp = make_response( render_template( "pagos_list.html", dt=dt ) )

    resp.set_cookie( "filter"     , dt.filter        )
    resp.set_cookie( "vendedor"   , dt.vendedor      )
    resp.set_cookie( "sort-attr4" , dt.sort_attr     )
    resp.set_cookie( "page-now4"  , str(dt.page_now) )
    return resp

#-------------------------------------------------------------------------------------------------------------------
def get_detalles( pagos, sfilter ):
    """Si el item esta fitrado por producto o per venta obtine los detalles del producto o la venta"""
    desc = "Totales:"

    if len(pagos)==0: return desc                                               # No hay pagos que mostrar
    pg = pagos[0]    

    vals = sfilter.split( "/" )
    nfilt = len(vals)
    if nfilt<3: return desc                                                     # No se filtra por producto o venta

    app = current_app
    if nfilt==3 and len(vals[2].strip())>0:
        prod = app.bd.viajes.find_prod( pg.iVj, pg.idProd )   
        return f"Producto {pg.idProd} ▶ {prod.count} items ▶ {prod.monto:.2f} cuc"

    if nfilt==4 and len(vals[3].strip())>0:
        prod = app.bd.viajes.find_venta( pg.iVj, pg.idVent )   
        return f"Venta {pg.idVent} ▶ {prod.count} items ▶ {prod.monto:.2f} cuc"

    return desc