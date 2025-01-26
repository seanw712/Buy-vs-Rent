import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple
import config as cfg

@dataclass
class ScenarioInputs:
    """
    Represents the input parameters for comparing housing and investment scenarios.
    
    Attributes:
        initial_savings (float): Initial savings available for investment or down payment.
        house_cost (float): Total cost of the house.
        monthly_rent (float): Monthly rent payment.
        time_horizon_years (int): Time horizon for the scenario in years.
        mortgage_term_years (int): Term of the mortgage in years.
        monthly_disposable_income (float): Monthly disposable income after expenses.
        rent_inflation (float): Annual inflation rate for rent (default: cfg.DEFAULT_RENT_INFLATION).
        house_inflation (float): Annual inflation rate for house prices (default: cfg.DEFAULT_HOUSE_PRICE_INFLATION).
        cpi (float): Consumer Price Index inflation rate (default: cfg.DEFAULT_CPI).
        investment_return (float): Annual return on investments (default: cfg.DEFAULT_INVESTMENT_RETURN).
        mortgage_rate (float): Annual mortgage interest rate (default: cfg.DEFAULT_MORTGAGE_RATE).
        min_down_payment_percent (float): Minimum down payment percentage (default: cfg.DEFAULT_MIN_DOWN_PAYMENT_PERCENT).
    """
    initial_savings: float
    house_cost: float
    monthly_rent: float
    time_horizon_years: int
    mortgage_term_years: int
    monthly_disposable_income: float
    
    # Economic variables (optional with defaults)
    rent_inflation: float = cfg.DEFAULT_RENT_INFLATION
    house_inflation: float = cfg.DEFAULT_HOUSE_PRICE_INFLATION
    cpi: float = cfg.DEFAULT_CPI
    investment_return: float = cfg.DEFAULT_INVESTMENT_RETURN
    mortgage_rate: float = cfg.DEFAULT_MORTGAGE_RATE
    min_down_payment_percent: float = cfg.DEFAULT_MIN_DOWN_PAYMENT_PERCENT

    def validate(self):
        """
        Validate input values to prevent calculation errors.
        
        Raises:
            ValueError: If any input value is invalid.
        """
        # Validate time periods
        if self.time_horizon_years <= 0 or self.mortgage_term_years <= 0:
            raise ValueError("Time periods must be positive.")
        
        # Validate costs and payments
        if self.house_cost < 0 or self.monthly_rent < 0:
            raise ValueError("Costs cannot be negative.")
        if self.monthly_disposable_income < 0:
            raise ValueError("Disposable income cannot be negative.")
        
        # Validate economic variables
        if self.rent_inflation < 0 or self.house_inflation < 0:
            raise ValueError("Inflation rates cannot be negative.")
        if self.investment_return < 0:
            raise ValueError("Investment return cannot be negative.")
        if self.mortgage_rate < 0:
            raise ValueError("Mortgage rate cannot be negative.")
        
        # Additional validation for realistic values
        if self.rent_inflation > 0.2 or self.house_inflation > 0.2:
            raise ValueError("Inflation rates are unrealistically high.")
        if self.investment_return > 0.2:
            raise ValueError("Investment return is unrealistically high.")
        if self.mortgage_rate > 0.2:
            raise ValueError("Mortgage rate is unrealistically high.")
        
        if self.min_down_payment_percent < 0 or self.min_down_payment_percent > 1:
            raise ValueError("Down payment percentage must be between 0 and 1")

@dataclass
class ScenarioResults:
    """
    Represents the results of a scenario calculation.
    
    Attributes:
        principal_investment_value (float): Future value of initial investment.
        monthly_investment_value (float): Future value of monthly investments.
        house_value (float): Future value of the house (if applicable).
        remaining_mortgage (float): Remaining mortgage principal (if applicable).
        total_interest_paid (float): Total interest paid on mortgage (if applicable).
        total_rent_paid (float): Total rent paid over time (if applicable).
    """
    principal_investment_value: float
    monthly_investment_value: float
    house_value: float = 0.0
    remaining_mortgage: float = 0.0
    total_interest_paid: float = 0.0
    total_rent_paid: float = 0.0
    
    @property
    def final_investment_value(self) -> float:
        """Total value of all investments."""
        return self.principal_investment_value + self.monthly_investment_value
    
    @property
    def net_worth(self) -> float:
        """Total net worth including all assets and liabilities."""
        return self.final_investment_value + self.house_value - self.remaining_mortgage

def calculate_future_value(principal: float, monthly_payment: float, 
                         years: int, annual_rate: float) -> float:
    """
    Calculate future value of an investment with monthly contributions.
    
    Args:
        principal (float): Initial investment amount.
        monthly_payment (float): Monthly contribution amount.
        years (int): Investment period in years.
        annual_rate (float): Annual return rate (as decimal).
    
    Returns:
        float: Future value of the investment.
    """
    if years <= 0:
        return principal
        
    monthly_rate = annual_rate / 12
    n_months = years * 12
    
    # Future value of initial principal
    fv_principal = principal * (1 + annual_rate) ** years
    
    # Future value of monthly payments (using annuity formula)
    if abs(monthly_rate) < 1e-10:  # Effectively zero rate
        fv_payments = monthly_payment * n_months
    else:
        fv_payments = monthly_payment * ((1 + monthly_rate) ** n_months - 1) / monthly_rate
    
    return max(0, fv_principal + fv_payments)

