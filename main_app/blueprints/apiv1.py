from flask import Blueprint
from flask_restplus import Api
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


limiter = Limiter(key_func=get_remote_address, default_limits=["1000 per day"])

api_blueprint = Blueprint('api', __name__, url_prefix='/api/v1')

api = Api(api_blueprint,
          title='Credit Risk Model-as-Service',
          description='API limit is 1000 calls per day.',
          version=1.0)

from main_app.blueprints.api import creditriskmodelsns
api.add_namespace(creditriskmodelsns.credit_risk_model_ns)
