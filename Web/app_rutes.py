from flask import Blueprint

bp = Blueprint('Web', __name__, url_prefix='')

@bp.route( '/sumario/<int:num>/', methods=('GET','POST')  )
def ShowSumario(num):
    from .sumarios import ShowSumario
    return ShowSumario(num)

@bp.route( '/sumarios/', methods=('GET','POST')  )
def ShowSumarios():
    from .sumarios import ShowSumario_list
    return ShowSumario_list()

from .productos import show_prods_list
@bp.route( '/productos/', methods=('GET','POST')  )
def show_productos():
    return show_prods_list( )

from .ventas import show_ventas_list
@bp.route( '/ventas/', methods=('GET','POST')  )
def show_ventas():
    return show_ventas_list( )

from .pagos import show_pagos_list
@bp.route( '/pagos/', methods=('GET','POST') )
def show_pagos():
    return show_pagos_list( )

from .sin_vender import show_sinVender_list
@bp.route( '/por-vender/', methods=('GET','POST')  )
def show_sinvender():
    return show_sinVender_list( )

from .sin_pagar import show_sinPagar_list
@bp.route( '/por-pagar/', methods=('GET','POST')  )
def show_sinPagar():
    return show_sinPagar_list( )