def calculate_mortgage_payment(principal: float, annual_rate: float, years: int) -> float:
    """
    Calculate fixed monthly mortgage payment.
    
    Args:
        principal (float): Initial mortgage amount.
        annual_rate (float): Annual interest rate (as decimal).
        years (int): Mortgage term in years.
    
    Returns:
        float: Monthly payment amount.
    """
    if annual_rate == 0:
        return principal / (years * 12)
    
    monthly_rate = annual_rate / 12
    n_months = years * 12
    
    # Standard mortgage payment formula
    return principal * (monthly_rate * (1 + monthly_rate) ** n_months) / ((1 + monthly_rate) ** n_months - 1)

def calculate_remaining_mortgage(principal: float, payment: float, 
                              annual_rate: float, years_elapsed: int) -> tuple[float, float]:
    """
    Calculate remaining mortgage principal and total interest paid.
    
    Args:
        principal (float): Initial mortgage amount.
        payment (float): Monthly payment amount.
        annual_rate (float): Annual interest rate (as decimal).
        years_elapsed (int): Years elapsed since mortgage start.
    
    Returns:
        tuple[float, float]: (Remaining principal, Total interest paid)
    """
    monthly_rate = annual_rate / 12
    n_months = years_elapsed * 12
    remaining = principal
    total_interest = 0.0
    
    for _ in range(n_months):
        if remaining <= 0:
            break
            
        interest = remaining * monthly_rate
        principal_part = payment - interest
        
        if principal_part <= 0:  # Payment doesn't cover interest
            break
            
        total_interest += interest
        remaining -= principal_part
    
    return max(0, remaining), total_interest

def calculate_rent_scenario(inputs: ScenarioInputs) -> ScenarioResults:
    """
    Calculate results for the rent and invest scenario.
    
    Args:
        inputs (ScenarioInputs): Calculation input parameters.
    
    Returns:
        ScenarioResults: Calculated scenario results.
    """
    # Calculate total rent paid with inflation
    total_rent = 0
    monthly_rent = inputs.monthly_rent
    for year in range(inputs.time_horizon_years):
        total_rent += monthly_rent * 12
        monthly_rent *= (1 + inputs.rent_inflation)
    
    # Calculate monthly investment amount (disposable income minus rent)
    monthly_investment = inputs.monthly_disposable_income - inputs.monthly_rent
    
    # Calculate investment growth
    principal_investment = calculate_future_value(
        inputs.initial_savings,
        0,  # No monthly additions to principal
        inputs.time_horizon_years,
        inputs.investment_return
    )
    
    monthly_investment_value = calculate_future_value(
        0,  # No initial principal
        monthly_investment,
        inputs.time_horizon_years,
        inputs.investment_return
    )
    
    return ScenarioResults(
        principal_investment_value=principal_investment,
        monthly_investment_value=monthly_investment_value,
        total_rent_paid=total_rent
    )

def calculate_buy_scenario(inputs, max_mortgage=True):
    # Calculate total purchase cost including fees
    total_house_cost = inputs.house_cost * (1 + cfg.HOUSE_PURCHASE_FEES_PERCENT)
    
    # Calculate maximum allowed mortgage based on minimum down payment rule
    max_total_mortgage_amount = total_house_cost * (1 - inputs.min_down_payment_percent)
    
    if not max_mortgage:
        # For min mortgage scenario, take the smaller of:
        # 1. What you need after using all savings
        # 2. Maximum allowed mortgage
        max_total_mortgage_amount = min(total_house_cost - inputs.initial_savings, max_total_mortgage_amount)
    
    down_payment = total_house_cost - max_total_mortgage_amount

    # Calculate monthly mortgage payment using the amortization formula
    monthly_payment = calculate_mortgage_payment(
        principal=max_total_mortgage_amount,
        annual_rate=inputs.mortgage_rate,
        years=inputs.mortgage_term_years
    )

    # Calculate remaining mortgage and total interest paid
    remaining_mortgage, total_interest = calculate_remaining_mortgage(
        principal=max_total_mortgage_amount,
        payment=monthly_payment,
        annual_rate=inputs.mortgage_rate,
        years_elapsed=min(inputs.time_horizon_years, inputs.mortgage_term_years)
    )

    # Calculate future house value
    future_house_value = inputs.house_cost * (1 + inputs.house_inflation) ** inputs.time_horizon_years
    
    # Calculate investment of remaining money
    initial_investment = max(0, inputs.initial_savings - down_payment)
    monthly_investment = max(0, inputs.monthly_disposable_income - monthly_payment)
    
    principal_investment = calculate_future_value(
        initial_investment,
        0,  # No monthly additions to principal
        inputs.time_horizon_years,
        inputs.investment_return
    )
    
    monthly_investment_value = calculate_future_value(
        0,  # No initial principal
        monthly_investment,
        inputs.time_horizon_years,
        inputs.investment_return
    )
    
    return ScenarioResults(
        principal_investment_value=principal_investment,
        monthly_investment_value=monthly_investment_value,
        house_value=future_house_value,
        remaining_mortgage=remaining_mortgage,
        total_interest_paid=total_interest
    )

def compare_scenarios(inputs: ScenarioInputs) -> Dict[str, ScenarioResults]:
    """
    Compare all three scenarios: rent, max mortgage, and min mortgage.
    
    Args:
        inputs (ScenarioInputs): Calculation input parameters.
    
    Returns:
        Dict[str, ScenarioResults]: Results for each scenario.
    """
    inputs.validate()
    
    return {
        "rent": calculate_rent_scenario(inputs),
        "max_mortgage": calculate_buy_scenario(inputs, max_mortgage=True),
        "min_mortgage": calculate_buy_scenario(inputs, max_mortgage=False)
    }