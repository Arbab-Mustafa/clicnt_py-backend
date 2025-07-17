#!/usr/bin/env python3
"""
Hero Products Data
Complete product catalog and pricing information for Hero protection products
"""

# Hero Products Pricing Configuration
HERO_PRODUCTS_PRICING = {
    'home_protection': {
        'base_price': 199,
        'multipliers': {
            1: 1.0,    # 1 year: $199
            2: 1.8,    # 2 years: $358
            3: 2.5,    # 3 years: $498
            4: 3.2,    # 4 years: $637
            5: 3.8     # 5 years: $756
        }
    },
    'auto_protection': {
        'base_price': 299,
        'multipliers': {
            1: 1.0,    # 1 year: $299
            2: 1.9,    # 2 years: $568
            3: 2.7,    # 3 years: $807
            4: 3.4,    # 4 years: $1,017
            5: 4.0     # 5 years: $1,196
        }
    },
    'deductible_reimbursement': {
        'base_price': 150,
        'multipliers': {
            1: 1.0,    # 1 year: $150
            2: 1.7,    # 2 years: $255
            3: 2.3     # 3 years: $345
        }
    }
}

# Complete Hero Products Catalog
HERO_PRODUCTS_CATALOG = {
    "home_protection": {
        "category_name": "Home Protection Plans",
        "category_description": "Comprehensive home protection with deductible reimbursement and emergency services",
        "products": [
            {
                "product_code": "HOME_PROTECTION_PLAN",
                "product_name": "Home Protection Plan",
                "short_description": "Complete home protection coverage",
                "detailed_description": "Comprehensive home protection plan including deductible reimbursement for covered claims, glass repair coverage, lockout assistance, and emergency services. Provides peace of mind for homeowners with 24/7 support and nationwide coverage.",
                "features": [
                    "Deductible reimbursement up to policy limits",
                    "Glass repair and replacement coverage",
                    "24/7 lockout assistance",
                    "Emergency plumbing and electrical services",
                    "HVAC emergency coverage",
                    "Identity theft restoration services",
                    "Warranty vault document storage"
                ],
                "coverage_limits": [500, 1000],
                "terms_available": [1, 2, 3, 4, 5],
                "base_price": 199,
                "price_range": {
                    "min_price": 199,
                    "max_price": 756
                }
            },
            {
                "product_code": "HOME_DEDUCTIBLE_REIMBURSEMENT",
                "product_name": "Home Deductible Reimbursement",
                "short_description": "Home insurance deductible coverage",
                "detailed_description": "Specialized coverage for home insurance deductibles with additional identity theft restoration and warranty vault services. Perfect for homeowners looking to reduce out-of-pocket expenses when filing insurance claims.",
                "features": [
                    "Home insurance deductible reimbursement",
                    "Identity theft restoration services",
                    "Warranty vault document storage",
                    "24/7 customer support",
                    "Fast claim processing",
                    "No waiting periods"
                ],
                "coverage_limits": [500, 1000],
                "terms_available": [1, 2, 3],
                "base_price": 160,
                "price_range": {
                    "min_price": 160,
                    "max_price": 368
                }
            },
            {
                "product_code": "HERO_LEVEL_HOME_PROTECTION",
                "product_name": "Hero-Level Protection for Your Home",
                "short_description": "Premium home protection package",
                "detailed_description": "Our most comprehensive home protection plan offering maximum coverage limits, premium services, and enhanced benefits. Designed for homeowners who want the ultimate protection and peace of mind.",
                "features": [
                    "Maximum deductible reimbursement coverage",
                    "Premium glass repair and replacement",
                    "Priority 24/7 emergency services",
                    "Enhanced HVAC and appliance coverage",
                    "Premium identity theft restoration",
                    "Concierge-level customer service",
                    "Extended warranty vault services",
                    "Home security system monitoring discounts"
                ],
                "coverage_limits": [1000, 2000],
                "terms_available": [1, 2, 3],
                "base_price": 789,
                "price_range": {
                    "min_price": 789,
                    "max_price": 1814
                }
            }
        ]
    },
    "auto_protection": {
        "category_name": "Auto Protection Plans",
        "category_description": "Complete automotive protection including deductible reimbursement and emergency services",
        "products": [
            {
                "product_code": "COMPREHENSIVE_AUTO_PROTECTION",
                "product_name": "Comprehensive Auto Protection",
                "short_description": "Complete automotive protection package",
                "detailed_description": "All-inclusive automotive protection plan covering deductible reimbursement, dent repair, emergency roadside assistance, and more. Designed to keep you protected and on the road with minimal out-of-pocket expenses.",
                "features": [
                    "Auto insurance deductible reimbursement",
                    "Paintless dent repair coverage",
                    "24/7 emergency roadside assistance",
                    "Towing and labor coverage",
                    "Rental car assistance",
                    "Key replacement services",
                    "Battery jump-start service",
                    "Flat tire assistance",
                    "Emergency fuel delivery"
                ],
                "coverage_limits": [500, 1000],
                "terms_available": [1, 2, 3, 4, 5],
                "base_price": 299,
                "price_range": {
                    "min_price": 299,
                    "max_price": 1196
                }
            }
        ]
    },
    "deductible_reimbursement": {
        "category_name": "Deductible Reimbursement Plans",
        "category_description": "Specialized deductible reimbursement coverage for various vehicle types",
        "products": [
            {
                "product_code": "AUTO_ADVANTAGE_DEDUCTIBLE_REIMBURSEMENT",
                "product_name": "Auto Advantage Deductible Reimbursement",
                "short_description": "Single vehicle deductible coverage",
                "detailed_description": "Targeted deductible reimbursement for a single vehicle with additional identity restoration and warranty vault services. Perfect for individual vehicle owners looking to minimize insurance claim costs.",
                "features": [
                    "Single VIN auto deductible reimbursement",
                    "Identity theft restoration services",
                    "Warranty vault document storage",
                    "Fast claim processing",
                    "24/7 customer support",
                    "No mileage restrictions"
                ],
                "coverage_limits": [500, 1000],
                "terms_available": [1, 2, 3],
                "base_price": 120,
                "price_range": {
                    "min_price": 120,
                    "max_price": 276
                }
            },
            {
                "product_code": "ALL_VEHICLE_DEDUCTIBLE_REIMBURSEMENT",
                "product_name": "All Vehicle Deductible Reimbursement",
                "short_description": "Multi-vehicle protection coverage",
                "detailed_description": "Comprehensive deductible reimbursement covering cars, motorcycles, ATVs, boats, and RVs. Ideal for families or individuals with multiple recreational vehicles who want complete protection.",
                "features": [
                    "Multi-vehicle coverage (cars, motorcycles, ATVs, boats, RVs)",
                    "Unlimited vehicle additions during term",
                    "Identity theft restoration services",
                    "Warranty vault document storage",
                    "Priority claim processing",
                    "24/7 customer support",
                    "Recreational vehicle specialist support"
                ],
                "coverage_limits": [500, 1000],
                "terms_available": [1, 2, 3],
                "base_price": 150,
                "price_range": {
                    "min_price": 150,
                    "max_price": 345
                }
            },
            {
                "product_code": "AUTO_RV_DEDUCTIBLE_REIMBURSEMENT",
                "product_name": "Auto & RV Deductible Reimbursement",
                "short_description": "Auto and RV specialized coverage",
                "detailed_description": "Specialized deductible reimbursement for both automobiles and recreational vehicles with enhanced benefits for RV owners including roadside assistance and emergency services.",
                "features": [
                    "Auto and RV deductible coverage",
                    "Enhanced RV emergency services",
                    "Specialized RV roadside assistance",
                    "Identity theft restoration services",
                    "Warranty vault document storage",
                    "RV-specific customer support",
                    "Campground directory access"
                ],
                "coverage_limits": [500, 1000],
                "terms_available": [1, 2, 3],
                "base_price": 175,
                "price_range": {
                    "min_price": 175,
                    "max_price": 403
                }
            },
            {
                "product_code": "MULTI_VEHICLE_DEDUCTIBLE_REIMBURSEMENT",
                "product_name": "Multi Vehicle Deductible Reimbursement",
                "short_description": "Multiple vehicle protection plan",
                "detailed_description": "Flexible deductible reimbursement plan covering multiple vehicles with the ability to add or remove vehicles during the coverage term. Perfect for growing families or changing vehicle needs.",
                "features": [
                    "Multiple vehicle protection",
                    "Flexible vehicle additions/removals",
                    "Comprehensive deductible reimbursement",
                    "Identity theft restoration services",
                    "Warranty vault document storage",
                    "Family-friendly customer support",
                    "Online account management"
                ],
                "coverage_limits": [500, 1000],
                "terms_available": [1, 2, 3],
                "base_price": 150,
                "price_range": {
                    "min_price": 150,
                    "max_price": 345
                }
            }
        ]
    }
}

