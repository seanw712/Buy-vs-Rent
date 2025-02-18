// Global chart instance
let netWorthChart = null;

// Cache form data in localStorage
function saveFormDataToCache() {
    const formData = {};
    const inputs = document.querySelectorAll('#calculatorForm input[type="number"]');
    inputs.forEach(input => {
        formData[input.id] = input.value;
    });
    localStorage.setItem('calculatorFormData', JSON.stringify(formData));
}

// Load form data from cache
function loadFormDataFromCache() {
    const cachedData = localStorage.getItem('calculatorFormData');
    if (cachedData) {
        const formData = JSON.parse(cachedData);
        Object.entries(formData).forEach(([id, value]) => {
            const input = document.getElementById(id);
            if (input) {
                input.value = value;
            }
        });
    }
}

// Update net worth label with time horizon
function updateNetWorthLabel() {
    const timeHorizon = document.getElementById('time_horizon_years').value;
    const netWorthLabels = document.querySelectorAll('.net-worth-label');
    netWorthLabels.forEach(label => {
        label.textContent = `Net Worth after ${timeHorizon} years`;
    });
}

// Add event listeners for input changes
document.addEventListener('DOMContentLoaded', function() {
    // Load cached data when page loads
    loadFormDataFromCache();
    
    // Add change event listeners to all number inputs
    const inputs = document.querySelectorAll('#calculatorForm input[type="number"]');
    inputs.forEach(input => {
        input.addEventListener('change', saveFormDataToCache);
    });

    // Add specific listener for time horizon changes
    document.getElementById('time_horizon_years').addEventListener('change', updateNetWorthLabel);
    
    // Initial update of net worth label
    updateNetWorthLabel();
});

// Format currency values
function formatCurrency(value) {
    // Handle invalid values
    if (value === null || value === undefined || isNaN(value) || !isFinite(value)) {
        console.log(`Invalid currency value: ${value} (${typeof value})`);
        return '-';
    }
    // Ensure value is a number
    const numValue = Number(value);
    if (isNaN(numValue)) {
        console.log(`Could not convert to number: ${value} (${typeof value})`);
        return '-';
    }
    return new Intl.NumberFormat('de-DE', {
        style: 'currency',
        currency: 'EUR',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(numValue);
}

// Create or update the chart
function updateChart(results) {
    const ctx = document.getElementById('netWorthChart').getContext('2d');
    
    // Prepare data
    const data = {
        labels: ['Rent + Invest', 'Max. Mortgage + Invest', 'Min. Mortgage + Invest'],
        datasets: [
            {
                label: 'Growth of Initial Savings',
                data: [
                    results.rent.principal_investment_value,
                    results.max_mortgage.principal_investment_value,
                    results.min_mortgage.principal_investment_value
                ],
                backgroundColor: 'rgba(52, 152, 219, 0.5)',
                borderColor: 'rgba(52, 152, 219, 1)',
                borderWidth: 1
            },
            {
                label: 'Growth of Monthly Savings',
                data: [
                    results.rent.monthly_investment_value,
                    results.max_mortgage.monthly_investment_value,
                    results.min_mortgage.monthly_investment_value
                ],
                backgroundColor: 'rgba(46, 204, 113, 0.5)',
                borderColor: 'rgba(46, 204, 113, 1)',
                borderWidth: 1
            },
            {
                label: 'House Value',
                data: [
                    0,
                    results.max_mortgage.house_value,
                    results.min_mortgage.house_value
                ],
                backgroundColor: 'rgba(155, 89, 182, 0.5)',
                borderColor: 'rgba(155, 89, 182, 1)',
                borderWidth: 1
            }
        ]
    };
    
    const options = {
        responsive: true,
        maintainAspectRatio: false,
        layout: {
            padding: {
                top: window.innerWidth < 768 ? 5 : 10,
                right: window.innerWidth < 768 ? 5 : 10,
                bottom: window.innerWidth < 768 ? 25 : 10,
                left: window.innerWidth < 768 ? 5 : 10
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    callback: function(value) {
                        return formatCurrency(value);
                    },
                    maxTicksLimit: window.innerWidth < 768 ? 6 : 8,
                    font: {
                        size: window.innerWidth < 768 ? 9 : 12
                    }
                },
                stacked: true
            },
            x: {
                grid: {
                    display: false
                },
                stacked: true,
                ticks: {
                    font: {
                        size: window.innerWidth < 768 ? 9 : 12
                    }
                }
            }
        },
        plugins: {
            legend: {
                position: 'bottom',
                align: 'start',
                labels: {
                    padding: window.innerWidth < 768 ? 8 : 20,
                    boxWidth: window.innerWidth < 768 ? 8 : 15,
                    font: {
                        size: window.innerWidth < 768 ? 9 : 12
                    }
                }
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        return context.dataset.label + ': ' + formatCurrency(context.raw);
                    }
                }
            }
        }
    };
    
    // Destroy existing chart if it exists
    if (netWorthChart) {
        netWorthChart.destroy();
    }
    
    // Create new chart
    netWorthChart = new Chart(ctx, {
        type: 'bar',
        data: data,
        options: options
    });
}

