from flask_restful import Api
api = Api(prefix='/api/v1.0')
from . import classified, details, macro, reference


__all__ = [classified, details, macro, reference, api]