def get_hero_products():
    """Get the complete Hero products catalog"""
    return HERO_PRODUCTS_CATALOG

def get_hero_product_by_code(product_code):
    """Get a specific Hero product by its product code"""
    for category in HERO_PRODUCTS_CATALOG.values():
        for product in category['products']:
            if product['product_code'] == product_code:
                return product
    return None

def get_hero_products_by_category(category):
    """Get Hero products for a specific category"""
    return HERO_PRODUCTS_CATALOG.get(category, {})

def get_hero_pricing():
    """Get Hero products pricing configuration"""
    return HERO_PRODUCTS_PRICING

def get_available_terms(product_type):
    """Get available terms for a specific product type"""
    if product_type in HERO_PRODUCTS_PRICING:
        return list(HERO_PRODUCTS_PRICING[product_type]['multipliers'].keys())
    return []

def calculate_hero_price(product_type, term_years, coverage_limit=500, customer_type='retail'):
    """
    Calculate Hero product price
    
    Args:
        product_type (str): Type of Hero product
        term_years (int): Coverage term in years
        coverage_limit (int): Coverage limit (500 or 1000)
        customer_type (str): 'retail' or 'wholesale'
        
    Returns:
        dict: Price calculation result
    """
    try:
        if product_type not in HERO_PRODUCTS_PRICING:
            return {'success': False, 'error': f'Unknown product type: {product_type}'}
        
        config = HERO_PRODUCTS_PRICING[product_type]
        
        if term_years not in config['multipliers']:
            return {'success': False, 'error': f'Invalid term: {term_years}'}
        
        base_price = config['base_price']
        term_multiplier = config['multipliers'][term_years]
        coverage_multiplier = 1.2 if coverage_limit == 1000 else 1.0
        
        subtotal = base_price * term_multiplier * coverage_multiplier
        
        if customer_type == 'wholesale':
            subtotal *= 0.85  # 15% wholesale discount
        
        return {
            'success': True,
            'base_price': base_price,
            'term_multiplier': term_multiplier,
            'coverage_multiplier': coverage_multiplier,
            'subtotal': round(subtotal, 2),
            'customer_type': customer_type
        }
        
    except Exception as e:
        return {'success': False, 'error': str(e)}

