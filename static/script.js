// Global chart instance
let netWorthChart = null;

// Format currency values
function formatCurrency(value) {
    return new Intl.NumberFormat('de-DE', {
        style: 'currency',
        currency: 'EUR',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(value);
}

// Create or update the chart
function updateChart(results) {
    const ctx = document.getElementById('netWorthChart').getContext('2d');
    
    // Prepare data
    const data = {
        labels: ['Rent + Invest', 'Max Mortgage', 'Min Mortgage'],
        datasets: [
            {
                label: 'Initial Investment Growth',
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
                label: 'Monthly Savings Growth',
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
            },
            {
                label: 'Remaining Mortgage',
                data: [
                    0,
                    -results.max_mortgage.remaining_mortgage,
                    -results.min_mortgage.remaining_mortgage
                ],
                backgroundColor: 'rgba(231, 76, 60, 0.5)',
                borderColor: 'rgba(231, 76, 60, 1)',
                borderWidth: 1
            }
        ]
    };
    
    const options = {
        responsive: true,
        maintainAspectRatio: false,
        layout: {
            padding: {
                top: 20,
                right: 20,
                bottom: 20,
                left: 20
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    callback: function(value) {
                        return formatCurrency(value);
                    }
                },
                stacked: true
            },
            x: {
                grid: {
                    display: false
                },
                stacked: true
            }
        },
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    padding: 20,
                    boxWidth: 15
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
                    <td>Initial Investment Growth</td>
                    <td>${formatCurrency(results.rent.principal_investment_value)}</td>
                    <td>${formatCurrency(results.max_mortgage.principal_investment_value)}</td>
                    <td>${formatCurrency(results.min_mortgage.principal_investment_value)}</td>
                </tr>
                <tr>
                    <td>Monthly Savings Growth</td>
                    <td>${formatCurrency(results.rent.monthly_investment_value)}</td>
                    <td>${formatCurrency(results.max_mortgage.monthly_investment_value)}</td>
                    <td>${formatCurrency(results.min_mortgage.monthly_investment_value)}</td>
                </tr>
                <tr>
                    <td>Total Investment Value</td>
                    <td>${formatCurrency(results.rent.final_investment_value)}</td>
                    <td>${formatCurrency(results.max_mortgage.final_investment_value)}</td>
                    <td>${formatCurrency(results.min_mortgage.final_investment_value)}</td>
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
                    <td>${formatCurrency(results.max_mortgage.remaining_mortgage)}</td>
                    <td>${formatCurrency(results.min_mortgage.remaining_mortgage)}</td>
                </tr>
                <tr>
                    <td>Total Interest Paid</td>
                    <td>-</td>
                    <td>${formatCurrency(results.max_mortgage.total_interest_paid)}</td>
                    <td>${formatCurrency(results.min_mortgage.total_interest_paid)}</td>
                </tr>
                <tr>
                    <td>Total Rent Paid</td>
                    <td>${formatCurrency(results.rent.total_rent_paid)}</td>
                    <td>-</td>
                    <td>-</td>
                </tr>
                <tr class="table-primary">
                    <th>Net Worth</th>
                    <td>${formatCurrency(results.rent.net_worth)}</td>
                    <td>${formatCurrency(results.max_mortgage.net_worth)}</td>
                    <td>${formatCurrency(results.min_mortgage.net_worth)}</td>
                </tr>
            </tbody>
        </table>
    `;
    
    document.getElementById('resultsTable').innerHTML = tableHtml;
}

// Handle form submission
document.getElementById('calculatorForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Show loading spinner
    document.getElementById('loadingSpinner').style.display = 'block';
    document.getElementById('resultsArea').style.display = 'none';
    
    // Prepare form data
    const formData = {
        initial_savings: parseFloat(document.getElementById('initial_savings').value),
        house_cost: parseFloat(document.getElementById('house_cost').value),
        monthly_rent: parseFloat(document.getElementById('monthly_rent').value),
        monthly_mortgage_max: parseFloat(document.getElementById('monthly_mortgage_max').value),
        monthly_mortgage_min: parseFloat(document.getElementById('monthly_mortgage_min').value),
        monthly_disposable: parseFloat(document.getElementById('monthly_disposable').value),
        time_horizon: parseInt(document.getElementById('time_horizon').value),
        mortgage_term: parseInt(document.getElementById('mortgage_term').value),
        rent_inflation: parseFloat(document.getElementById('rent_inflation').value) / 100,
        house_inflation: parseFloat(document.getElementById('house_inflation').value) / 100,
        investment_return: parseFloat(document.getElementById('investment_return').value) / 100,
        mortgage_rate: parseFloat(document.getElementById('mortgage_rate').value) / 100
    };
    
    try {
        // Send calculation request
        const response = await fetch('/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Update results visualization
            updateChart(data.results);
            updateResultsTable(data.results);
            
            // Show results
            document.getElementById('resultsArea').style.display = 'block';
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        alert('Error calculating results: ' + error.message);
    } finally {
        // Hide loading spinner
        document.getElementById('loadingSpinner').style.display = 'none';
    }
}); 