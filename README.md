# credit-risk-models
Simple example of Credit Risk Model-as-a-service API using Flask-Restplus

## KMV Model
The sample model given here is the KMV model. The KMV model calculates the firm's expected default frequency (EDF) of a firm. EDF is also a proxy for probability-of-default. Credit to(HK UST) for the actual presentation - https://www.math.ust.hk/~maykwok/Web_ppt/KMV/KMV.pdf

```
def kmv(enterprise_value, short_term_debt, long_term_debt, mu, sigma, period=1):
    """
    KMV Model - https://www.math.ust.hk/~maykwok/Web_ppt/KMV/KMV.pdf
    :param enterprise_value: Enterprise Value of the Firm (can market capitalisation)
    :param short_term_debt: Firm's short term debt
    :param long_term_debt: Firm's long term debt
    :param mu: Expected Return after 1 year
    :param sigma: Expected Annualized Volatility
    :param period: period in years
    :return: EDF (Expected Default Frequency or Probability of Default)
    """

    # Calculate default point
    default_point = short_term_debt + (0.5 * long_term_debt)

    # Numerator
    numer = math.log(enterprise_value / default_point) + (mu - math.pow(sigma, 2) / 2) * period

    # Denominator
    denom = sigma * period

    # Distance to Default
    distance_to_default = numer / denom
    edf = norm.cdf(-distance_to_default)

    return edf

```


## Postman
![Postman](https://quantmill.s3.eu-west-2.amazonaws.com/github/credit-risk-kmv-postman.PNG)

## Swagger-UI
![Swagger-UI](https://quantmill.s3.eu-west-2.amazonaws.com/github/credit-risk-kmv-swagger.PNG)