// Create the results table
function updateResultsTable(results) {
    const tableHtml = `
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Component</th>
                    <th>Rent + Invest</th>
                    <th>Max Mortgage</th>
                    <th>Min Mortgage</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Growth of Initial Savings</td>
                    <td>${formatCurrency(results.rent.principal_investment_value)}</td>
                    <td>${formatCurrency(results.max_mortgage.principal_investment_value)}</td>
                    <td>${formatCurrency(results.min_mortgage.principal_investment_value)}</td>
                </tr>
                <tr>
                    <td>Growth of Monthly Savings</td>
                    <td>${formatCurrency(results.rent.monthly_investment_value)}</td>
                    <td>${formatCurrency(results.max_mortgage.monthly_investment_value)}</td>
                    <td>${formatCurrency(results.min_mortgage.monthly_investment_value)}</td>
                </tr>
                <tr>
                    <td>House Value</td>
                    <td>-</td>
                    <td>${formatCurrency(results.max_mortgage.house_value)}</td>
                    <td>${formatCurrency(results.min_mortgage.house_value)}</td>
                </tr>
                <tr>
                    <td>Remaining Mortgage</td>
                    <td>-</td>
                    <td>${formatCurrency(-results.max_mortgage.remaining_mortgage)}</td>
                    <td>${formatCurrency(-results.min_mortgage.remaining_mortgage)}</td>
                </tr>
                <tr class="table-primary">
                    <th>Net Worth</th>
                    <td>${formatCurrency(results.rent.net_worth)}</td>
                    <td>${formatCurrency(results.max_mortgage.net_worth)}</td>
                    <td>${formatCurrency(results.min_mortgage.net_worth)}</td>
                </tr>
            </tbody>
        </table>
        
        <h4 class="mt-4">Additional Information</h4>
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Component</th>
                    <th>Rent + Invest</th>
                    <th>Max Mortgage</th>
                    <th>Min Mortgage</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Total Interest + Purchase Costs</td>
                    <td>-</td>
                    <td>${formatCurrency(results.max_mortgage.total_purchase_costs)}</td>
                    <td>${formatCurrency(results.min_mortgage.total_purchase_costs)}</td>
                </tr>
                <tr>
                    <td>Total Rent Costs</td>
                    <td>${formatCurrency(results.rent.total_rent_paid)}</td>
                    <td>-</td>
                    <td>-</td>
                </tr>
                <tr>
                    <td>Monthly Housing Cost</td>
                    <td>${formatCurrency(results.rent.total_rent_paid / (getFormData().time_horizon_years * 12))}</td>
                    <td>${formatCurrency(results.max_mortgage.monthly_mortgage_max)}</td>
                    <td>${formatCurrency(results.min_mortgage.monthly_mortgage_min)}</td>
                </tr>
            </tbody>
        </table>
    `;
    
    document.getElementById('resultsTable').innerHTML = tableHtml;
}

// Get form data
function getFormData() {
    const formData = {
        initial_savings: parseFloat(document.getElementById('initial_savings').value),
        house_cost: parseFloat(document.getElementById('house_cost').value),
        monthly_rent: parseFloat(document.getElementById('monthly_rent').value),
        monthly_savings_capacity: parseFloat(document.getElementById('monthly_savings_capacity').value),
        time_horizon_years: parseInt(document.getElementById('time_horizon_years').value),
        mortgage_term_years: parseInt(document.getElementById('mortgage_term_years').value),
        min_down_payment_percent: parseFloat(document.getElementById('min_down_payment_percent').value) / 100,
        house_purchase_fees_percent: parseFloat(document.getElementById('house_purchase_fees_percent').value) / 100,
        house_inflation: parseFloat(document.getElementById('house_inflation').value) / 100,
        investment_return: parseFloat(document.getElementById('investment_return').value) / 100,
        mortgage_rate: parseFloat(document.getElementById('mortgage_rate').value) / 100,
        min_mortgage_rate: parseFloat(document.getElementById('min_mortgage_rate').value) / 100,
        cpi: parseFloat(document.getElementById('cpi').value) / 100
    };

    // Validate all values are numbers
    for (const [key, value] of Object.entries(formData)) {
        if (isNaN(value)) {
            console.error(`Invalid value for ${key}: ${value}`);
            throw new Error(`Please enter a valid number for ${key}`);
        }
    }

    return formData;
}

