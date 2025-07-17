#!/usr/bin/env python3
"""
VSC (Vehicle Service Contract) Rates Data
Complete rate cards and vehicle classification for VSC pricing
"""

# Vehicle Classification System
VEHICLE_CLASSIFICATION = {
    # Class A - Most Reliable (Lowest Rates)
    'honda': 'A',
    'acura': 'A',
    'toyota': 'A',
    'lexus': 'A',
    'nissan': 'A',
    'infiniti': 'A',
    'hyundai': 'A',
    'kia': 'A',
    'mazda': 'A',
    'mitsubishi': 'A',
    'scion': 'A',
    'subaru': 'A',
    
    # Class B - Moderate Risk (Medium Rates)
    'buick': 'B',
    'chevrolet': 'B',
    'chrysler': 'B',
    'dodge': 'B',
    'ford': 'B',
    'gmc': 'B',
    'jeep': 'B',
    'mercury': 'B',
    'oldsmobile': 'B',
    'plymouth': 'B',
    'pontiac': 'B',
    'saturn': 'B',
    'ram': 'B',
    
    # Class C - Higher Risk (Highest Rates)
    'cadillac': 'C',
    'lincoln': 'C',
    'volkswagen': 'C',
    'volvo': 'C',
    'bmw': 'C',
    'mercedes-benz': 'C',
    'mercedes': 'C',
    'audi': 'C',
    'jaguar': 'C',
    'land rover': 'C',
    'porsche': 'C',
    'saab': 'C',
    'mini': 'C'
}

# VSC Base Rates by Vehicle Class and Coverage Level
VSC_RATES = {
    'A': {  # Class A - Most Reliable
        'silver': {
            'base_rate': 800,
            'description': 'Basic powertrain coverage'
        },
        'gold': {
            'base_rate': 1200,
            'description': 'Enhanced coverage including major components'
        },
        'platinum': {
            'base_rate': 1600,
            'description': 'Comprehensive coverage with exclusionary benefits'
        }
    },
    'B': {  # Class B - Moderate Risk
        'silver': {
            'base_rate': 1000,
            'description': 'Basic powertrain coverage'
        },
        'gold': {
            'base_rate': 1500,
            'description': 'Enhanced coverage including major components'
        },
        'platinum': {
            'base_rate': 2000,
            'description': 'Comprehensive coverage with exclusionary benefits'
        }
    },
    'C': {  # Class C - Higher Risk
        'silver': {
            'base_rate': 1400,
            'description': 'Basic powertrain coverage'
        },
        'gold': {
            'base_rate': 2100,
            'description': 'Enhanced coverage including major components'
        },
        'platinum': {
            'base_rate': 2800,
            'description': 'Comprehensive coverage with exclusionary benefits'
        }
    }
}

# Coverage Level Descriptions
COVERAGE_DESCRIPTIONS = {
    'silver': {
        'name': 'Silver Coverage',
        'description': 'Basic powertrain protection',
        'covered_components': [
            'Engine (internal lubricated parts)',
            'Transmission (internal parts)',
            'Drive axle assembly',
            'Transfer case (4WD vehicles)',
            'Seals and gaskets for covered components'
        ],
        'benefits': [
            '24/7 roadside assistance',
            'Towing coverage',
            'Rental car allowance',
            'Trip interruption coverage'
        ]
    },
    'gold': {
        'name': 'Gold Coverage',
        'description': 'Enhanced component protection',
        'covered_components': [
            'All Silver coverage components',
            'Air conditioning system',
            'Electrical system components',
            'Fuel system components',
            'Cooling system components',
            'Steering system components',
            'Brake system components (excluding pads/shoes)',
            'Suspension system components'
        ],
        'benefits': [
            'All Silver benefits',
            'Enhanced rental car allowance',
            'Extended trip interruption coverage',
            'Substitute transportation'
        ]
    },
    'platinum': {
        'name': 'Platinum Coverage',
        'description': 'Comprehensive exclusionary coverage',
        'covered_components': [
            'All vehicle components EXCEPT those specifically excluded',
            'Most comprehensive coverage available'
        ],
        'exclusions': [
            'Maintenance items (oil, filters, belts, hoses)',
            'Wear items (brake pads, wiper blades)',
            'Glass and body panels',
            'Interior and exterior trim'
        ],
        'benefits': [
            'All Gold benefits',
            'Maximum rental car allowance',
            'Comprehensive trip interruption coverage',
            'Emergency expense coverage',
            'Concierge services'
        ]
    }
}

# Term Options and Multipliers
TERM_MULTIPLIERS = {
    12: 0.40,   # 12 months
    24: 0.70,   # 24 months
    36: 1.00,   # 36 months (base)
    48: 1.25,   # 48 months
    60: 1.45,   # 60 months
    72: 1.60    # 72 months
}

# Deductible Options and Multipliers
DEDUCTIBLE_MULTIPLIERS = {
    0: 1.25,     # $0 deductible
    50: 1.15,    # $50 deductible
    100: 1.00,   # $100 deductible (base)
    200: 0.90,   # $200 deductible
    500: 0.75,   # $500 deductible
    1000: 0.65   # $1000 deductible
}

# Mileage Multipliers
MILEAGE_MULTIPLIERS = {
    'low': {'max': 50000, 'multiplier': 1.00},      # 0-50k miles
    'medium': {'max': 75000, 'multiplier': 1.15},   # 50k-75k miles
    'high': {'max': 100000, 'multiplier': 1.30},    # 75k-100k miles
    'very_high': {'max': 125000, 'multiplier': 1.50}, # 100k-125k miles
    'extreme': {'max': 999999, 'multiplier': 1.75}   # 125k+ miles
}

