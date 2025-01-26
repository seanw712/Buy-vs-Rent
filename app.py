"""
Web interface for the house vs stocks calculator.
"""

from flask import Flask, render_template, request, jsonify
from calculator import ScenarioInputs, compare_scenarios
import config as cfg

app = Flask(__name__)

@app.route('/')
def index():
    """Serve the main calculator interface."""
    return render_template('index.html', config=cfg)

@app.route('/calculate', methods=['POST'])
def calculate():
    """Handle calculation requests and return results."""
    try:
        data = request.json
        
        # Create inputs object
        inputs = ScenarioInputs(
            initial_savings=float(data['initial_savings']),
            house_cost=float(data['house_cost']),
            monthly_rent=float(data['monthly_rent']),
            monthly_disposable_income=float(data['monthly_disposable']),
            time_horizon_years=int(data['time_horizon']),
            mortgage_term_years=int(data['mortgage_term']),
            rent_inflation=float(data['rent_inflation']),
            house_inflation=float(data['house_inflation']),
            investment_return=float(data['investment_return']),
            mortgage_rate=float(data['mortgage_rate']),
            min_down_payment_percent=float(data['min_down_payment_percent'])
        )
        
        # Calculate scenarios
        results = compare_scenarios(inputs)
        
        # Convert results to JSON-serializable format
        response = {
            scenario: {
                'principal_investment_value': result.principal_investment_value,
                'monthly_investment_value': result.monthly_investment_value,
                'final_investment_value': result.final_investment_value,
                'house_value': result.house_value,
                'remaining_mortgage': result.remaining_mortgage,
                'total_interest_paid': result.total_interest_paid,
                'total_rent_paid': result.total_rent_paid,
                'net_worth': result.net_worth
            }
            for scenario, result in results.items()
        }
        
        return jsonify({'success': True, 'results': response})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000) 