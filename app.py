"""
Web interface for the house vs stocks calculator.
"""

from flask import Flask, render_template, request, jsonify
from calculator import ScenarioInputs, compare_scenarios
from dataclasses import asdict
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
        data = request.get_json()
        
        # Create inputs object matching calculator.py exactly
        inputs = ScenarioInputs(
            initial_savings=float(data['initial_savings']),
            house_cost=float(data['house_cost']),
            monthly_rent=float(data['monthly_rent']),
            monthly_disposable_income=float(data['monthly_disposable_income']),
            time_horizon_years=int(data['time_horizon_years']),
            mortgage_term_years=int(data['mortgage_term_years']),
            rent_inflation=float(data.get('rent_inflation', cfg.DEFAULT_RENT_INFLATION)),
            house_inflation=float(data.get('house_inflation', cfg.DEFAULT_HOUSE_PRICE_INFLATION)),
            investment_return=float(data.get('investment_return', cfg.DEFAULT_INVESTMENT_RETURN)),
            mortgage_rate=float(data.get('mortgage_rate', cfg.DEFAULT_MORTGAGE_RATE)),
            min_down_payment_percent=float(data.get('min_down_payment_percent', cfg.DEFAULT_MIN_DOWN_PAYMENT_PERCENT)),
            cpi=float(data.get('cpi', cfg.DEFAULT_CPI))
        )
        
        results = compare_scenarios(inputs)
        return jsonify({
            'rent': asdict(results['rent']),
            'min_mortgage': asdict(results['min_mortgage']),
            'max_mortgage': asdict(results['max_mortgage'])
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True) 