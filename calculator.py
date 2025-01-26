import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple
import config as cfg

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
        # Validate time periods
        if self.time_horizon_years <= 0 or self.mortgage_term_years <= 0:
            raise ValueError("Time periods must be positive.")
        
        # Validate costs and payments
        if self.house_cost < 0 or self.monthly_rent < 0:
            raise ValueError("Costs cannot be negative.")
        if self.monthly_disposable_income < 0:
            raise ValueError("Disposable income cannot be negative.")
        
        # Validate economic variables
        if self.house_inflation < 0 or self.cpi < 0:
            raise ValueError("Inflation rates cannot be negative.")
        if self.investment_return < 0:
            raise ValueError("Investment return cannot be negative.")
        if self.mortgage_rate < 0:
            raise ValueError("Mortgage rate cannot be negative.")
        
        # Additional validation for realistic values
        if self.house_inflation > 0.2 or self.cpi > 0.2:
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
    
    @property
    def final_investment_value(self) -> float:
        """Total value of all investments."""
        return max(0.0, (self.principal_investment_value or 0.0) + (self.monthly_investment_value or 0.0))
    
    @property
    def net_worth(self) -> float:
        """Total net worth including all assets and liabilities."""
        return (self.principal_investment_value or 0.0) + \
               (self.monthly_investment_value or 0.0) + \
               (self.house_value or 0.0) - \
               (self.remaining_mortgage or 0.0)

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
    try:
        if years <= 0:
            return principal
            
        if principal < 0:
            principal = 0
            
        # Future value of initial principal (prevent negative growth)
        fv_principal = max(0, principal * (1 + annual_rate) ** years)
        
        return fv_principal
        
    except Exception as e:
        print(f"Future value calculation error: principal={principal}, " +
              f"years={years}, annual_rate={annual_rate}")
        raise ValueError(str(e))

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
    try:
        if years <= 0:
            raise ValueError("Mortgage term must be positive")
            
        if principal <= 0:
            return 0.0
            
        if annual_rate < 0:
            raise ValueError("Interest rate cannot be negative")
            
        # Handle zero or very small interest rate
        if abs(annual_rate) < 1e-10:
            return principal / (years * 12)
            
        monthly_rate = annual_rate / 12
        n_payments = years * 12
        
        # Standard mortgage payment formula: P * (r(1+r)^n)/((1+r)^n - 1)
        # where P = principal, r = monthly rate, n = number of payments
        try:
            numerator = monthly_rate * (1 + monthly_rate) ** n_payments
            denominator = (1 + monthly_rate) ** n_payments - 1
            
            if abs(denominator) < 1e-10:  # Prevent division by zero
                return principal / n_payments
                
            payment = principal * (numerator / denominator)
            return max(0, payment)
            
        except OverflowError:  # Handle very large exponents
            raise ValueError("Interest rate or term too high for calculation")
            
    except Exception as e:
        print(f"Mortgage payment calculation error: principal={principal}, " +
              f"annual_rate={annual_rate}, years={years}")
        raise ValueError(str(e))

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
    try:
        if years_elapsed <= 0:
            return principal, 0.0
            
        if principal <= 0:
            return 0.0, 0.0
            
        if payment <= 0:
            return principal, 0.0
            
        if annual_rate < 0:
            raise ValueError("Interest rate cannot be negative")
            
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
            remaining = max(0, remaining - principal_part)  # Prevent negative remaining
        
        return remaining, total_interest
        
    except Exception as e:
        print(f"Mortgage calculation error: principal={principal}, " +
              f"payment={payment}, rate={annual_rate}, " +
              f"years={years_elapsed}")
        raise ValueError(str(e))

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
    try:
        if years <= 0:
            return 0.0
            
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
            monthly_investment = max(0, monthly_disposable - monthly_housing)
            
            # Add and grow this year's monthly investments
            for month in range(12):
                # Add this month's investment
                total_value += monthly_investment
                # Grow total for one month
                total_value *= (1 + monthly_rate)
        
        return max(0, total_value)
        
    except Exception as e:
        print(f"Monthly investment calculation error: " +
              f"disposable={initial_monthly_disposable}, " +
              f"housing={initial_monthly_housing_cost}, " +
              f"years={years}, return={investment_return}, " +
              f"cpi={cpi}, fixed={is_fixed_housing_cost}")
        raise ValueError(str(e))

