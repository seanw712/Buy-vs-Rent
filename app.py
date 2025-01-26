"""
Web interface for the house vs stocks calculator.
"""

from flask import Flask, render_template, request, jsonify
from calculator import ScenarioInputs, compare_scenarios
import config as cfg
from dataclasses import asdict

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
        
        # Create inputs object with correct attribute names
        inputs = ScenarioInputs(
            initial_savings=float(data['initial_savings']),
            house_cost=float(data['house_cost']),
            monthly_rent=float(data['monthly_rent']),
            monthly_disposable_income=float(data['monthly_disposable_income']),
            time_horizon_years=int(data['time_horizon_years']),
            mortgage_term_years=int(data['mortgage_term_years']),
            rent_inflation=float(data['rent_inflation']),
            house_inflation=float(data['house_inflation']),
            investment_return=float(data['investment_return']),
            mortgage_rate=float(data['mortgage_rate']),
            min_down_payment_percent=float(data['min_down_payment_percent'])
        )

        # Calculate scenarios
        results = compare_scenarios(inputs)
        
        # Convert results to dict for JSON response
        response = {
            'rent': asdict(results['rent']),
            'min_mortgage': asdict(results['min_mortgage']),
            'max_mortgage': asdict(results['max_mortgage'])
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000) 