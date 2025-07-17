#!/usr/bin/env python3
"""
Response Helper Utilities
Standardized response formatting for API endpoints
"""

from datetime import datetime
from flask import jsonify

def success_response(data, message=None, status_code=200):
    """
    Create a standardized success response
    
    Args:
        data: Response data
        message (str): Optional success message
        status_code (int): HTTP status code
        
    Returns:
        tuple: (response_dict, status_code)
    """
    response = {
        'success': True,
        'data': data,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    
    if message:
        response['message'] = message
    
    return response, status_code

def error_response(message, status_code=400, error_code=None):
    """
    Create a standardized error response
    
    Args:
        message (str): Error message
        status_code (int): HTTP status code
        error_code (str): Optional error code
        
    Returns:
        tuple: (response_dict, status_code)
    """
    response = {
        'success': False,
        'error': message,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    
    if error_code:
        response['error_code'] = error_code
    
    return response, status_code

def validation_error_response(errors, status_code=400):
    """
    Create a validation error response
    
    Args:
        errors (list): List of validation errors
        status_code (int): HTTP status code
        
    Returns:
        tuple: (response_dict, status_code)
    """
    response = {
        'success': False,
        'error': 'Validation failed',
        'validation_errors': errors,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    
    return response, status_code

def paginated_response(data, page=1, per_page=10, total=None):
    """
    Create a paginated response
    
    Args:
        data: Response data
        page (int): Current page number
        per_page (int): Items per page
        total (int): Total number of items
        
    Returns:
        dict: Paginated response
    """
    response = {
        'success': True,
        'data': data,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total or len(data),
            'pages': (total // per_page) + (1 if total % per_page > 0 else 0) if total else 1
        },
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    
    return response

