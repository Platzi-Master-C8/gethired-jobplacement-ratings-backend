from enum import Enum


class CompanyRatingType(Enum):
    good = "Good"
    regular = "Regular"
    bad = "Bad"


class CurrencyCodeISO4217(Enum):
    mxn = "MXN"
    cop = "COP"
    clp = "CLP"
    usd = "USD"
    eur = "EUR"


class SalaryFrecuency(Enum):
    hour = "Hour"
    day = "Day"
    month = "Month"
    year = "Year"