def calculate_rent_scenario(inputs: ScenarioInputs) -> ScenarioResults:
    """Calculate results for rent and invest scenario."""
    try:
        # Calculate growth of initial savings (principal only)
        principal_growth = calculate_future_value_principal(
            principal=max(0, inputs.initial_savings),
            years=inputs.time_horizon_years,
            annual_rate=inputs.investment_return
        )
        
        # Calculate investment growth from monthly contributions
        total_investment = calculate_future_value_monthly_investment(
            initial_monthly_disposable=max(0, inputs.monthly_disposable_income),
            initial_monthly_housing_cost=max(0, inputs.monthly_rent),
            years=max(1, inputs.time_horizon_years),
            investment_return=max(0, inputs.investment_return),
            cpi=max(0, inputs.cpi),
            is_fixed_housing_cost=False
        )
        
        # Calculate total rent paid with inflation
        total_rent = 0
        monthly_rent = max(0, inputs.monthly_rent)
        for year in range(inputs.time_horizon_years):
            total_rent += monthly_rent * 12
            monthly_rent *= (1 + inputs.cpi)
        
        return ScenarioResults(
            principal_investment_value=principal_growth,  # Growth of initial savings only
            monthly_investment_value=total_investment,  # Growth of monthly contributions
            house_value=0.0,
            remaining_mortgage=0.0,
            total_interest_paid=0.0,
            total_rent_paid=max(0, total_rent),
            monthly_mortgage_min=0.0,
            monthly_mortgage_max=0.0
        )
        
    except Exception as e:
        print(f"Rent scenario calculation error")
        raise ValueError(str(e))

def calculate_buy_scenario(inputs: ScenarioInputs, max_mortgage=True) -> ScenarioResults:
    """Calculate results for buying scenario."""
    try:
        # Calculate total purchase cost including fees
        total_house_cost = max(0, inputs.house_cost * (1 + cfg.HOUSE_PURCHASE_FEES_PERCENT))
        
        # Calculate mortgage amounts for both scenarios
        max_mortgage_amount = total_house_cost * (1 - inputs.min_down_payment_percent)
        min_mortgage_amount = min(total_house_cost - inputs.initial_savings, max_mortgage_amount)
        
        # Ensure non-negative mortgage amounts
        max_mortgage_amount = max(0, max_mortgage_amount)
        min_mortgage_amount = max(0, min_mortgage_amount)
        
        # Calculate monthly payments for both scenarios
        max_monthly_payment = calculate_mortgage_payment(
            principal=max_mortgage_amount,
            annual_rate=max(0, inputs.mortgage_rate),
            years=max(1, inputs.mortgage_term_years)
        )
        
        min_monthly_payment = calculate_mortgage_payment(
            principal=min_mortgage_amount,
            annual_rate=max(0, inputs.mortgage_rate),
            years=max(1, inputs.mortgage_term_years)
        )
        
        # Select current scenario's values
        mortgage_amount = max_mortgage_amount if max_mortgage else min_mortgage_amount
        monthly_payment = max_monthly_payment if max_mortgage else min_monthly_payment
        down_payment = min(inputs.initial_savings, total_house_cost - mortgage_amount)
        
        # Calculate remaining mortgage and total interest
        remaining_mortgage, total_interest = calculate_remaining_mortgage(
            principal=mortgage_amount,
            payment=monthly_payment,
            annual_rate=max(0, inputs.mortgage_rate),
            years_elapsed=min(inputs.time_horizon_years, inputs.mortgage_term_years)
        )
        
        # Calculate future house value (prevent negative growth)
        future_house_value = max(0, inputs.house_cost * (1 + inputs.house_inflation) ** inputs.time_horizon_years)
        
        # Calculate growth of remaining initial savings (after down payment)
        principal_growth = calculate_future_value_principal(
            principal=max(0, inputs.initial_savings - down_payment),
            years=inputs.time_horizon_years,
            annual_rate=inputs.investment_return
        )
        
        # Calculate investment growth from monthly contributions
        total_investment = calculate_future_value_monthly_investment(
            initial_monthly_disposable=max(0, inputs.monthly_disposable_income),
            initial_monthly_housing_cost=monthly_payment,
            years=max(1, inputs.time_horizon_years),
            investment_return=max(0, inputs.investment_return),
            cpi=max(0, inputs.cpi),
            is_fixed_housing_cost=True
        )
        
        return ScenarioResults(
            principal_investment_value=principal_growth,  # Growth of initial savings only
            monthly_investment_value=total_investment,  # Growth of monthly contributions
            house_value=future_house_value,
            remaining_mortgage=remaining_mortgage,
            total_interest_paid=total_interest,
            total_rent_paid=0.0,
            monthly_mortgage_min=min_monthly_payment,
            monthly_mortgage_max=max_monthly_payment
        )
        
    except Exception as e:
        print(f"Buy scenario calculation error: max_mortgage={max_mortgage}")
        raise ValueError(str(e))

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
            if scenario.final_investment_value < 0:
                raise ValueError(f"Negative investment value calculated in {name} scenario")
            if scenario.net_worth < -inputs.house_cost:
                raise ValueError(f"Unrealistic negative net worth calculated in {name} scenario")
        
        return {
            "rent": rent_scenario,
            "max_mortgage": max_mortgage_scenario,
            "min_mortgage": min_mortgage_scenario
        }
        
    except Exception as e:
        raise ValueError(f"Error calculating scenarios: {str(e)}")