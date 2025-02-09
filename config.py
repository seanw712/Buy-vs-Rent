"""
Configuration file containing default economic variables and constants.
"""

# Economic Variables (annual rates)
DEFAULT_CPI = 0.025  # 2.5  % consumer price inflation (used for rent and income growth)
DEFAULT_HOUSE_PRICE_INFLATION = 0.035  # 3.5% annual house price appreciation
DEFAULT_INVESTMENT_RETURN = 0.09  # 9% annual investment return (after tax)
DEFAULT_MORTGAGE_RATE = 0.025  # 2.5% mortgage interest rate

# Default Input Values
DEFAULT_INITIAL_SAVINGS = 50000  # €50,000 initial savings
DEFAULT_HOUSE_COST = 200000  # €200,000 house price
DEFAULT_MONTHLY_RENT = 650  # €650 monthly rent
DEFAULT_MONTHLY_SAVINGS_CAPACITY = 700  # €700 monthly savings capacity
DEFAULT_TIME_HORIZON_YEARS = 30  # 30 years time horizon
DEFAULT_MORTGAGE_TERM_YEARS = 25  # 25 years mortgage term
DEFAULT_MIN_DOWN_PAYMENT_PERCENT = 0.15  # 15% minimum down payment

# Mortgage Constants
MIN_DOWN_PAYMENT_PERCENT = 0.10  # 10% minimum down payment
MAX_DOWN_PAYMENT_PERCENT = 0.90  # 90% maximum down payment

# Transaction Costs
DEFAULT_HOUSE_PURCHASE_FEES_PERCENT = 0.07  # 7% of house price for closing costs, fees, etc.

# Time Constants
MONTHS_PER_YEAR = 12 