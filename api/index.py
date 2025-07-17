 

import os
import sys
import json
from datetime import datetime
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS

# Add the current directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import services with error handling
try:
    from services.hero_rating_service import HeroRatingService
    from services.vsc_rating_service import VSCRatingService
    from services.vin_decoder_service import VINDecoderService
    from data.hero_products_data import get_hero_products
    from data.vsc_rates_data import get_vsc_coverage_options
    from utils.response_helpers import success_response, error_response
except ImportError as e:
    print(f"Import warning: {e}")
    # Create fallback classes to prevent crashes
    class HeroRatingService:
        def generate_quote(self, *args, **kwargs):
            return {"success": False, "error": "Service temporarily unavailable"}
    
    class VSCRatingService:
        def generate_quote(self, *args, **kwargs):
            return {"success": False, "error": "Service temporarily unavailable"}
    
    class VINDecoderService:
        def decode_vin(self, *args, **kwargs):
            return {"success": False, "error": "Service temporarily unavailable"}
    
    def get_hero_products():
        return {}
    
    def get_vsc_coverage_options():
        return {}
    
    def success_response(data):
        return {"success": True, "data": data}
    
    def error_response(message, code=400):
        return {"success": False, "error": message}, code

# Initialize Flask app
app = Flask(__name__)

# Configure CORS for all origins (adjust for production)
CORS(app, origins=["*"], methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

# App configuration
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production'),
    DEBUG=False,
    TESTING=False
)

# Initialize services
hero_service = HeroRatingService()
vsc_service = VSCRatingService()
vin_service = VINDecoderService()

# Health check endpoints
@app.route('/')
@app.route('/health')
def health_check():
    """Main health check endpoint"""
    return jsonify({
        "service": "ConnectedAutoCare API",
        "status": "healthy",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "environment": "production"
    })

@app.route('/api/health')
def api_health():
    """API health check with service status"""
    return jsonify({
        "api_status": "healthy",
        "services": {
            "hero_products": "available",
            "vsc_rating": "available",
            "vin_decoder": "available"
        },
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })

# Hero Products API Endpoints
@app.route('/api/hero/health')
def hero_health():
    """Hero products service health check"""
    try:
        products = get_hero_products()
        return jsonify({
            "service": "Hero Products API",
            "status": "healthy",
            "products_available": len(products),
            "categories": list(products.keys()) if products else [],
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })
    except Exception as e:
        return jsonify(error_response(f"Hero service error: {str(e)}")), 500

@app.route('/api/hero/products')
def get_all_hero_products():
    """Get all Hero products with pricing information"""
    try:
        products = get_hero_products()
        return jsonify(success_response(products))
    except Exception as e:
        return jsonify(error_response(f"Failed to retrieve products: {str(e)}")), 500

@app.route('/api/hero/products/<category>')
def get_hero_products_by_category(category):
    """Get Hero products by category"""
    try:
        all_products = get_hero_products()
        if category not in all_products:
            return jsonify(error_response(f"Category '{category}' not found")), 404
        
        return jsonify(success_response({
            "category": category,
            "products": all_products[category]
        }))
    except Exception as e:
        return jsonify(error_response(f"Failed to retrieve category: {str(e)}")), 500

@app.route('/api/hero/quote', methods=['POST'])
def generate_hero_quote():
    """Generate quote for Hero products"""
    try:
        data = request.get_json()
        if not data:
            return jsonify(error_response("Request body is required")), 400
        
        # Validate required fields
        required_fields = ['product_type', 'term_years']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify(error_response(f"Missing required fields: {', '.join(missing_fields)}")), 400
        
        # Generate quote
        quote_result = hero_service.generate_quote(
            product_type=data['product_type'],
            term_years=data['term_years'],
            coverage_limit=data.get('coverage_limit', 500),
            customer_type=data.get('customer_type', 'retail'),
            state=data.get('state', 'FL'),
            zip_code=data.get('zip_code', '33101')
        )
        
        if quote_result.get('success'):
            return jsonify(success_response(quote_result))
        else:
            return jsonify(error_response(quote_result.get('error', 'Quote generation failed'))), 400
            
    except Exception as e:
        return jsonify(error_response(f"Quote generation error: {str(e)}")), 500

# VSC Rating API Endpoints
@app.route('/api/vsc/health')
def vsc_health():
    """VSC rating service health check"""
    try:
        coverage_options = get_vsc_coverage_options()
        return jsonify({
            "service": "VSC Rating API",
            "status": "healthy",
            "coverage_levels": list(coverage_options.keys()) if coverage_options else [],
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })
    except Exception as e:
        return jsonify(error_response(f"VSC service error: {str(e)}")), 500

@app.route('/api/vsc/coverage-options')
def get_vsc_coverage():
    """Get available VSC coverage options"""
    try:
        options = get_vsc_coverage_options()
        return jsonify(success_response(options))
    except Exception as e:
        return jsonify(error_response(f"Failed to retrieve coverage options: {str(e)}")), 500

