# ConnectedAutoCare.com Backend API

## Overview

This is the backend API server for ConnectedAutoCare.com, built with Python Flask and optimized for Vercel serverless deployment. The API provides comprehensive rating engines for Hero protection products and Vehicle Service Contracts (VSCs).

## Architecture d

### Serverless Design

- **Entry Point**: `api/index.py` serves as the main Flask application
- **Modular Services**: Separate rating engines for different product types
- **Static Data**: Rate cards and vehicle classification stored as Python modules
- **CORS Enabled**: Configured for cross-origin requests from frontend

### Key Components

#### Services (`api/services/`)

- `hero_rating_service.py` - Hero products rating engine
- `vsc_rating_service.py` - VSC rating and pricing calculations
- `vin_decoder_service.py` - Vehicle identification and validation

#### Data (`api/data/`)

- `hero_products_data.py` - Hero products catalog and pricing
- `vsc_rates_data.py` - VSC rate cards and vehicle classification
- `vehicle_data.py` - Vehicle makes, models, and classification

#### Utilities (`api/utils/`)

- `response_helpers.py` - Standardized API response formatting
- `validation.py` - Input validation and sanitization

## API Endpoints

### Health Check

```
GET /health
Response: {"status": "healthy", "message": "ConnectedAutoCare API is running"}
```

### Hero Products

#### Get All Products

```
GET /api/hero/products
Response: {
  "success": true,
  "data": [
    {
      "id": "home_protection",
      "name": "Home Protection Plan",
      "category": "home_protection",
      "description": "Comprehensive home protection coverage",
      "min_price": 199,
      "max_price": 569,
      "terms": [1, 2, 3, 4, 5]
    }
  ]
}
```

#### Generate Quote

```
POST /api/hero/quote
Content-Type: application/json

{
  "product_type": "home_protection",
  "term_years": 3,
  "coverage_limit": "1000",
  "customer_type": "retail"
}

Response: {
  "success": true,
  "data": {
    "product_name": "Home Protection Plan",
    "term_years": 3,
    "base_price": 399,
    "admin_fee": 25,
    "tax": 31.92,
    "total_price": 455.92,
    "monthly_payment": 12.66,
    "customer_type": "retail"
  }
}
```

### Vehicle Service Contracts

#### Generate VSC Quote

```
POST /api/vsc/quote
Content-Type: application/json

{
  "make": "Honda",
  "model": "Accord",
  "year": 2020,
  "mileage": 45000,
  "coverage_level": "gold",
  "term_months": 36,
  "customer_type": "retail"
}

Response: {
  "success": true,
  "data": {
    "vehicle_info": {
      "make": "Honda",
      "model": "Accord",
      "year": 2020,
      "class": "A"
    },
    "coverage_level": "gold",
    "term_months": 36,
    "base_price": 1850,
    "discount": 277.50,
    "total_price": 1572.50,
    "monthly_payment": 43.68,
    "customer_type": "retail"
  }
}
```

### VIN Decoder

#### Decode VIN

```
POST /api/vin/decode
Content-Type: application/json

{
  "vin": "1HGBH41JXMN109186"
}

Response: {
  "success": true,
  "data": {
    "vin": "1HGBH41JXMN109186",
    "make": "Honda",
    "model": "Accord",
    "year": 2021,
    "engine": "2.0L I4",
    "transmission": "CVT",
    "class": "A"
  }
}
```

## Local Development

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export FLASK_ENV=development
export FLASK_DEBUG=1

# Run the application
python api/index.py
```

### Testing

```bash
# Test health endpoint
curl http://localhost:5000/health

# Test Hero products
curl http://localhost:5000/api/hero/products

# Test quote generation
curl -X POST http://localhost:5000/api/hero/quote \
  -H "Content-Type: application/json" \
  -d '{"product_type":"home_protection","term_years":3,"coverage_limit":"1000","customer_type":"retail"}'
