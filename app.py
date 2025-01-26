"""
Web interface for the house vs stocks calculator.
"""

from flask import Flask, render_template, request, jsonify
from calculator import ScenarioInputs, compare_scenarios
from dataclasses import asdict
import config as cfg
import math

app = Flask(__name__)

@app.route('/')
def index():
    """Serve the main calculator interface."""
    return render_template('index.html', config=cfg)

@app.route('/calculate', methods=['POST'])
def calculate():
    """Handle calculation requests and return results."""
    try:
        data = request.get_json()
        
        # Create inputs object matching calculator.py exactly
        inputs = ScenarioInputs(
            initial_savings=float(data['initial_savings']),
            house_cost=float(data['house_cost']),
            monthly_rent=float(data['monthly_rent']),
            monthly_disposable_income=float(data['monthly_disposable_income']),
            time_horizon_years=int(data['time_horizon_years']),
            mortgage_term_years=int(data['mortgage_term_years']),
            house_inflation=float(data.get('house_inflation', cfg.DEFAULT_HOUSE_PRICE_INFLATION)),
            investment_return=float(data.get('investment_return', cfg.DEFAULT_INVESTMENT_RETURN)),
            mortgage_rate=float(data.get('mortgage_rate', cfg.DEFAULT_MORTGAGE_RATE)),
            min_down_payment_percent=float(data.get('min_down_payment_percent', cfg.DEFAULT_MIN_DOWN_PAYMENT_PERCENT)),
            cpi=float(data.get('cpi', cfg.DEFAULT_CPI))
        )
        
        results = compare_scenarios(inputs)
        
        # Validate results before sending
        for scenario_name, scenario in results.items():
            if not hasattr(scenario, 'net_worth'):
                print(f"Missing net_worth in {scenario_name} scenario")
                scenario.net_worth = 0.0
            if not isinstance(scenario.net_worth, (int, float)) or math.isnan(scenario.net_worth) or math.isinf(scenario.net_worth):
                print(f"Invalid net_worth in {scenario_name} scenario: {scenario.net_worth}")
                scenario.net_worth = 0.0
        
        # Convert results to dict and explicitly include net_worth
        response_data = {
            'rent': {**asdict(results['rent']), 'net_worth': float(results['rent'].net_worth)},
            'min_mortgage': {**asdict(results['min_mortgage']), 'net_worth': float(results['min_mortgage'].net_worth)},
            'max_mortgage': {**asdict(results['max_mortgage']), 'net_worth': float(results['max_mortgage'].net_worth)}
        }
        
        # Debug log the response
        print("Response data:", response_data)
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Calculation error: {str(e)}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True) 