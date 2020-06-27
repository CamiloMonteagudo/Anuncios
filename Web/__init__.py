import os, sys
from flask import Flask, g
import locale
locale.setlocale(locale.LC_ALL, 'es_ES')

sep = os.path.sep                                       # Obtiene separador de directorios
dir_root = sep.join( __file__.split(sep)[0:-2] )        # Obtiene el directorio raiz del proyecto
dir_data = os.path.join(dir_root, "Datos")              # Obtiene el directorio del modulos de datos

sys.path.insert( 0, dir_data )                          # Inserta el directorio en la busqueda de modulos
print( "\n")
print( f"DIRECTORIO RAIZ  ->'{dir_root}'")
print( f"DIRECTORIO DATOS ->'{dir_data}'\n")
    
dir_viajes = os.path.join(dir_data, "Viajes")

from .viajes_datos import ViajesData                    # Modulos que maneja los datos

#=================================================================================================================
def create_app():
    app = Flask(__name__, instance_relative_config=True )           # Crea la aplicación

    app.dir_root   = dir_root                                       # Guarda los direcctorios en la aplicación
    app.dir_data   = dir_data
    app.dir_viajes = dir_viajes

    app.bd = ViajesData( dir_viajes )                               # Guarda los datos de los viajes en la aplicación

    from . import app_rutes                                         # Impota las rutas del sitio
    app.register_blueprint( app_rutes.bp )


    return app

#=================================================================================================================


