#!/usr/bin/env python3
"""
VSC (Vehicle Service Contract) Rating Service
Handles quote generation for vehicle service contracts using actual rate cards
"""

import os
import sys
from datetime import datetime

# Add parent directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

try:
    from data.vsc_rates_data import VSC_RATES, VEHICLE_CLASSIFICATION
except ImportError:
    # Fallback rate data
    VSC_RATES = {
        'A': {'silver': 800, 'gold': 1200, 'platinum': 1600},
        'B': {'silver': 1000, 'gold': 1500, 'platinum': 2000},
        'C': {'silver': 1400, 'gold': 2100, 'platinum': 2800}
    }
    VEHICLE_CLASSIFICATION = {
        'honda': 'A', 'toyota': 'A', 'nissan': 'A', 'hyundai': 'A',
        'ford': 'B', 'chevrolet': 'B', 'dodge': 'B', 'gmc': 'B',
        'bmw': 'C', 'mercedes': 'C', 'audi': 'C', 'cadillac': 'C'
    }

class VSCRatingService:
    """Service for generating VSC quotes based on actual rate cards"""
    
    def __init__(self):
        self.rates = VSC_RATES
        self.vehicle_classes = VEHICLE_CLASSIFICATION
        self.tax_rate = 0.07  # 7% tax rate
        self.admin_fee = 50.00  # VSC administrative fee
        
    def generate_quote(self, make, year, mileage, model='', coverage_level='gold', 
                      term_months=36, deductible=100, customer_type='retail', **kwargs):
        """
        Generate VSC quote based on vehicle information and coverage options
        
        Args:
            make (str): Vehicle make
            year (int): Vehicle year
            mileage (int): Current mileage
            model (str): Vehicle model (optional)
            coverage_level (str): silver, gold, or platinum
            term_months (int): Contract term in months
            deductible (int): Deductible amount
            customer_type (str): retail or wholesale
            
        Returns:
            dict: Comprehensive quote with pricing breakdown
        """
        try:
            # Normalize inputs
            make = make.lower().strip()
            year = int(year)
            mileage = int(mileage)
            coverage_level = coverage_level.lower().strip()
            term_months = int(term_months)
            
            # Validate inputs
            validation_errors = self._validate_inputs(make, year, mileage, coverage_level, term_months)
            if validation_errors:
                return {
                    'success': False,
                    'error': '; '.join(validation_errors)
                }
            
            # Determine vehicle class
            vehicle_class = self._get_vehicle_class(make)
            
            # Get base rate
            base_rate = self.rates[vehicle_class][coverage_level]
            
            # Apply adjustments
            age_factor = self._calculate_age_factor(year)
            mileage_factor = self._calculate_mileage_factor(mileage)
            term_factor = self._calculate_term_factor(term_months)
            deductible_factor = self._calculate_deductible_factor(deductible)
            
            # Calculate adjusted price
            adjusted_price = base_rate * age_factor * mileage_factor * term_factor * deductible_factor
            
            # Apply customer discount
            if customer_type == 'wholesale':
                adjusted_price *= 0.85  # 15% wholesale discount
            
            # Add administrative fee
            subtotal = adjusted_price + self.admin_fee
            
            # Calculate tax
            tax_amount = subtotal * self.tax_rate
            
            # Calculate total
            total_price = subtotal + tax_amount
            
            # Calculate payment options
            monthly_payment = total_price / term_months if term_months > 0 else total_price
            
            # Generate quote ID
            quote_id = f"VSC-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
            
            return {
                'success': True,
                'quote_id': quote_id,
                'vehicle_info': {
                    'make': make.title(),
                    'model': model.title() if model else 'Not Specified',
                    'year': year,
                    'mileage': mileage,
                    'vehicle_class': vehicle_class,
                    'age_years': datetime.now().year - year
                },
                'coverage_details': {
                    'level': coverage_level.title(),
                    'term_months': term_months,
                    'term_years': round(term_months / 12, 1),
                    'deductible': deductible,
                    'customer_type': customer_type
                },
                'pricing_breakdown': {
                    'base_rate': round(base_rate, 2),
                    'adjusted_price': round(adjusted_price, 2),
                    'admin_fee': round(self.admin_fee, 2),
                    'subtotal': round(subtotal, 2),
                    'tax_amount': round(tax_amount, 2),
                    'total_price': round(total_price, 2),
                    'monthly_payment': round(monthly_payment, 2)
                },
                'rating_factors': {
                    'age_factor': round(age_factor, 3),
                    'mileage_factor': round(mileage_factor, 3),
                    'term_factor': round(term_factor, 3),
                    'deductible_factor': round(deductible_factor, 3),
                    'customer_discount': 0.85 if customer_type == 'wholesale' else 1.0
                },
                'payment_options': {
                    'full_payment': round(total_price, 2),
                    'monthly_payment': round(monthly_payment, 2),
                    'financing_available': True,
                    'financing_terms': ['12 months 0% APR', '24 months 0% APR']
                },
                'quote_details': {
                    'timestamp': datetime.utcnow().isoformat() + 'Z',
                    'valid_until': self._calculate_expiry_date(),
                    'tax_rate': self.tax_rate,
                    'currency': 'USD'
                }
            }
            
        except ValueError as e:
            return {
                'success': False,
                'error': f'Invalid input data: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Quote generation failed: {str(e)}'
            }
    
    def _get_vehicle_class(self, make):
        """Determine vehicle class based on make"""
        make_lower = make.lower()
        
        # Check for exact match first
        if make_lower in self.vehicle_classes:
            return self.vehicle_classes[make_lower]
        
        # Check for partial matches
        for vehicle_make, vehicle_class in self.vehicle_classes.items():
            if vehicle_make in make_lower or make_lower in vehicle_make:
                return vehicle_class
        
        # Default to Class B if not found
        return 'B'
    
    def _calculate_age_factor(self, year):
        """Calculate age-based pricing factor"""
        current_year = datetime.now().year
        age = current_year - year
        
        if age <= 3:
            return 1.0
        elif age <= 6:
            return 1.15
        elif age <= 10:
            return 1.35
        else:
            return 1.60
    
    def _calculate_mileage_factor(self, mileage):
        """Calculate mileage-based pricing factor"""
        if mileage <= 50000:
            return 1.0
        elif mileage <= 75000:
            return 1.15
        elif mileage <= 100000:
            return 1.30
        elif mileage <= 125000:
            return 1.50
        else:
            return 1.75
    
    def _calculate_term_factor(self, term_months):
        """Calculate term-based pricing factor"""
        term_factors = {
            12: 0.40,
            24: 0.70,
            36: 1.00,
            48: 1.25,
            60: 1.45,
            72: 1.60
        }
        return term_factors.get(term_months, 1.0)
    
    def _calculate_deductible_factor(self, deductible):
        """Calculate deductible-based pricing factor"""
        deductible_factors = {
            0: 1.25,
            50: 1.15,
            100: 1.00,
            200: 0.90,
            500: 0.75,
            1000: 0.65
        }
        return deductible_factors.get(deductible, 1.0)
    
    def _validate_inputs(self, make, year, mileage, coverage_level, term_months):
        """Validate input parameters"""
        errors = []
        current_year = datetime.now().year
        
        if not make or len(make.strip()) < 2:
            errors.append("Vehicle make is required")
        
        if year < 1990 or year > current_year + 1:
            errors.append(f"Vehicle year must be between 1990 and {current_year + 1}")
        
        if mileage < 0 or mileage > 500000:
            errors.append("Mileage must be between 0 and 500,000")
        
        if coverage_level not in ['silver', 'gold', 'platinum']:
            errors.append("Coverage level must be silver, gold, or platinum")
        
        valid_terms = [12, 24, 36, 48, 60, 72]
        if term_months not in valid_terms:
            errors.append(f"Term must be one of: {valid_terms}")
        
        return errors
    
    def _calculate_expiry_date(self):
        """Calculate quote expiry date (30 days from now)"""
        from datetime import timedelta
        expiry = datetime.utcnow() + timedelta(days=30)
        return expiry.isoformat() + 'Z'
    
    def get_coverage_options(self):
        """Get available coverage options"""
        return {
            'coverage_levels': ['silver', 'gold', 'platinum'],
            'term_options': [12, 24, 36, 48, 60, 72],
            'deductible_options': [0, 50, 100, 200, 500, 1000],
            'vehicle_classes': list(set(self.vehicle_classes.values()))
        }
    
    def get_vehicle_class_info(self, make):
        """Get vehicle class information for a specific make"""
        vehicle_class = self._get_vehicle_class(make)
        return {
            'make': make.title(),
            'class': vehicle_class,
            'base_rates': self.rates[vehicle_class]
        }

