class obj: pass                             # Define un objeto generico para adicionarle propiedades

#-------------------------------------------------------------------------------------------------------------
def pages_data( pg_now, num_pages, num_items, pg_items ):
    """Obtiene una lista con los datos de todas las paginas a mostrar"""

    pg_last = (int)((num_items+(pg_items-1))/pg_items) + 1      # Indice de la última pagina

    if pg_now < 1       : pg_now = 1                            # Garantiza que la página actual este entre los limites                                    
    if pg_now >= pg_last: pg_now = pg_last-1             

    ini = pg_now - int (num_pages/2)                            # Pone la pagina actual en el medio del rango
    if ini < 1: ini = 1                                         # Ajusta la primera pagina, si antes de la primera

    fin = ini + num_pages                                       # Calcula última pagina del rango
    if fin > pg_last:                                           # Si es mayor que la última
        fin = pg_last                                           # Ajusta la ultima página
        ini = pg_last - num_pages                               # Calcula a partir de la última               
        if ini < 1: ini = 1                                     # Si menor que la primera, la corrige

    mrkDel = 4                                                  # Cantidad de items a marcar para borrar
    sz     = (fin-ini)                                          # Cantidad real de paginas a mostrar
    ndel   = sz - (num_pages-mrkDel)                            # Cantidad real de items a borrar
    delIzg = int(ndel/(mrkDel/2))                               # Número a marcar a la izquierda
    delDer = int(ndel-delIzg)                                   # Número a marcar a la derecha

    dt = pg_now - (ini + int(sz/2))                             # Desviacion de la pagina actual del medio del rango
    if dt<0:                                                    # Si la pagina actual esta hasta la izquierda
        if dt<-delIzg: dt = -delIzg                             # Limita la desviacion a la cantidad necesaria
    elif dt>0:                                                  # Si la pagina actual esta hacia la derecha
        if dt>delDer: dt = delDer                               # Limimita la desviación a la cantidad necesaria

    delIzg = ini + delIzg + dt                                  # Calcula los extermos por ambos lados
    delDer = fin - (delDer-dt)

    pages = []
    for i in range(ini,fin):                                    # Pone toda la informacion en una lista de páginas
        pg = obj()
        pg.num = i

        if i==pg_now:  pg.css=' class="active"'
        elif i< delIzg: pg.css=' class="del"'
        elif i>=delDer: pg.css=' class="del"'
        else          : pg.css=''    

        pages.append( pg )    

    return pg_now, pages                                       # Retorna la información de todas las páginas

#-------------------------------------------------------------------------------------------------------------
def get_paremetros( rq ):
    """Obtiene todos los parametros de la pagina tanto POST o GET"""
    
    if rq.method == 'POST': return rq.form

    return rq.cookies

#-------------------------------------------------------------------------------------------------------------
def SortList( lst, sort_attr):
    """ Ordena una lista de listas, según el indice 'idx_sort' de la lista interior """
    if len(lst)<2: return 

    desc = False
    if sort_attr.startswith("-") : desc, sort_attr = True, sort_attr[1:]  

    if not hasattr( lst[0], sort_attr ): return    
        
    lst.sort( key=lambda x:getattr(x,sort_attr), reverse=desc )    

#-------------------------------------------------------------------------------------------------------------
def header_fun( sort_attr ):
    """Obtiene una función para determinar el estilo del encabezamiento de la tabla"""

    def get_css( sAttr ):
        nonlocal sort_attr
        attrs = f' name-col="{sAttr}"'
        sort  = sort_attr 
        
        css = 'asc' 
        if sort.startswith("-") : css, sort = 'desc', sort[1:]  
        if sAttr != sort: return attrs

        return attrs + f' class="{css}"' 

    return get_css

#-------------------------------------------------------------------------------------------------------------
def filter_items( lst, sfilter, fields ):
    """Filtra la lista, según 'sfilter' por los campos 'field1' y 'field2'"""

    vals = parse_filter( sfilter  )

    flist = []
    for item in lst:     
        if not check_filter( item, fields, vals ):                          # Filtra por una cadena
            continue

        flist.append(item)                                                  # Adiciona el item a los encontrados

    return flist      

