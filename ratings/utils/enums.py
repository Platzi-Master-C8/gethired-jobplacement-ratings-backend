from enum import Enum


class CompanySalaryRating(Enum):
    high = "High"
    average = "Average"
    low = "Low"


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


class SalaryFrequency(Enum):
    hour = "Hour"
    day = "Day"
    week = "Week"
    month = "Month"
    year = "Year"
