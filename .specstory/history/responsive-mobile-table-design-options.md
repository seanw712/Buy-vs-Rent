## SpecStory

## Responsive Mobile Table Design Options (2/17/2025, 5:52:57 AM)

_**User**_

The mobile table looks a bit squished but works fine in desktop, can you give me some options that keep the current formatting for desktop, but create intuitive cards for each of the rows (Growth of initial savings, growth of monthly savings etc. etc.) that are colour coded for the various scenarios. 

---

_**Assistant**_

I'll help you modify the CSS to create a responsive card-based layout for mobile while preserving the desktop table view. I'll first search for the relevant code.

---

_**Assistant**_



---

_**Assistant**_



Let me update the table structure to make the components bold and remove the 'Components' header. I'll edit the JavaScript file:

```javascript
function updateResultsTable(results) {
    const tableHtml = `
        <table class="table">
            <thead>
                <tr>
                    <th></th>
                    <th>Rent + Invest</th>
                    <th>Max. Mortgage + Invest</th>
                    <th>Min. Mortgage + Invest</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Growth of Initial Savings</strong></td>
                    <td class="text-end">${formatCurrency(results.rent.initial_savings_growth)}</td>
                    <td class="text-end">${formatCurrency(results.max_mortgage.initial_savings_growth)}</td>
                    <td class="text-end">${formatCurrency(results.min_mortgage.initial_savings_growth)}</td>
                </tr>
                <tr>
                    <td><strong>Growth of Monthly Savings</strong></td>
                    <td class="text-end">${formatCurrency(results.rent.monthly_savings_growth)}</td>
                    <td class="text-end">${formatCurrency(results.max_mortgage.monthly_savings_growth)}</td>
                    <td class="text-end">${formatCurrency(results.min_mortgage.monthly_savings_growth)}</td>
                </tr>
                <tr>
                    <td><strong>House Value</strong></td>
                    <td class="text-end">-</td>
                    <td class="text-end">${formatCurrency(results.max_mortgage.house_value)}</td>
                    <td class="text-end">${formatCurrency(results.min_mortgage.house_value)}</td>
                </tr>
                <tr class="table-primary">
                    <td><strong>Net Worth</strong></td>
                    <td class="text-end">${formatCurrency(results.rent.net_worth)}</td>
                    <td class="text-end">${formatCurrency(results.max_mortgage.net_worth)}</td>
                    <td class="text-end">${formatCurrency(results.min_mortgage.net_worth)}</td>
                </tr>
            </tbody>
        </table>
        
        <h5 class="mt-4">Additional Information</h5>
        <table class="table">
            <thead>
                <tr>
                    <th></th>
                    <th>Rent + Invest</th>
                    <th>Max. Mortgage + Invest</th>
                    <th>Min. Mortgage + Invest</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Total Interest + Purchase Costs</strong></td>
                    <td class="text-end">-</td>
                    <td class="text-end">${formatCurrency(results.max_mortgage.total_purchase_costs)}</td>
                    <td class="text-end">${formatCurrency(results.min_mortgage.total_purchase_costs)}</td>
                </tr>
                <tr>
                    <td><strong>Total Rent Costs</strong></td>
                    <td class="text-end">${formatCurrency(results.rent.total_rent_paid)}</td>
                    <td class="text-end">-</td>
                    <td class="text-end">-</td>
                </tr>
                <tr>
                    <td><strong>Monthly Housing Cost</strong></td>
                    <td class="text-end">${formatCurrency(results.rent.total_rent_paid / (getFormData().time_horizon_years * 12))}</td>
                    <td class="text-end">${formatCurrency(results.max_mortgage.monthly_mortgage_max)}</td>
                    <td class="text-end">${formatCurrency(results.min_mortgage.monthly_mortgage_min)}</td>
                </tr>
            </tbody>
        </table>
    `;
    
    document.getElementById('resultsTable').innerHTML = tableHtml;
}
```

Key changes made:
1. Removed the 'Component' header from both tables by changing `<th>Component</th>` to `<th></th>`
2. Added `<strong>` tags around all component names in both tables
3. Ensured consistent text alignment with `text-end` class for numerical values
4. Maintained the same table structure but with cleaner headers
5. Kept the "Additional Information" section header but made it more subtle with h5

