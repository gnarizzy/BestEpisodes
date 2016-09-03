import math
K_VALUE = 32
from decimal import Decimal
#calculates elo changes
#could also just return the negative rating change for rating2, but calculating it seems more precise if k-values aren't
#fixed for both players



def calculate(rating1, rating2, result):
    result = Decimal(result)
    expected = expected_score(rating1, rating2)
    new_rating1 = rating1 + K_VALUE*(result - expected)
    new_rating2 = rating2 + K_VALUE*(expected - result)
    return new_rating1, new_rating2

#splits up calculation into multiple variables for clarity
def expected_score(rating1, rating2):
    difference = rating2 - rating1
    exponent = Decimal(difference/400)
    denonimator = Decimal(1 + math.pow(10, exponent))
    return Decimal(1/denonimator)

#TODO add tests