# Age Multipliers (based on vehicle age)
AGE_MULTIPLIERS = {
    'new': {'max_age': 3, 'multiplier': 1.00},       # 0-3 years
    'recent': {'max_age': 6, 'multiplier': 1.15},    # 4-6 years
    'older': {'max_age': 10, 'multiplier': 1.35},    # 7-10 years
    'old': {'max_age': 999, 'multiplier': 1.60}      # 11+ years
}

def get_vehicle_class(make):
    """
    Get vehicle class for a given make
    
    Args:
        make (str): Vehicle make
        
    Returns:
        str: Vehicle class (A, B, or C)
    """
    make_lower = make.lower().strip()
    
    # Direct lookup
    if make_lower in VEHICLE_CLASSIFICATION:
        return VEHICLE_CLASSIFICATION[make_lower]
    
    # Partial match for compound names
    for vehicle_make, vehicle_class in VEHICLE_CLASSIFICATION.items():
        if vehicle_make in make_lower or make_lower in vehicle_make:
            return vehicle_class
    
    # Default to Class B if not found
    return 'B'

def get_base_rate(vehicle_class, coverage_level):
    """
    Get base rate for vehicle class and coverage level
    
    Args:
        vehicle_class (str): Vehicle class (A, B, or C)
        coverage_level (str): Coverage level (silver, gold, platinum)
        
    Returns:
        int: Base rate
    """
    return VSC_RATES.get(vehicle_class, {}).get(coverage_level, {}).get('base_rate', 1500)

def get_mileage_multiplier(mileage):
    """
    Get mileage multiplier based on vehicle mileage
    
    Args:
        mileage (int): Vehicle mileage
        
    Returns:
        float: Mileage multiplier
    """
    for category, config in MILEAGE_MULTIPLIERS.items():
        if mileage <= config['max']:
            return config['multiplier']
    return MILEAGE_MULTIPLIERS['extreme']['multiplier']

def get_age_multiplier(vehicle_age):
    """
    Get age multiplier based on vehicle age
    
    Args:
        vehicle_age (int): Vehicle age in years
        
    Returns:
        float: Age multiplier
    """
    for category, config in AGE_MULTIPLIERS.items():
        if vehicle_age <= config['max_age']:
            return config['multiplier']
    return AGE_MULTIPLIERS['old']['multiplier']

def get_vsc_coverage_options():
    """
    Get all available VSC coverage options
    
    Returns:
        dict: Complete coverage options
    """
    return {
        'coverage_levels': {
            level: {
                'name': info['name'],
                'description': info['description'],
                'base_rates': {
                    vehicle_class: VSC_RATES[vehicle_class][level]['base_rate']
                    for vehicle_class in VSC_RATES.keys()
                }
            }
            for level, info in COVERAGE_DESCRIPTIONS.items()
        },
        'term_options': {
            'available_terms': list(TERM_MULTIPLIERS.keys()),
            'multipliers': TERM_MULTIPLIERS
        },
        'deductible_options': {
            'available_deductibles': list(DEDUCTIBLE_MULTIPLIERS.keys()),
            'multipliers': DEDUCTIBLE_MULTIPLIERS
        },
        'vehicle_classes': {
            vehicle_class: {
                'description': f'Class {vehicle_class} vehicles',
                'example_makes': [
                    make for make, cls in VEHICLE_CLASSIFICATION.items() 
                    if cls == vehicle_class
                ][:5]  # Show first 5 examples
            }
            for vehicle_class in VSC_RATES.keys()
        }
    }

def calculate_vsc_price(make, year, mileage, coverage_level='gold', term_months=36, 
                       deductible=100, customer_type='retail'):
    """
    Calculate VSC price based on all factors
    
    Args:
        make (str): Vehicle make
        year (int): Vehicle year
        mileage (int): Vehicle mileage
        coverage_level (str): Coverage level
        term_months (int): Contract term in months
        deductible (int): Deductible amount
        customer_type (str): Customer type (retail/wholesale)
        
    Returns:
        dict: Price calculation breakdown
    """
    try:
        from datetime import datetime
        
        # Get vehicle class
        vehicle_class = get_vehicle_class(make)
        
        # Get base rate
        base_rate = get_base_rate(vehicle_class, coverage_level)
        
        # Calculate multipliers
        vehicle_age = datetime.now().year - year
        age_multiplier = get_age_multiplier(vehicle_age)
        mileage_multiplier = get_mileage_multiplier(mileage)
        term_multiplier = TERM_MULTIPLIERS.get(term_months, 1.0)
        deductible_multiplier = DEDUCTIBLE_MULTIPLIERS.get(deductible, 1.0)
        
        # Calculate price
        calculated_price = (base_rate * age_multiplier * mileage_multiplier * 
                          term_multiplier * deductible_multiplier)
        
        # Apply customer discount
        if customer_type == 'wholesale':
            calculated_price *= 0.85  # 15% wholesale discount
        
        return {
            'success': True,
            'vehicle_class': vehicle_class,
            'base_rate': base_rate,
            'calculated_price': round(calculated_price, 2),
            'multipliers': {
                'age': age_multiplier,
                'mileage': mileage_multiplier,
                'term': term_multiplier,
                'deductible': deductible_multiplier,
                'customer_discount': 0.85 if customer_type == 'wholesale' else 1.0
            }
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