Would you like me to make any other adjustments to the table formatting?

---

_**User**_

Can you fix the mobile view - the table doesn't show properly with the labels (column & row headers) as well as the values overly concentrated and condensed. The desktop view is fine and should not change.

---

_**Assistant**_

I'll update the mobile view to make it more readable while keeping the desktop view unchanged. I'll modify the CSS to create a better card-like view for mobile:

```css:static/style.css
/* Existing table styles remain the same */
.table {
    width: 100%;
    margin: 0;
    border-collapse: collapse;
    background: white;
    font-size: 0.9rem;
    table-layout: fixed;
}

/* Mobile-specific table styles */
@media (max-width: 768px) {
    .table {
        border: none;
        background: none;
    }

    .table thead {
        display: none; /* Hide table headers on mobile */
    }

    .table tbody tr {
        display: block;
        background: white;
        margin-bottom: 1.5rem;
        padding: 1.25rem;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-sm);
    }

    .table td {
        display: grid;
        grid-template-columns: 1fr;
        gap: 0.5rem;
        padding: 0.75rem 0;
        text-align: left;
        border: none;
        font-size: 0.95rem;
    }

    .table td:not(:last-child) {
        border-bottom: 1px solid #e5e7eb;
    }

    /* Style for the component name (first cell) */
    .table td:first-child {
        background: #f8f9fa;
        margin: -1.25rem -1.25rem 1rem -1.25rem;
        padding: 1rem 1.25rem;
        border-radius: var(--border-radius) var(--border-radius) 0 0;
        font-size: 1.1rem;
    }

    /* Create labels for each scenario */
    .table td:not(:first-child)::before {
        content: attr(data-label);
        font-weight: 600;
        color: var(--text-secondary);
        display: block;
        margin-bottom: 0.25rem;
    }

    /* Special styling for Net Worth row */
    .table tr.table-primary {
        background: #f5f3ff;
        border: 1px solid rgba(99, 102, 241, 0.2);
    }

    .table tr.table-primary td:first-child {
        background: #ebe9fe;
        color: #6366f1;
    }

    /* Adjust spacing for values */
    .table td.text-end {
        text-align: left;
        font-size: 1.1rem;
        color: var(--text-primary);
    }

    /* Additional Info table specific styles */
    .additional-info .table tbody tr {
        border: 1px solid #e5e7eb;
    }
}
```

Now I'll update the JavaScript to add the necessary data attributes for the mobile labels:

