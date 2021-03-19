from flask import Blueprint

routes = Blueprint ( 'routes' , __name__ )

# register routes 
from .processMethod import *