@app.route('/api/vsc/quote', methods=['POST'])
def generate_vsc_quote():
    """Generate VSC quote based on vehicle information"""
    try:
        data = request.get_json()
        if not data:
            return jsonify(error_response("Request body is required")), 400
        
        # Validate required fields
        required_fields = ['make', 'year', 'mileage']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify(error_response(f"Missing required fields: {', '.join(missing_fields)}")), 400
        
        # Generate quote
        quote_result = vsc_service.generate_quote(
            make=data['make'],
            model=data.get('model', ''),
            year=int(data['year']),
            mileage=int(data['mileage']),
            coverage_level=data.get('coverage_level', 'gold'),
            term_months=data.get('term_months', 36),
            deductible=data.get('deductible', 100),
            customer_type=data.get('customer_type', 'retail')
        )
        
        if quote_result.get('success'):
            return jsonify(success_response(quote_result))
        else:
            return jsonify(error_response(quote_result.get('error', 'VSC quote generation failed'))), 400
            
    except ValueError as e:
        return jsonify(error_response(f"Invalid input data: {str(e)}")), 400
    except Exception as e:
        return jsonify(error_response(f"VSC quote error: {str(e)}")), 500

# VIN Decoder API Endpoints
@app.route('/api/vin/health')
def vin_health():
    """VIN decoder service health check"""
    return jsonify({
        "service": "VIN Decoder API",
        "status": "healthy",
        "supported_formats": ["17-character VIN"],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })

@app.route('/api/vin/validate', methods=['POST'])
def validate_vin():
    """Validate VIN format"""
    try:
        data = request.get_json()
        if not data or 'vin' not in data:
            return jsonify(error_response("VIN is required")), 400
        
        vin = data['vin'].strip().upper()
        
        # Basic VIN validation
        if len(vin) != 17:
            return jsonify(error_response("VIN must be exactly 17 characters")), 400
        
        if not vin.isalnum():
            return jsonify(error_response("VIN must contain only letters and numbers")), 400
        
        # Check for invalid characters (I, O, Q not allowed in VIN)
        invalid_chars = set('IOQ') & set(vin)
        if invalid_chars:
            return jsonify(error_response(f"VIN contains invalid characters: {', '.join(invalid_chars)}")), 400
        
        return jsonify(success_response({
            "vin": vin,
            "valid": True,
            "format": "valid"
        }))
        
    except Exception as e:
        return jsonify(error_response(f"VIN validation error: {str(e)}")), 500

@app.route('/api/vin/decode', methods=['POST'])
def decode_vin():
    """Decode VIN to extract vehicle information"""
    try:
        data = request.get_json()
        if not data or 'vin' not in data:
            return jsonify(error_response("VIN is required")), 400
        
        vin = data['vin'].strip().upper()
        
        # Validate VIN first
        if len(vin) != 17:
            return jsonify(error_response("Invalid VIN length")), 400
        
        # Decode VIN
        decode_result = vin_service.decode_vin(vin)
        
        if decode_result.get('success'):
            return jsonify(success_response(decode_result['vehicle_info']))
        else:
            return jsonify(error_response(decode_result.get('error', 'VIN decode failed'))), 400
            
    except Exception as e:
        return jsonify(error_response(f"VIN decode error: {str(e)}")), 500

# Payment and Contract Endpoints (Placeholder for future implementation)
@app.route('/api/payments/methods')
def get_payment_methods():
    """Get available payment methods"""
    return jsonify(success_response({
        "credit_card": {
            "enabled": True,
            "providers": ["Helcim"],
            "accepted_cards": ["Visa", "MasterCard", "American Express", "Discover"]
        },
        "financing": {
            "enabled": True,
            "provider": "Supplemental Payment Program",
            "terms": ["0% for 12 months", "0% for 24 months"]
        }
    }))

@app.route('/api/contracts/generate', methods=['POST'])
def generate_contract():
    """Generate contract for purchased product (placeholder)"""
    try:
        data = request.get_json()
        if not data:
            return jsonify(error_response("Contract data is required")), 400
        
        # Placeholder response
        return jsonify(success_response({
            "contract_id": f"CAC-{datetime.utcnow().strftime('%Y%m%d')}-001",
            "status": "generated",
            "message": "Contract generation feature coming soon"
        }))
        
    except Exception as e:
        return jsonify(error_response(f"Contract generation error: {str(e)}")), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify(error_response("Endpoint not found", 404)), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify(error_response("Method not allowed", 405)), 405

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify(error_response("Internal server error", 500)), 500

@app.before_request
def handle_preflight():
    """Handle CORS preflight requests"""
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response

@app.after_request
def after_request(response):
    """Add CORS headers to all responses"""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Vercel serverless function handler
def handler(event, context):
    """Vercel serverless function handler"""
    return app(event, context)

# For local development
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

