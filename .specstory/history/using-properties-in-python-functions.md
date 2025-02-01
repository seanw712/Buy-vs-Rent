## SpecStory

## Using Properties in Python Functions (2/1/2025, 2:40:42 PM)

_**User**_

can I use a property in a function in this way?

---

_**Assistant**_

Yes, you can use a property in a function call just like any other attribute. Properties in Python are accessed like regular attributes, even though they're actually methods under the hood.

In your code, `monthly_disposable_income` is a property of the `ScenarioInputs` class:

```python:calculator.py
@property
def monthly_disposable_income(self) -> float:
    return self.monthly_savings_capacity + self.monthly_rent
```

When you use `inputs.monthly_disposable_income` in the function call, Python will automatically call this property method and return the calculated value. It works transparently just like accessing a regular attribute.

This is one of the benefits of using properties in Python - they allow you to define computed attributes that can be accessed with the same syntax as regular attributes, making your code cleaner and more intuitive to use.

---



---

