from flask import jsonify
from flask_restplus import Resource, fields, Namespace
from main_app.blueprints.apiv1 import limiter
from quant_models.credit_risk_models import kmv

credit_risk_model_ns = Namespace('creditrisk', description="Http methods")

kmv_model = credit_risk_model_ns.model("KMV", {
    "enterpriseValue": fields.Float(description="Firm's Enterprise Value (market cap can be substituted)"),
    "shortTermDebt": fields.Float(description="Firm's Short Term Debt"),
    "longTermDebt": fields.Float(description="Firm's Long Term Debt"),
    "expectedAnnualReturn": fields.Float(description="Firm's Expected Annual Return"),
    "expectedAnnualVolatility": fields.Float(description="Firm's Expected Annual Volatility")})


@credit_risk_model_ns.route('/kmv')
class KealhoferMcQuownVasicek(Resource):
    """
            KMV model is based on the structural approach to calculate a forward looking default probability.
     """

    @credit_risk_model_ns.doc('Kealhofer, McQuown, Vasicek or KMV model estimates the 1yr forward looking probability of default')
    @credit_risk_model_ns.expect(kmv_model)
    @limiter.limit("1000 per day")
    def post(self):
        """ KMV model is based on the structural approach to calculate a forward looking default probability. """
        try:
            pl = credit_risk_model_ns.payload

            enterprise_value = pl.get('enterpriseValue')
            short_term_debt = pl.get('shortTermDebt')
            long_term_debt = pl.get('longTermDebt')
            mu = pl.get('expectedAnnualReturn')
            sigma = pl.get('expectedAnnualVolatility')

            edf = kmv(enterprise_value, short_term_debt, long_term_debt, mu, sigma)

            response = jsonify(edf=edf)
            response.status_code = 200
            return response

        except Exception as error:

            response = jsonify(message=error)
            response.status_code = 400


