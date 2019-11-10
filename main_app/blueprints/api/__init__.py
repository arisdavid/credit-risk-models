from flask import jsonify
from flask_restplus import Resource, fields, Namespace
from main_app.blueprints.apiv1 import limiter

credit_risk_model_ns = Namespace('creditrisk', description="Http methods")

kmv_model = credit_risk_model_ns.model("KMV", {
    "enterpriseValue": fields.Float(description="Firm's Enterprise Value (market cap can be substituted)"),
    "shortTermDebt": fields.Float(description="Firm's Short Term Debt"),
    "longTermDebt": fields.Float(description="Firm's Long Term Debt"),
    "expectedAnnualReturn": fields.Float(description="Firm's Expected Annual Return"),
    "expectedAnnualVolatility": fields.Float(description="Firm's Expected Annual Volatility")}
                                       )


@credit_risk_model_ns.route('/kmv')
class KealhoferMcQuownVasicek(Resource):
    """
            KMV model is based on the structural approach to calculate a forward looking default probability.
            #ev = enterprise value
            #stDebt = short term debt
            #ltDebt = long term debt
            #mu = expected growth after 1 year
            #sigma = annualized volatility
            #period = period in years
        """

    @credit_risk_model_ns.doc('Kealhofer, McQuown, Vasicek or KMV model estimates the 1yr forward looking probability of default')
    @credit_risk_model_ns.expect(kmv_model)
    @limiter.limit("1000 per day")
    def post(self):
        """ KMV model is based on the structural approach to calculate a forward looking default probability. """
        try:
            pl = credit_risk_model_ns.payload

            # Invoke AWS amazon
            kmv_api_aws_url = "https://cgk5gj9sx6.execute-api.eu-west-2.amazonaws.com/live/kmv"
            response = requests.post(kmv_api_aws_url, json=pl)

            return response.json()


        except Exception as e:

            return jsonify({"message": e}), 400