```

## Deployment

### Vercel Configuration

The `vercel.json` file configures the deployment:

```json
{
  "version": 2,
  "name": "connectedautocare-backend",
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ]
}
```

### Environment Variables

Set these in Vercel dashboard:

```
FLASK_ENV=production
PYTHON_VERSION=3.11
CORS_ORIGINS=https://your-frontend-domain.com
SECRET_KEY=your-secret-key-here
```

### Dependencies

The `requirements.txt` includes:

```
Flask==3.0.0
Flask-CORS==4.0.0
Werkzeug==3.0.1
requests==2.31.0
```

## Data Models

### Hero Products

```python
{
    "id": "product_identifier",
    "name": "Product Display Name",
    "category": "home_protection|auto_protection|deductible_reimbursement",
    "description": "Product description",
    "base_prices": {
        "1": 199,  # 1 year price
        "2": 299,  # 2 year price
        "3": 399   # 3 year price
    },
    "admin_fee": 25,
    "tax_rate": 0.08,
    "wholesale_discount": 0.15
}
```

### VSC Rates

```python
{
    "coverage_level": "silver|gold|platinum",
    "vehicle_class": "A|B|C",
    "term_months": 12,
    "mileage_limit": "15K|25K|50K|75K|100K|125K|Unlimited",
    "price": 1250
}
```

### Vehicle Classification

```python
{
    "class_a": [
        "Honda", "Toyota", "Nissan", "Hyundai", "Kia",
        "Lexus", "Mazda", "Mitsubishi", "Subaru"
    ],
    "class_b": [
        "Ford", "Chevrolet", "Buick", "Chrysler", "Dodge",
        "GMC", "Jeep", "Mercury", "Oldsmobile", "Plymouth",
        "Pontiac", "Saturn"
    ],
    "class_c": [
        "BMW", "Mercedes-Benz", "Audi", "Cadillac", "Lincoln",
        "Volkswagen", "Volvo"
    ]
}
```

## Error Handling

### Standard Error Response

```json
{
  "success": false,
  "error": "Error message description",
  "code": "ERROR_CODE",
  "details": {
    "field": "Additional error details"
  }
}
```

### Common Error Codes

- `INVALID_INPUT` - Missing or invalid request parameters
- `PRODUCT_NOT_FOUND` - Requested product does not exist
- `RATING_ERROR` - Error in pricing calculation
- `VIN_INVALID` - Invalid VIN format or checksum
- `VEHICLE_NOT_SUPPORTED` - Vehicle not eligible for coverage

## Performance

### Optimization Features

- **Cold Start Optimization**: Minimal imports and lazy loading
- **Caching**: Static data cached in memory
- **Efficient Calculations**: Optimized rating algorithms
- **Response Compression**: Automatic gzip compression

### Monitoring

- Vercel provides automatic function monitoring
- Response times typically under 200ms
- Automatic scaling based on demand
- Error tracking and alerting available

## Security

### CORS Configuration

```python
CORS(app, origins=[
    "https://connectedautocare.com",
    "https://www.connectedautocare.com",
    "https://your-frontend-domain.vercel.app"
])
```

### Input Validation

- All inputs validated and sanitized
- SQL injection prevention (though no database used)
- XSS protection through proper encoding
- Rate limiting recommended for production

## Troubleshooting

### Common Issues

**Issue**: Function timeout
**Solution**: Optimize imports and reduce cold start time

**Issue**: CORS errors
**Solution**: Verify CORS_ORIGINS environment variable

**Issue**: Import errors
**Solution**: Check requirements.txt and Python version

**Issue**: Rate calculation errors
**Solution**: Verify input data format and product configuration

### Debugging

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Add debug prints
print(f"Debug: {variable_name}")

# Check Vercel function logs
# Available in Vercel dashboard under Functions tab
```

## Contributing

### Code Style

- Follow PEP 8 Python style guidelines
- Use type hints where appropriate
- Add docstrings to all functions
- Keep functions focused and modular

### Testing

```python
# Add unit tests for new features
def test_hero_quote_generation():
    response = generate_hero_quote({
        "product_type": "home_protection",
        "term_years": 3,
        "coverage_limit": "1000",
        "customer_type": "retail"
    })
    assert response["success"] == True
    assert "total_price" in response["data"]
```

### Deployment

1. Test locally first
2. Commit changes to GitHub
3. Vercel automatically deploys
4. Monitor function logs for errors
5. Test production endpoints

---

**ConnectedAutoCare.com Backend** - Professional API for Protection Plans