```javascript:static/style.css
function updateResultsTable(results) {
    const tableHtml = `
        <table class="table">
            <thead>
                <tr>
                    <th></th>
                    <th>Rent + Invest</th>
                    <th>Max. Mortgage + Invest</th>
                    <th>Min. Mortgage + Invest</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Growth of Initial Savings</strong></td>
                    <td class="text-end" data-label="Rent + Invest">${formatCurrency(results.rent.initial_savings_growth)}</td>
                    <td class="text-end" data-label="Max. Mortgage + Invest">${formatCurrency(results.max_mortgage.initial_savings_growth)}</td>
                    <td class="text-end" data-label="Min. Mortgage + Invest">${formatCurrency(results.min_mortgage.initial_savings_growth)}</td>
                </tr>
                <tr>
                    <td><strong>Growth of Monthly Savings</strong></td>
                    <td class="text-end" data-label="Rent + Invest">${formatCurrency(results.rent.monthly_savings_growth)}</td>
                    <td class="text-end" data-label="Max. Mortgage + Invest">${formatCurrency(results.max_mortgage.monthly_savings_growth)}</td>
                    <td class="text-end" data-label="Min. Mortgage + Invest">${formatCurrency(results.min_mortgage.monthly_savings_growth)}</td>
                </tr>
                <tr>
                    <td><strong>House Value</strong></td>
                    <td class="text-end" data-label="Rent + Invest">-</td>
                    <td class="text-end" data-label="Max. Mortgage + Invest">${formatCurrency(results.max_mortgage.house_value)}</td>
                    <td class="text-end" data-label="Min. Mortgage + Invest">${formatCurrency(results.min_mortgage.house_value)}</td>
                </tr>
                <tr class="table-primary">
                    <td><strong>Net Worth</strong></td>
                    <td class="text-end" data-label="Rent + Invest">${formatCurrency(results.rent.net_worth)}</td>
                    <td class="text-end" data-label="Max. Mortgage + Invest">${formatCurrency(results.max_mortgage.net_worth)}</td>
                    <td class="text-end" data-label="Min. Mortgage + Invest">${formatCurrency(results.min_mortgage.net_worth)}</td>
                </tr>
            </tbody>
        </table>
        
        <h5 class="mt-4">Additional Information</h5>
        <table class="table">
            <thead>
                <tr>
                    <th></th>
                    <th>Rent + Invest</th>
                    <th>Max. Mortgage + Invest</th>
                    <th>Min. Mortgage + Invest</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Total Interest + Purchase Costs</strong></td>
                    <td class="text-end" data-label="Rent + Invest">-</td>
                    <td class="text-end" data-label="Max. Mortgage + Invest">${formatCurrency(results.max_mortgage.total_purchase_costs)}</td>
                    <td class="text-end" data-label="Min. Mortgage + Invest">${formatCurrency(results.min_mortgage.total_purchase_costs)}</td>
                </tr>
                <tr>
                    <td><strong>Total Rent Costs</strong></td>
                    <td class="text-end" data-label="Rent + Invest">${formatCurrency(results.rent.total_rent_paid)}</td>
                    <td class="text-end" data-label="Max. Mortgage + Invest">-</td>
                    <td class="text-end" data-label="Min. Mortgage + Invest">-</td>
                </tr>
                <tr>
                    <td><strong>Monthly Housing Cost</strong></td>
                    <td class="text-end" data-label="Rent + Invest">${formatCurrency(results.rent.total_rent_paid / (getFormData().time_horizon_years * 12))}</td>
                    <td class="text-end" data-label="Max. Mortgage + Invest">${formatCurrency(results.max_mortgage.monthly_mortgage_max)}</td>
                    <td class="text-end" data-label="Min. Mortgage + Invest">${formatCurrency(results.min_mortgage.monthly_mortgage_min)}</td>
                </tr>
            </tbody>
        </table>
    `;
    
    document.getElementById('resultsTable').innerHTML = tableHtml;
}
```

These changes will:
1. Transform each row into a card on mobile
2. Show the component name as a header for each card
3. Display each scenario value with its label
4. Maintain proper spacing and readability
5. Keep the desktop view exactly as it is
6. Add subtle shadows and borders for better visual separation
7. Use larger font sizes for better readability on mobile
8. Maintain the special styling for the Net Worth row
9. Keep proper alignment and spacing for all elements

The mobile view will now show each row as a card with:
- Component name at the top
- Each scenario value clearly labeled
- Proper spacing between elements
- Better visual hierarchy
- Improved readability

Let me know if you'd like any adjustments to the mobile layout!

---

_**User**_

Now can you colour code them to ensure one can easily distinguish between the different scenarios. Also find a way to assign a colour to each scenario (a clear legenda for instance).

---

_**Assistant**_

I'll add color coding for each scenario and create a legend to make it easy to distinguish between them. I'll update the CSS to include this:

