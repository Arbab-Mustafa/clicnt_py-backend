#!/usr/bin/env python3
"""
Hero Products Rating Service
Handles quote generation for all Hero protection products
"""

import os
import sys
from datetime import datetime

# Add parent directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

try:
    from data.hero_products_data import HERO_PRODUCTS_PRICING
except ImportError:
    # Fallback pricing data
    HERO_PRODUCTS_PRICING = {
        'home_protection': {'base_price': 199, 'multipliers': {1: 1.0, 2: 1.8, 3: 2.5, 4: 3.2, 5: 3.8}},
        'auto_protection': {'base_price': 299, 'multipliers': {1: 1.0, 2: 1.9, 3: 2.7, 4: 3.4, 5: 4.0}},
        'deductible_reimbursement': {'base_price': 150, 'multipliers': {1: 1.0, 2: 1.7, 3: 2.3}}
    }

class HeroRatingService:
    """Service for generating Hero product quotes"""
    
    def __init__(self):
        self.pricing_data = HERO_PRODUCTS_PRICING
        self.tax_rate = 0.07  # 7% tax rate (adjustable by state)
        self.admin_fee = 25.00  # Administrative fee
        
    def generate_quote(self, product_type, term_years, coverage_limit=500, 
                      customer_type='retail', state='FL', zip_code='33101', **kwargs):
        """
        Generate a comprehensive quote for Hero products
        
        Args:
            product_type (str): Type of Hero product
            term_years (int): Coverage term in years
            coverage_limit (int): Coverage limit (500 or 1000)
            customer_type (str): 'retail' or 'wholesale'
            state (str): State code for tax calculation
            zip_code (str): ZIP code for regional pricing
            
        Returns:
            dict: Quote result with pricing breakdown
        """
        try:
            # Validate product type
            if product_type not in self.pricing_data:
                return {
                    'success': False,
                    'error': f'Unknown product type: {product_type}. Available types: {list(self.pricing_data.keys())}'
                }
            
            product_config = self.pricing_data[product_type]
            
            # Validate term
            available_terms = list(product_config['multipliers'].keys())
            if term_years not in available_terms:
                return {
                    'success': False,
                    'error': f'Invalid term: {term_years}. Available terms: {available_terms}'
                }
            
            # Calculate base pricing
            base_price = product_config['base_price']
            term_multiplier = product_config['multipliers'][term_years]
            
            # Coverage limit adjustment
            coverage_multiplier = 1.2 if coverage_limit == 1000 else 1.0
            
            # State-based adjustments
            state_multiplier = self._get_state_multiplier(state)
            
            # Calculate subtotal
            subtotal = base_price * term_multiplier * coverage_multiplier * state_multiplier
            
            # Apply customer type discount
            if customer_type == 'wholesale':
                subtotal *= 0.85  # 15% wholesale discount
            
            # Add administrative fee
            subtotal_with_fee = subtotal + self.admin_fee
            
            # Calculate tax
            tax_amount = subtotal_with_fee * self.tax_rate
            
            # Calculate total
            total_price = subtotal_with_fee + tax_amount
            
            # Calculate payment options
            monthly_payment = total_price / (term_years * 12)
            
            # Generate quote ID
            quote_id = f"HERO-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
            
            return {
                'success': True,
                'quote_id': quote_id,
                'product_info': {
                    'type': product_type,
                    'term_years': term_years,
                    'coverage_limit': coverage_limit,
                    'customer_type': customer_type
                },
                'pricing': {
                    'base_price': round(base_price, 2),
                    'subtotal': round(subtotal, 2),
                    'admin_fee': round(self.admin_fee, 2),
                    'tax_amount': round(tax_amount, 2),
                    'total_price': round(total_price, 2),
                    'monthly_payment': round(monthly_payment, 2)
                },
                'multipliers_applied': {
                    'term': term_multiplier,
                    'coverage': coverage_multiplier,
                    'state': state_multiplier,
                    'customer_discount': 0.85 if customer_type == 'wholesale' else 1.0
                },
                'location': {
                    'state': state,
                    'zip_code': zip_code,
                    'tax_rate': self.tax_rate
                },
                'payment_options': {
                    'full_payment': round(total_price, 2),
                    'monthly_payment': round(monthly_payment, 2),
                    'financing_available': True
                },
                'quote_timestamp': datetime.utcnow().isoformat() + 'Z',
                'valid_until': self._calculate_expiry_date()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Quote generation failed: {str(e)}'
            }
    
    def _get_state_multiplier(self, state):
        """Get pricing multiplier based on state"""
        state_multipliers = {
            'FL': 1.0,   # Florida (base)
            'CA': 1.15,  # California
            'NY': 1.20,  # New York
            'TX': 1.05,  # Texas
            'IL': 1.10,  # Illinois
        }
        return state_multipliers.get(state.upper(), 1.0)
    
    def _calculate_expiry_date(self):
        """Calculate quote expiry date (30 days from now)"""
        from datetime import timedelta
        expiry = datetime.utcnow() + timedelta(days=30)
        return expiry.isoformat() + 'Z'
    
    def get_available_products(self):
        """Get list of available Hero products"""
        return list(self.pricing_data.keys())
    
    def get_product_terms(self, product_type):
        """Get available terms for a specific product"""
        if product_type in self.pricing_data:
            return list(self.pricing_data[product_type]['multipliers'].keys())
        return []
    
    def validate_quote_data(self, data):
        """Validate quote request data"""
        required_fields = ['product_type', 'term_years']
        errors = []
        
        for field in required_fields:
            if field not in data:
                errors.append(f'Missing required field: {field}')
        
        if 'product_type' in data and data['product_type'] not in self.pricing_data:
            errors.append(f'Invalid product type: {data["product_type"]}')
        
        if 'term_years' in data:
            try:
                term = int(data['term_years'])
                if 'product_type' in data and data['product_type'] in self.pricing_data:
                    available_terms = list(self.pricing_data[data['product_type']]['multipliers'].keys())
                    if term not in available_terms:
                        errors.append(f'Invalid term for {data["product_type"]}: {term}')
            except (ValueError, TypeError):
                errors.append('term_years must be a valid integer')
        
        return errors