#-------------------------------------------------------------------------------------------------------------
def parse_filter( sfilter ):
    """Analiza la cadena de filtrado y retorna los 2 posibles campos de filtrado"""

    values = []    
    sfilter = sfilter.strip().lower()                                   # Pone todo el filtro a ninusculas
    if len(sfilter)==0 : return values                                  # Si no hay filtro no hace nada

    for sVal in sfilter.split( "/" ):
        sVal = sVal.strip()                                             # Quita espacios a primera busqueda
        if len(sVal)==0: sVal=False                                     # Chequea por los campos a buscar
        values.append(sVal)    

    return values                                                       # retorna los filtros para buecar

#-------------------------------------------------------------------------------------------------------------
def check_filter( item, fields, values ):
    """Cheque si el item 'item' cumple con los filtros especificados"""

    chks = zip(fields, values)
    for fd, val in chks:
        if not val: continue

        fval = getattr( item, fd )
        if isinstance(fval,str):
            idx = fval.lower().find( val )
            if idx<0: return False
            setattr( item, fd, set_mark( fval, idx, len(val)) )    
        else:
            if val != str(fval): return False

    return True

#-------------------------------------------------------------------------------------------------------------
def set_mark( str,  ini, count ):
    """ Pone una marca en la cadena 'str', desde el indice 'idx' y la cantidad de caracteres 'count' """

    fin = ini + count
    return f"{str[:ini]}<b>{str[ini:fin]}</b>{str[fin:]}"
#-------------------------------------------------------------------------------------------------------------
def suma_attrs( lst,  attrs ):
    """Obtiene las sumatoria de todos los atrbutos especificados en 'attrs' """

    sums = obj()
    for attr in attrs: setattr( sums, attr, 0 )

    for item in lst:                         
        for attr in attrs: 
            val1 = getattr( item, attr )
            val2 = getattr( sums, attr )

            setattr( sums, attr, val2 + val1 )

    return sums
                
#-------------------------------------------------------------------------------------------------------------
def promedia( sums, count,  attrs ):
    """Obtiene el promedio de todos los atrbutos de 'sum' especificados en 'attrs' """

    if count==0: return
    for attr in attrs: 
        sum = getattr( sums, attr )

        setattr( sums, attr, sum/count )

#-------------------------------------------------------------------------------------------------------------------
def foot_detalles( viajes, lista, sfilter ):
    """Si el item esta fitrado por producto o por venta obtine los detalles del producto o la venta"""
    desc = "Totales:"

    if len(lista)==0: return desc                                               # No hay pagos que mostrar
    item = lista[0]    

    vals = sfilter.split( "/" )
    nfilt = len(vals)
    if nfilt<3: return desc                                                     # No se filtra por producto o venta

    if nfilt==3 and len(vals[2].strip())>0:
        prod = viajes.find_prod( item.iVj, item.idProd )   
        return f"Producto {item.idProd} ▶ {prod.count} items ▶ {prod.monto:.2f} cuc"

    idVent = getattr( item, "idVent", False )    
    if nfilt==4 and idVent and len(vals[3].strip())>0:
        prod = viajes.find_venta( item.iVj, idVent )   
        return f"Venta {idVent} ▶ {prod.count} items ▶ {prod.monto:.2f} cuc"

    return desc

#=====================================================================================================================
if __name__ == '__main__':
    pg_now = 6                         # Pagina actual
    num_pages = 11                      # Número de paginas a mostrar
    num_items = 260                     # Numero de items totales
    pg_items  = 25                      # Número de items por pagina

    pnow, pages = pages_data( pg_now, num_pages, num_items, pg_items )

    print("\n")
    for pg in pages:
        if   "active" in pg.css :print( f"[{pg.num}]", end='' )
        elif "del"    in pg.css :print( f"-{pg.num}-", end='' )
        else                    :print( f"{pg.num}", end = '' )

        ini = (pg.num-1)*pg_items + 1     
        print( f"({ini}-{ini+pg_items-1})", end = ' ' )

    print("\n")