```css:static/style.css
/* Scenario Colors */
:root {
    /* Adding scenario-specific colors */
    --rent-color: #3b82f6;    /* Blue */
    --max-mortgage-color: #10b981; /* Green */
    --min-mortgage-color: #8b5cf6; /* Purple */
    
    /* Lighter versions for backgrounds */
    --rent-bg: #eff6ff;
    --max-mortgage-bg: #ecfdf5;
    --min-mortgage-bg: #f5f3ff;
}

/* Scenario Legend */
.scenario-legend {
    display: flex;
    gap: 1.5rem;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
}

.scenario-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.scenario-color {
    width: 1rem;
    height: 1rem;
    border-radius: 0.25rem;
}

.rent-color {
    background-color: var(--rent-color);
}

.max-mortgage-color {
    background-color: var(--max-mortgage-color);
}

.min-mortgage-color {
    background-color: var(--min-mortgage-color);
}

/* Table Column Colors */
.table th:nth-child(2),
.table td:nth-child(2) {
    color: var(--rent-color);
}

.table th:nth-child(3),
.table td:nth-child(3) {
    color: var(--max-mortgage-color);
}

.table th:nth-child(4),
.table td:nth-child(4) {
    color: var(--min-mortgage-color);
}

/* Mobile Card Colors */
@media (max-width: 768px) {
    .table tbody tr {
        border-left: 4px solid transparent;
    }
    
    .table td:not(:first-child)::before {
        color: var(--text-secondary);
    }
    
    /* Color coding for mobile cards */
    .table td[data-label="Rent + Invest"] {
        background-color: var(--rent-bg);
        color: var(--rent-color);
    }
    
    .table td[data-label="Max. Mortgage + Invest"] {
        background-color: var(--max-mortgage-bg);
        color: var(--max-mortgage-color);
    }
    
    .table td[data-label="Min. Mortgage + Invest"] {
        background-color: var(--min-mortgage-bg);
        color: var(--min-mortgage-color);
    }
    
    /* Special styling for Net Worth row maintained */
    .table tr.table-primary {
        border-color: var(--primary-gradient);
    }
}
```

And I'll update the JavaScript to add the legend above the results:

```javascript
function updateResultsTable(results) {
    const legendHtml = `
        <div class="scenario-legend">
            <div class="scenario-item">
                <div class="scenario-color rent-color"></div>
                <span>Rent + Invest</span>
            </div>
            <div class="scenario-item">
                <div class="scenario-color max-mortgage-color"></div>
                <span>Max. Mortgage + Invest</span>
            </div>
            <div class="scenario-item">
                <div class="scenario-color min-mortgage-color"></div>
                <span>Min. Mortgage + Invest</span>
            </div>
        </div>
    `;

    const tableHtml = `
        ${legendHtml}
        <table class="table">
        // ... rest of your existing table HTML ...
    `;
    
    document.getElementById('resultsTable').innerHTML = tableHtml;
}
```

These changes will:

1. Add a clear color scheme for each scenario:
   - Rent + Invest: Blue
   - Max Mortgage + Invest: Green
   - Min Mortgage + Invest: Purple

2. Add a legend at the top of the results showing the color coding

3. For desktop view:
   - Color code the numbers in each column according to their scenario
   - Maintain readability with appropriate contrast

4. For mobile view:
   - Add subtle background colors to each scenario's card section
   - Maintain the special styling for the Net Worth row
   - Use lighter background colors for better readability

5. Keep the existing card structure but add color indicators to make it easier to track scenarios

The colors are chosen to be:
- Visually distinct from each other
- Professional and modern looking
- Accessible (good contrast)
- Consistent with the existing design

Would you like me to adjust any of the colors or make other changes to the visual hierarchy?

---

_**User**_

can you check whether the function update results table is added properly

---

_**Assistant**_

Looking at the code, I notice there are multiple definitions of the `updateResultsTable` function in the JavaScript file. Let me help you consolidate them into a single, correct version that includes both the legend and the color-coded tables:

```javascript:static/script.js
function updateResultsTable(results) {
    const legendHtml = `
        <div class="scenario-legend">
            <div class="scenario-item">
                <div class="scenario-color rent-color"></div>
                <span>Rent + Invest</span>
            </div>
            <div class="scenario-item">
                <div class="scenario-color max-mortgage-color"></div>
                <span>Max. Mortgage + Invest</span>
            </div>
            <div class="scenario-item">
                <div class="scenario-color min-mortgage-color"></div>
                <span>Min. Mortgage + Invest</span>
            </div>
        </div>
    `;

    const tableHtml = `
        ${legendHtml}
        <table class="table">
            <thead>
                <tr>
                    <th></th>
                    <th>Rent + Invest</th>
                    <th>Max. Mortgage + Invest</th>
                    <th>Min. Mortgage + Invest</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Growth of Initial Savings</strong></td>
                    <td class="text-end" data-label="Rent + Invest">${formatCurrency(results.rent.initial_savings_growth)}</td>
                    <td class="text-end" data-label="Max. Mortgage + Invest">${formatCurrency(results.max_mortgage.initial_savings_growth)}</td>
                    <td class="text-end" data-label="Min. Mortgage + Invest">${formatCurrency(results.min_mortgage.initial_savings_growth)}</td>
                </tr>
                <tr>
                    <td><strong>Growth of Monthly Savings</strong></td>
                    <td class="text-end" data-label="Rent + Invest">${formatCurrency(results.rent.monthly_savings_growth)}</td>
                    <td class="text-end" data-label="Max. Mortgage + Invest">${formatCurrency(results.max_mortgage.monthly_savings_growth)}</td>
                    <td class="text-end" data-label="Min. Mortgage + Invest">${formatCurrency(results.min_mortgage.monthly_savings_growth)}</td>
                </tr>
                <tr>
                    <td><strong>House Value</strong></td>
                    <td class="text-end" data-label="Rent + Invest">-</td>
                    <td class="text-end" data-label="Max. Mortgage + Invest">${formatCurrency(results.max_mortgage.house_value)}</td>
                    <td class="text-end" data-label="Min. Mortgage + Invest">${formatCurrency(results.min_mortgage.house_value)}</td>
                </tr>
                <tr class="table-primary">
                    <td><strong>Net Worth</strong></td>
                    <td class="text-end" data-label="Rent + Invest">${formatCurrency(results.rent.net_worth)}</td>
                    <td class="text-end" data-label="Max. Mortgage + Invest">${formatCurrency(results.max_mortgage.net_worth)}</td>
                    <td class="text-end" data-label="Min. Mortgage + Invest">${formatCurrency(results.min_mortgage.net_worth)}</td>
                </tr>
            </tbody>
        </table>
        
        <h5 class="mt-4">Additional Information</h5>
        <table class="table">
            <thead>
                <tr>
                    <th></th>
                    <th>Rent + Invest</th>
                    <th>Max. Mortgage + Invest</th>
                    <th>Min. Mortgage + Invest</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Total Interest + Purchase Costs</strong></td>
                    <td class="text-end" data-label="Rent + Invest">-</td>
                    <td class="text-end" data-label="Max. Mortgage + Invest">${formatCurrency(results.max_mortgage.total_purchase_costs)}</td>
                    <td class="text-end" data-label="Min. Mortgage + Invest">${formatCurrency(results.min_mortgage.total_purchase_costs)}</td>
                </tr>
                <tr>
                    <td><strong>Total Rent Costs</strong></td>
                    <td class="text-end" data-label="Rent + Invest">${formatCurrency(results.rent.total_rent_paid)}</td>
                    <td class="text-end" data-label="Max. Mortgage + Invest">-</td>
                    <td class="text-end" data-label="Min. Mortgage + Invest">-</td>
                </tr>
                <tr>
                    <td><strong>Monthly Housing Cost</strong></td>
                    <td class="text-end" data-label="Rent + Invest">${formatCurrency(results.rent.total_rent_paid / (getFormData().time_horizon_years * 12))}</td>
                    <td class="text-end" data-label="Max. Mortgage + Invest">${formatCurrency(results.max_mortgage.monthly_mortgage_max)}</td>
                    <td class="text-end" data-label="Min. Mortgage + Invest">${formatCurrency(results.min_mortgage.monthly_mortgage_min)}</td>
                </tr>
            </tbody>
        </table>
    `;
    
    document.getElementById('resultsTable').innerHTML = tableHtml;
}
```

The key changes in this consolidated version:

1. Added the legend at the top of the results
2. Added proper `data-label` attributes for mobile view
3. Made all component names bold with `<strong>` tags
4. Removed the 'Component' header from both tables
5. Ensured consistent column headers across both tables
6. Maintained color coding through CSS classes
7. Kept the special styling for the Net Worth row

You should replace all existing `updateResultsTable` functions in your JavaScript file with this single version. This will ensure:
1. Consistent styling across all tables
2. Proper color coding for all scenarios
3. Correct mobile view with labels
4. Legend display at the top of results

Would you like me to help you make this replacement in your JavaScript file?

---



---

