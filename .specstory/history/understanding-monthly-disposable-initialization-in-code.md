## SpecStory

## Understanding monthly_disposable Initialization in Code (2/1/2025, 2:39:33 PM)

_**User**_

Where is monthly_disposable initiated?

---

_**Assistant**_

Looking at the code, `monthly_disposable` is a local variable calculated within the `calculate_future_value_monthly_investment` function. It's calculated each year in the loop using the input parameter `initial_monthly_disposable`.

Here's the relevant function signature and context:

```python:calculator.py
def calculate_future_value_monthly_investment(
    initial_monthly_disposable: float,  # This is the input parameter
    initial_monthly_housing_cost: float,
    years: int,
    investment_return: float,
    cpi: float,
    is_fixed_housing_cost: bool = False
) -> float:
    # ... existing code ...
    
    # Year by year calculation
    for year in range(years):
        # Calculate this year's monthly disposable income (adjusted for CPI)
        monthly_disposable = initial_monthly_disposable * (1 + cpi) ** year
        # ... rest of the function ...
```

The variable is properly initiated within the function scope, taking the input parameter `initial_monthly_disposable` and applying inflation (CPI) growth for each year in the calculation. It's not a class attribute or global variable, but rather a local calculation variable that gets recreated in each iteration of the loop.

---



---