// Update results in the UI
function updateResults(results) {
    // Check if initial savings can cover the minimum down payment
    const formData = getFormData();
    const totalHouseCost = formData.house_cost * (1 + formData.house_purchase_fees_percent);
    const minDownPaymentRequired = totalHouseCost * formData.min_down_payment_percent;
    
    if (formData.initial_savings < minDownPaymentRequired) {
        const shortfall = formatCurrency(minDownPaymentRequired - formData.initial_savings);
        const message = `Error: Your initial savings are insufficient for the minimum down payment.

Required down payment: ${formatCurrency(minDownPaymentRequired)}
Your savings: ${formatCurrency(formData.initial_savings)}
Shortfall: ${shortfall}

To make this work, you could:
• Increase your initial savings
• Lower the house price
• Find a mortgage with a lower down payment requirement`;

        alert(message);
        document.getElementById('loadingSpinner').style.display = 'none';
        return;
    }

    // Check for negative monthly savings growth in mortgage scenarios
    if (results.max_mortgage.monthly_investment_value < 0 || results.min_mortgage.monthly_investment_value < 0) {
        const message = `Error: The mortgage payment would exceed your monthly savings capacity.

To make this work, you could:
• Lower the house price
• Extend the mortgage term
• Increase your down payment
• Find a lower mortgage interest rate`;

        alert(message);
        document.getElementById('loadingSpinner').style.display = 'none';
        return;
    }

    // Debug logging for net worth values
    console.log('Rent scenario:', {
        net_worth: results.rent.net_worth,
        principal: results.rent.principal_investment_value,
        monthly: results.rent.monthly_investment_value,
        house: results.rent.house_value,
        mortgage: results.rent.remaining_mortgage
    });
    console.log('Max mortgage scenario:', {
        net_worth: results.max_mortgage.net_worth,
        principal: results.max_mortgage.principal_investment_value,
        monthly: results.max_mortgage.monthly_investment_value,
        house: results.max_mortgage.house_value,
        mortgage: results.max_mortgage.remaining_mortgage
    });
    console.log('Min mortgage scenario:', {
        net_worth: results.min_mortgage.net_worth,
        principal: results.min_mortgage.principal_investment_value,
        monthly: results.min_mortgage.monthly_investment_value,
        house: results.min_mortgage.house_value,
        mortgage: results.min_mortgage.remaining_mortgage
    });
    
    // Show results area and hide loading spinner
    document.getElementById('resultsArea').style.display = 'block';
    document.getElementById('loadingSpinner').style.display = 'none';
    
    // Update net worth label
    updateNetWorthLabel();
    
    // Update Net Worth Summary Table and Mobile Cards
    const netWorthTable = document.querySelector('.net-worth-summary .table tbody');
    const timeHorizon = document.getElementById('time_horizon_years').value;
    const cpi = parseFloat(document.getElementById('cpi').value) / 100;
    
    // Calculate inflation adjustment factor
    const inflationFactor = 1 / Math.pow(1 + cpi, timeHorizon);
    
    // Update desktop table
    netWorthTable.innerHTML = `
        <tr>
            <td><strong>Growth of Initial Savings</strong></td>
            <td class="text-end">${formatCurrency(results.rent.principal_investment_value)}</td>
            <td class="text-end">${formatCurrency(results.max_mortgage.principal_investment_value)}</td>
            <td class="text-end">${formatCurrency(results.min_mortgage.principal_investment_value)}</td>
        </tr>
        <tr>
            <td><strong>Growth of Monthly Savings</strong></td>
            <td class="text-end">${formatCurrency(results.rent.monthly_investment_value)}</td>
            <td class="text-end">${formatCurrency(results.max_mortgage.monthly_investment_value)}</td>
            <td class="text-end">${formatCurrency(results.min_mortgage.monthly_investment_value)}</td>
        </tr>
        <tr>
            <td><strong>House Value</strong></td>
            <td class="text-end">-</td>
            <td class="text-end">${formatCurrency(results.max_mortgage.house_value)}</td>
            <td class="text-end">${formatCurrency(results.min_mortgage.house_value)}</td>
        </tr>
        <tr class="table-primary">
            <th><strong class="net-worth-label">Net Worth after ${timeHorizon} years</strong></th>
            <td class="text-end">${formatCurrency(results.rent.net_worth)}</td>
            <td class="text-end">${formatCurrency(results.max_mortgage.net_worth)}</td>
            <td class="text-end">${formatCurrency(results.min_mortgage.net_worth)}</td>
        </tr>
        <tr>
            <td><strong>(Adjusted for Inflation)</strong></td>
            <td class="text-end">${formatCurrency(results.rent.net_worth * inflationFactor)}</td>
            <td class="text-end">${formatCurrency(results.max_mortgage.net_worth * inflationFactor)}</td>
            <td class="text-end">${formatCurrency(results.min_mortgage.net_worth * inflationFactor)}</td>
        </tr>
    `;

    // Update mobile cards
    const mobileCards = document.querySelector('.mobile-cards');
    
    // Update Net Worth card
    const netWorthCard = mobileCards.querySelector('.result-card:nth-child(1)');
    const netWorthValues = netWorthCard.querySelectorAll('.result-card-value');
    netWorthValues[0].textContent = formatCurrency(results.rent.net_worth);
    netWorthValues[1].textContent = formatCurrency(results.max_mortgage.net_worth);
    netWorthValues[2].textContent = formatCurrency(results.min_mortgage.net_worth);

    // Update Inflation Adjusted card
    const inflationCard = mobileCards.querySelector('.result-card:nth-child(2)');
    const inflationValues = inflationCard.querySelectorAll('.result-card-value');
    inflationValues[0].textContent = formatCurrency(results.rent.net_worth * inflationFactor);
    inflationValues[1].textContent = formatCurrency(results.max_mortgage.net_worth * inflationFactor);
    inflationValues[2].textContent = formatCurrency(results.min_mortgage.net_worth * inflationFactor);

    // Update Initial Savings Growth card
    const initialSavingsCard = mobileCards.querySelector('.result-card:nth-child(3)');
    const initialSavingsValues = initialSavingsCard.querySelectorAll('.result-card-value');
    initialSavingsValues[0].textContent = formatCurrency(results.rent.principal_investment_value);
    initialSavingsValues[1].textContent = formatCurrency(results.max_mortgage.principal_investment_value);
    initialSavingsValues[2].textContent = formatCurrency(results.min_mortgage.principal_investment_value);

    // Update Monthly Savings Growth card
    const monthlySavingsCard = mobileCards.querySelector('.result-card:nth-child(4)');
    const monthlySavingsValues = monthlySavingsCard.querySelectorAll('.result-card-value');
    monthlySavingsValues[0].textContent = formatCurrency(results.rent.monthly_investment_value);
    monthlySavingsValues[1].textContent = formatCurrency(results.max_mortgage.monthly_investment_value);
    monthlySavingsValues[2].textContent = formatCurrency(results.min_mortgage.monthly_investment_value);

    // Update House Value card
    const houseValueCard = mobileCards.querySelector('.result-card:nth-child(5)');
    const houseValueValues = houseValueCard.querySelectorAll('.result-card-value');
    houseValueValues[0].textContent = '-';
    houseValueValues[1].textContent = formatCurrency(results.max_mortgage.house_value);
    houseValueValues[2].textContent = formatCurrency(results.min_mortgage.house_value);
    
    // Update Additional Information Table
    const additionalInfoTable = document.querySelector('.additional-info .table tbody');
    additionalInfoTable.innerHTML = `
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
    `;
    
    // Update chart
    updateChart(results);

    // Scroll to results section
    document.querySelector('.results-section').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Handle form submission
document.getElementById('calculatorForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    try {
        // Get form data
        const formData = getFormData();
        
        // Check if initial savings can cover the minimum down payment
        const totalHouseCost = formData.house_cost * (1 + formData.house_purchase_fees_percent);
        const minDownPaymentRequired = totalHouseCost * formData.min_down_payment_percent;
        
        if (formData.initial_savings < minDownPaymentRequired) {
            const shortfall = formatCurrency(minDownPaymentRequired - formData.initial_savings);
            const message = `Error: Your initial savings are insufficient for the minimum down payment.

Required down payment: ${formatCurrency(minDownPaymentRequired)}
Your savings: ${formatCurrency(formData.initial_savings)}
Shortfall: ${shortfall}

To make this work, you could:
• Increase your initial savings
• Lower the house price
• Find a mortgage with a lower down payment requirement`;

            alert(message);
            return;
        }
        
        // Show loading spinner and hide results
        document.getElementById('loadingSpinner').style.display = 'block';
        document.getElementById('resultsArea').style.display = 'none';
        
        // Debug log the form data
        console.log('Sending form data:', formData);
        
        // Send calculation request
        const response = await fetch('/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        // Log the raw response
        console.log('Raw response:', response);

        const results = await response.json();
        
        // Log the parsed results
        console.log('Parsed results:', results);

        if (results.error) {
            console.error('Server returned error:', results.error);
            alert('Calculation error: ' + results.error);
            document.getElementById('loadingSpinner').style.display = 'none';
            return;
        }

        // Update UI with results
        updateResults(results);
        
    } catch (error) {
        console.error('Detailed error:', error);
        console.error('Error stack:', error.stack);
        alert('An error occurred while calculating results. Please check the console for details.');
        document.getElementById('loadingSpinner').style.display = 'none';
    }
}); 