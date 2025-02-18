"""
Web interface for the house vs stocks calculator.
"""

from flask import Flask, render_template, request, jsonify, send_from_directory, make_response
from calculator import ScenarioInputs, compare_scenarios
from dataclasses import asdict
import config as cfg
import math
import os
from datetime import datetime

app = Flask(__name__)

def generate_sitemap():
    """Generate dynamic sitemap content."""
    base_url = "https://buyrentcalculator.app"
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Define all URLs with their properties
    urls = [
        {
            'loc': f"{base_url}/",
            'lastmod': current_date,
            'changefreq': 'daily',
            'priority': '1.0'
        },
        {
            'loc': f"{base_url}/terms",
            'lastmod': current_date,
            'changefreq': 'monthly',
            'priority': '0.8'
        },
        {
            'loc': f"{base_url}/privacy",
            'lastmod': current_date,
            'changefreq': 'monthly',
            'priority': '0.8'
        }
    ]
    
    # Generate XML content
    xml_content = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_content.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    for url in urls:
        xml_content.extend([
            '    <url>',
            f'        <loc>{url["loc"]}</loc>',
            f'        <lastmod>{url["lastmod"]}</lastmod>',
            f'        <changefreq>{url["changefreq"]}</changefreq>',
            f'        <priority>{url["priority"]}</priority>',
            '    </url>'
        ])
    
    xml_content.append('</urlset>')
    return '\n'.join(xml_content)

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
            monthly_savings_capacity=float(data['monthly_savings_capacity']),
            time_horizon_years=int(data['time_horizon_years']),
            mortgage_term_years=int(data['mortgage_term_years']),
            purchase_costs=float(data.get('house_purchase_fees_percent', cfg.DEFAULT_HOUSE_PURCHASE_FEES_PERCENT)),
            house_inflation=float(data.get('house_inflation', cfg.DEFAULT_HOUSE_PRICE_INFLATION)),
            investment_return=float(data.get('investment_return', cfg.DEFAULT_INVESTMENT_RETURN)),
            mortgage_rate=float(data.get('mortgage_rate', cfg.DEFAULT_MORTGAGE_RATE)),
            min_mortgage_rate=float(data.get('min_mortgage_rate', 0.025)),
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

@app.route('/robots.txt')
def serve_robots():
    """Serve the robots.txt file."""
    return send_from_directory(app.root_path, 'robots.txt')

@app.route('/sitemap.xml')
def serve_sitemap():
    """Serve the sitemap.xml file."""
    response = make_response(generate_sitemap())
    response.headers['Content-Type'] = 'application/xml'
    return response

if __name__ == '__main__':
    app.run(debug=True) 