import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple
import config as cfg
import math

@dataclass
class ScenarioInputs:
    """Input parameters for scenario calculations."""
    initial_savings: float
    house_cost: float
    monthly_rent: float
    monthly_disposable_income: float
    time_horizon_years: int
    mortgage_term_years: int
    house_inflation: float = cfg.DEFAULT_HOUSE_PRICE_INFLATION
    investment_return: float = cfg.DEFAULT_INVESTMENT_RETURN
    mortgage_rate: float = cfg.DEFAULT_MORTGAGE_RATE
    min_down_payment_percent: float = cfg.DEFAULT_MIN_DOWN_PAYMENT_PERCENT
    cpi: float = cfg.DEFAULT_CPI  # Consumer Price Index for income and rent growth

    def validate(self):
        """
        Validate input values to prevent calculation errors.
        
        Raises:
            ValueError: If any input value is invalid.
        """
        # Convert all numeric inputs to proper types
        self.initial_savings = float(self.initial_savings)
        self.house_cost = float(self.house_cost)
        self.monthly_rent = float(self.monthly_rent)
        self.monthly_disposable_income = float(self.monthly_disposable_income)
        self.time_horizon_years = int(self.time_horizon_years)
        self.mortgage_term_years = int(self.mortgage_term_years)
        self.house_inflation = float(self.house_inflation)
        self.investment_return = float(self.investment_return)
        self.mortgage_rate = float(self.mortgage_rate)
        self.min_down_payment_percent = float(self.min_down_payment_percent)
        self.cpi = float(self.cpi)
        
        # Validate time periods
        if self.time_horizon_years <= 0:
            raise ValueError("Time horizon must be positive.")
        if self.mortgage_term_years <= 0:
            raise ValueError("Mortgage term must be positive.")
        if self.mortgage_term_years > self.time_horizon_years:
            self.mortgage_term_years = self.time_horizon_years
        
        # Validate costs and payments
        if self.house_cost <= 0:
            raise ValueError("House cost must be positive.")
        if self.monthly_rent < 0:
            raise ValueError("Monthly rent cannot be negative.")
        if self.monthly_disposable_income <= 0:
            raise ValueError("Monthly disposable income must be positive.")
        if self.initial_savings < 0:
            raise ValueError("Initial savings cannot be negative.")
            
        # Validate rates
        if self.house_inflation < 0:
            raise ValueError("House inflation rate cannot be negative.")
        if self.investment_return < 0:
            raise ValueError("Investment return rate cannot be negative.")
        if self.mortgage_rate < 0:
            raise ValueError("Mortgage rate cannot be negative.")
        if self.cpi < 0:
            raise ValueError("CPI cannot be negative.")
        
        # Validate realistic value ranges
        if self.house_inflation > 0.2:
            raise ValueError("House inflation rate unrealistically high (>20%).")
        if self.investment_return > 0.2:
            raise ValueError("Investment return rate unrealistically high (>20%).")
        if self.mortgage_rate > 0.2:
            raise ValueError("Mortgage rate unrealistically high (>20%).")
        if self.cpi > 0.2:
            raise ValueError("CPI unrealistically high (>20%).")
        
        # Validate down payment
        if self.min_down_payment_percent < 0 or self.min_down_payment_percent > 1:
            raise ValueError("Down payment percentage must be between 0 and 1.")
        
        # Validate mortgage feasibility
        total_house_cost = self.house_cost * (1 + cfg.HOUSE_PURCHASE_FEES_PERCENT)
        min_down_payment = total_house_cost * self.min_down_payment_percent
        if min_down_payment > self.initial_savings:
            raise ValueError("Initial savings insufficient for minimum down payment.")

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
        monthly_mortgage_min (float): Minimum monthly mortgage payment.
        monthly_mortgage_max (float): Maximum monthly mortgage payment.
    """
    principal_investment_value: float = 0.0
    monthly_investment_value: float = 0.0
    house_value: float = 0.0
    remaining_mortgage: float = 0.0
    total_interest_paid: float = 0.0
    total_rent_paid: float = 0.0
    monthly_mortgage_min: float = 0.0
    monthly_mortgage_max: float = 0.0
    
    def __post_init__(self):
        """Ensure all values are initialized to at least 0.0"""
        self.principal_investment_value = self.principal_investment_value or 0.0
        self.monthly_investment_value = self.monthly_investment_value or 0.0
        self.house_value = self.house_value or 0.0
        self.remaining_mortgage = self.remaining_mortgage or 0.0
        self.total_interest_paid = self.total_interest_paid or 0.0
        self.total_rent_paid = self.total_rent_paid or 0.0
        self.monthly_mortgage_min = self.monthly_mortgage_min or 0.0
        self.monthly_mortgage_max = self.monthly_mortgage_max or 0.0
    
    @property
    def net_worth(self) -> float:
        """Total net worth including all assets and liabilities."""
        try:
            # Ensure all components are valid floats
            principal = float(self.principal_investment_value or 0.0)
            monthly = float(self.monthly_investment_value or 0.0)
            house = float(self.house_value or 0.0)
            mortgage = float(self.remaining_mortgage or 0.0)
            
            net_worth = principal + monthly + house - mortgage
            
            if not isinstance(net_worth, (int, float)) or math.isnan(net_worth) or math.isinf(net_worth):
                print(f"Invalid net worth calculated: {net_worth}")
                return 0.0
                
            return net_worth
            
        except Exception as e:
            print(f"Net worth calculation error: {str(e)}")
            print(f"Values: principal={self.principal_investment_value} ({type(self.principal_investment_value)}), " +
                  f"monthly={self.monthly_investment_value} ({type(self.monthly_investment_value)}), " +
                  f"house={self.house_value} ({type(self.house_value)}), " +
                  f"mortgage={self.remaining_mortgage} ({type(self.remaining_mortgage)})")
            return 0.0

def calculate_future_value_principal(principal: float, years: int, annual_rate: float) -> float:
    """
    Calculate future value of a fixed principal investment.
    
    Args:
        principal (float): Initial investment amount.
        years (int): Investment period in years.
        annual_rate (float): Annual return rate (as decimal).
    
    Returns:
        float: Future value of the principal investment.
    """
    return principal * (1 + annual_rate) ** years

def calculate_mortgage_payment(principal: float, annual_rate: float, years: int) -> float:
    """
    Calculate monthly mortgage payment using the standard amortization formula.
    
    Args:
        principal (float): Loan amount
        annual_rate (float): Annual interest rate (as decimal)
        years (int): Loan term in years
    
    Returns:
        float: Monthly payment amount
    """
    monthly_rate = annual_rate / 12
    n_payments = years * 12
    
    # Handle zero interest rate
    if annual_rate == 0:
        return principal / n_payments
    
    # Standard mortgage payment formula: P * (r(1+r)^n)/((1+r)^n - 1)
    numerator = monthly_rate * (1 + monthly_rate) ** n_payments
    denominator = (1 + monthly_rate) ** n_payments - 1
    return principal * (numerator / denominator)

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
            total_interest += payment * n_months  # All payments go to interest
            return principal, total_interest  # Principal remains unchanged
            
        total_interest += interest
        remaining -= principal_part
    
    return remaining, total_interest

def calculate_future_value_monthly_investment(
    initial_monthly_disposable: float,
    initial_monthly_housing_cost: float,
    years: int,
    investment_return: float,
    cpi: float,
    is_fixed_housing_cost: bool = False
) -> float:
    """
    Calculate future value of monthly investments from disposable income minus housing costs.
    For rent scenario: both disposable income and rent grow with CPI.
    For buy scenario: only disposable income grows with CPI, mortgage is fixed.
    
    Args:
        initial_monthly_disposable: Starting monthly disposable income
        initial_monthly_housing_cost: Starting housing cost (rent or mortgage)
        years: Investment period in years
        investment_return: Annual investment return rate
        cpi: Annual inflation rate for income (and rent if applicable)
        is_fixed_housing_cost: If True, housing cost doesn't grow with inflation (for mortgage)
    
    Returns:
        float: Future value of all monthly investments
    """
    monthly_rate = investment_return / 12
    total_value = 0.0
    
    # Year by year calculation
    for year in range(years):
        # Calculate this year's monthly disposable income (adjusted for CPI)
        monthly_disposable = initial_monthly_disposable * (1 + cpi) ** year
        
        # Calculate this year's housing cost
        if is_fixed_housing_cost:
            monthly_housing = initial_monthly_housing_cost  # Fixed mortgage payment
        else:
            monthly_housing = initial_monthly_housing_cost * (1 + cpi) ** year  # Growing rent
        
        # Calculate this year's monthly investment amount
        monthly_investment = monthly_disposable - monthly_housing
        
        # Add and grow this year's monthly investments
        for month in range(12):
            total_value += monthly_investment
            total_value *= (1 + monthly_rate)
    
    return total_value

def calculate_rent_scenario(inputs: ScenarioInputs) -> ScenarioResults:
    """Calculate results for rent and invest scenario."""
    # Calculate growth of initial savings (principal only)
    principal_growth = calculate_future_value_principal(
        principal=inputs.initial_savings,
        years=inputs.time_horizon_years,
        annual_rate=inputs.investment_return
    )
    
    # Calculate investment growth from monthly contributions
    monthly_growth = calculate_future_value_monthly_investment(
        initial_monthly_disposable=inputs.monthly_disposable_income,
        initial_monthly_housing_cost=inputs.monthly_rent,
        years=inputs.time_horizon_years,
        investment_return=inputs.investment_return,
        cpi=inputs.cpi,
        is_fixed_housing_cost=False
    )
    
    # Calculate total rent paid with inflation
    total_rent = 0.0
    monthly_rent = inputs.monthly_rent
    for year in range(inputs.time_horizon_years):
        total_rent += monthly_rent * 12
        monthly_rent *= (1 + inputs.cpi)
    
    return ScenarioResults(
        principal_investment_value=principal_growth,
        monthly_investment_value=monthly_growth,
        total_rent_paid=total_rent
    )

def calculate_buy_scenario(inputs: ScenarioInputs, max_mortgage=True) -> ScenarioResults:
    """Calculate results for buying scenario."""
    # Calculate total purchase cost including fees
    total_house_cost = inputs.house_cost * (1 + cfg.HOUSE_PURCHASE_FEES_PERCENT)
    
    # Calculate mortgage amounts for both scenarios
    max_mortgage_amount = total_house_cost * (1 - inputs.min_down_payment_percent)
    min_mortgage_amount = min(total_house_cost - inputs.initial_savings, max_mortgage_amount)
    
    # Calculate monthly payments for both scenarios
    max_monthly_payment = calculate_mortgage_payment(
        principal=max_mortgage_amount,
        annual_rate=inputs.mortgage_rate,
        years=inputs.mortgage_term_years
    )
    
    min_monthly_payment = calculate_mortgage_payment(
        principal=min_mortgage_amount,
        annual_rate=inputs.mortgage_rate,
        years=inputs.mortgage_term_years
    )
    
    # Select current scenario's values
    mortgage_amount = max_mortgage_amount if max_mortgage else min_mortgage_amount
    monthly_payment = max_monthly_payment if max_mortgage else min_monthly_payment
    down_payment = min(inputs.initial_savings, total_house_cost - mortgage_amount)
    
    # Calculate remaining mortgage and total interest
    remaining_mortgage, total_interest = calculate_remaining_mortgage(
        principal=mortgage_amount,
        payment=monthly_payment,
        annual_rate=inputs.mortgage_rate,
        years_elapsed=min(inputs.time_horizon_years, inputs.mortgage_term_years)
    )
    
    # Calculate future house value
    future_house_value = inputs.house_cost * (1 + inputs.house_inflation) ** inputs.time_horizon_years
    
    # Calculate growth of remaining initial savings (after down payment)
    principal_growth = calculate_future_value_principal(
        principal=inputs.initial_savings - down_payment,
        years=inputs.time_horizon_years,
        annual_rate=inputs.investment_return
    )
    
    # Calculate investment growth from monthly contributions
    monthly_growth = calculate_future_value_monthly_investment(
        initial_monthly_disposable=inputs.monthly_disposable_income,
        initial_monthly_housing_cost=monthly_payment,
        years=inputs.time_horizon_years,
        investment_return=inputs.investment_return,
        cpi=inputs.cpi,
        is_fixed_housing_cost=True
    )
    
    return ScenarioResults(
        principal_investment_value=principal_growth,
        monthly_investment_value=monthly_growth,
        house_value=future_house_value,
        remaining_mortgage=remaining_mortgage,
        total_interest_paid=total_interest,
        monthly_mortgage_min=min_monthly_payment,
        monthly_mortgage_max=max_monthly_payment
    )

def compare_scenarios(inputs: ScenarioInputs) -> Dict[str, ScenarioResults]:
    """
    Compare all three scenarios: rent, max mortgage, and min mortgage.
    
    Args:
        inputs (ScenarioInputs): Calculation input parameters.
    
    Returns:
        Dict[str, ScenarioResults]: Results for each scenario.
        
    Raises:
        ValueError: If input validation fails or calculations produce invalid results.
    """
    # Validate inputs first
    try:
        inputs.validate()
    except ValueError as e:
        raise ValueError(f"Input validation failed: {str(e)}")
    
    try:
        # Calculate rent scenario
        try:
            rent_scenario = calculate_rent_scenario(inputs)
        except Exception as e:
            raise ValueError(f"Error calculating rent scenario: {str(e)}")
            
        # Calculate max mortgage scenario
        try:
            max_mortgage_scenario = calculate_buy_scenario(inputs, max_mortgage=True)
        except Exception as e:
            raise ValueError(f"Error calculating max mortgage scenario: {str(e)}")
            
        # Calculate min mortgage scenario
        try:
            min_mortgage_scenario = calculate_buy_scenario(inputs, max_mortgage=False)
        except Exception as e:
            raise ValueError(f"Error calculating min mortgage scenario: {str(e)}")
        
        # Validate results have expected values
        for name, scenario in [
            ("rent", rent_scenario), 
            ("max mortgage", max_mortgage_scenario), 
            ("min mortgage", min_mortgage_scenario)
        ]:
            if not isinstance(scenario, ScenarioResults):
                raise ValueError(f"Invalid {name} scenario result type")
            if scenario.net_worth < -inputs.house_cost:
                raise ValueError(f"Unrealistic negative net worth calculated in {name} scenario")
        
        return {
            "rent": rent_scenario,
            "max_mortgage": max_mortgage_scenario,
            "min_mortgage": min_mortgage_scenario
        }
        
    except Exception as e:
        raise ValueError(f"Error calculating scenarios: {str(e)}")