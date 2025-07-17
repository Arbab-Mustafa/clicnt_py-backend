#!/usr/bin/env python3
"""
VIN Decoder Service
Handles VIN validation and decoding for vehicle information extraction
"""

import re
import requests
from datetime import datetime

class VINDecoderService:
    """Service for VIN validation and decoding"""
    
    def __init__(self):
        self.vin_pattern = re.compile(r'^[A-HJ-NPR-Z0-9]{17}$')
        
        # VIN position mappings for basic decoding
        self.wmi_mappings = {
            # World Manufacturer Identifier mappings (first 3 characters)
            '1HG': 'Honda',
            '1HT': 'Honda',
            '2HG': 'Honda',
            '3HG': 'Honda',
            '1G1': 'Chevrolet',
            '1G6': 'Cadillac',
            '1FA': 'Ford',
            '1FT': 'Ford',
            '1GC': 'Chevrolet',
            '1GM': 'Chevrolet',
            '2G1': 'Chevrolet',
            '3G1': 'Chevrolet',
            '4T1': 'Toyota',
            '4T3': 'Toyota',
            '5TD': 'Toyota',
            'JHM': 'Honda',
            'JTD': 'Toyota',
            'KMH': 'Hyundai',
            'WBA': 'BMW',
            'WBS': 'BMW',
            'WDD': 'Mercedes-Benz',
            'WDC': 'Mercedes-Benz',
        }
        
        # Model year mappings (10th position)
        self.year_mappings = {
            'A': 1980, 'B': 1981, 'C': 1982, 'D': 1983, 'E': 1984, 'F': 1985,
            'G': 1986, 'H': 1987, 'J': 1988, 'K': 1989, 'L': 1990, 'M': 1991,
            'N': 1992, 'P': 1993, 'R': 1994, 'S': 1995, 'T': 1996, 'V': 1997,
            'W': 1998, 'X': 1999, 'Y': 2000, '1': 2001, '2': 2002, '3': 2003,
            '4': 2004, '5': 2005, '6': 2006, '7': 2007, '8': 2008, '9': 2009,
            'A': 2010, 'B': 2011, 'C': 2012, 'D': 2013, 'E': 2014, 'F': 2015,
            'G': 2016, 'H': 2017, 'J': 2018, 'K': 2019, 'L': 2020, 'M': 2021,
            'N': 2022, 'P': 2023, 'R': 2024, 'S': 2025
        }
    
    def validate_vin(self, vin):
        """
        Validate VIN format and check digit
        
        Args:
            vin (str): VIN to validate
            
        Returns:
            dict: Validation result
        """
        try:
            vin = vin.strip().upper()
            
            # Check length
            if len(vin) != 17:
                return {
                    'success': False,
                    'valid': False,
                    'error': 'VIN must be exactly 17 characters'
                }
            
            # Check format (no I, O, Q allowed)
            if not self.vin_pattern.match(vin):
                return {
                    'success': False,
                    'valid': False,
                    'error': 'VIN contains invalid characters (I, O, Q not allowed)'
                }
            
            # Validate check digit (9th position)
            if not self._validate_check_digit(vin):
                return {
                    'success': False,
                    'valid': False,
                    'error': 'Invalid VIN check digit'
                }
            
            return {
                'success': True,
                'valid': True,
                'vin': vin,
                'message': 'VIN is valid'
            }
            
        except Exception as e:
            return {
                'success': False,
                'valid': False,
                'error': f'VIN validation error: {str(e)}'
            }
    
    def decode_vin(self, vin):
        """
        Decode VIN to extract vehicle information
        
        Args:
            vin (str): VIN to decode
            
        Returns:
            dict: Decoded vehicle information
        """
        try:
            # First validate the VIN
            validation_result = self.validate_vin(vin)
            if not validation_result.get('valid'):
                return validation_result
            
            vin = vin.strip().upper()
            
            # Extract basic information from VIN structure
            wmi = vin[:3]  # World Manufacturer Identifier
            vds = vin[3:9]  # Vehicle Descriptor Section
            vis = vin[9:]   # Vehicle Identifier Section
            
            # Decode manufacturer
            make = self._decode_manufacturer(wmi)
            
            # Decode model year
            year = self._decode_year(vin[9])
            
            # Decode plant code
            plant_code = vin[10]
            
            # For more detailed decoding, you would typically use an external API
            # For now, we'll provide basic information and attempt external lookup
            
            # Try external API for detailed information
            detailed_info = self._try_external_decode(vin)
            
            if detailed_info:
                return {
                    'success': True,
                    'vehicle_info': detailed_info,
                    'vin': vin,
                    'decode_method': 'external_api'
                }
            else:
                # Fallback to basic decoding
                return {
                    'success': True,
                    'vehicle_info': {
                        'vin': vin,
                        'make': make,
                        'year': year,
                        'model': 'Unknown',
                        'trim': 'Unknown',
                        'engine': 'Unknown',
                        'transmission': 'Unknown',
                        'body_style': 'Unknown',
                        'fuel_type': 'Unknown',
                        'plant_code': plant_code,
                        'wmi': wmi,
                        'note': 'Basic VIN decode - limited information available'
                    },
                    'decode_method': 'basic_structure'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'VIN decode error: {str(e)}'
            }
    
    def _validate_check_digit(self, vin):
        """Validate the VIN check digit (9th position)"""
        try:
            # VIN check digit calculation
            weights = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]
            transliteration = {
                'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8,
                'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'P': 7, 'R': 9,
                'S': 2, 'T': 3, 'U': 4, 'V': 5, 'W': 6, 'X': 7, 'Y': 8, 'Z': 9
            }
            
            sum_value = 0
            for i, char in enumerate(vin):
                if char.isdigit():
                    value = int(char)
                else:
                    value = transliteration.get(char, 0)
                sum_value += value * weights[i]
            
            remainder = sum_value % 11
            check_digit = 'X' if remainder == 10 else str(remainder)
            
            return vin[8] == check_digit
            
        except Exception:
            # If check digit validation fails, we'll still allow the VIN
            # as some older or international VINs may not follow this standard
            return True
    
    def _decode_manufacturer(self, wmi):
        """Decode manufacturer from WMI"""
        # Check exact match first
        if wmi in self.wmi_mappings:
            return self.wmi_mappings[wmi]
        
        # Check partial matches
        for key, value in self.wmi_mappings.items():
            if wmi.startswith(key[:2]):
                return value
        
        # Country/region based fallback
        if wmi[0] in '12345':
            return 'North American Manufacturer'
        elif wmi[0] in 'ABCDEFGH':
            return 'African Manufacturer'
        elif wmi[0] in 'JKL':
            return 'Asian Manufacturer'
        elif wmi[0] in 'MNP':
            return 'Asian Manufacturer'
        elif wmi[0] in 'RSTUVWXYZ':
            return 'European Manufacturer'
        
        return 'Unknown Manufacturer'
    
    def _decode_year(self, year_char):
        """Decode model year from 10th position"""
        current_year = datetime.now().year
        
        if year_char in self.year_mappings:
            decoded_year = self.year_mappings[year_char]
            
            # Handle the 30-year cycle
            if decoded_year < current_year - 20:
                decoded_year += 30
            
            return decoded_year
        
        return None
    
    def _try_external_decode(self, vin):
        """
        Attempt to decode VIN using external API
        This is a placeholder for integration with services like:
        - NHTSA VIN Decoder API
        - AutoCheck API
        - Carfax API
        """
        try:
            # Example: NHTSA VIN Decoder API (free but limited)
            # url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json"
            # response = requests.get(url, timeout=5)
            
            # For demo purposes, return None to use basic decoding
            # In production, implement actual API integration
            return None
            
        except Exception:
            return None
    
    def get_vin_info(self, vin):
        """
        Get comprehensive VIN information including validation and decoding
        
        Args:
            vin (str): VIN to analyze
            
        Returns:
            dict: Complete VIN analysis
        """
        try:
            vin = vin.strip().upper()
            
            # Validate VIN
            validation = self.validate_vin(vin)
            
            if not validation.get('valid'):
                return validation
            
            # Decode VIN
            decode_result = self.decode_vin(vin)
            
            # Combine results
            return {
                'success': True,
                'vin': vin,
                'validation': {
                    'valid': True,
                    'format_check': 'passed',
                    'check_digit': 'validated'
                },
                'vehicle_info': decode_result.get('vehicle_info', {}),
                'decode_method': decode_result.get('decode_method', 'unknown'),
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'VIN analysis error: {str(e)}'
            }

