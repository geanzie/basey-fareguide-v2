"""
Fare calculation service - replicates the Next.js fare calculation logic
Based on Municipal Ordinance 105 Series of 2023
"""
from decimal import Decimal, ROUND_HALF_UP
import math
from typing import Dict, Optional, Tuple
from django.conf import settings
import googlemaps
from datetime import datetime


class FareCalculator:
    """
    Fare calculation based on Basey Municipal Ordinance 105 Series of 2023
    
    Base Fare: ₱15.00 (covers first 3 kilometers)
    Additional Rate: ₱3.00 per kilometer beyond 3km
    Rounding: Final fare rounded to nearest ₱0.50
    Discount: 20% for Senior Citizens, PWDs, Students
    """
    
    BASE_FARE = Decimal('15.00')
    BASE_DISTANCE_KM = Decimal('3.00')
    ADDITIONAL_RATE_PER_KM = Decimal('3.00')
    DISCOUNT_RATE = Decimal('0.20')  # 20%
    
    @staticmethod
    def round_to_nearest_half(amount: Decimal) -> Decimal:
        """Round to nearest 0.50"""
        return (amount * 2).quantize(Decimal('1'), rounding=ROUND_HALF_UP) / 2
    
    @classmethod
    def calculate_fare(
        cls,
        distance_km: float,
        discount_rate: Optional[float] = None
    ) -> Dict:
        """
        Calculate fare based on distance and optional discount
        
        Args:
            distance_km: Distance in kilometers
            discount_rate: Optional discount rate (0.20 for 20%)
        
        Returns:
            Dict with fare, original_fare, discount_applied, breakdown
        """
        distance = Decimal(str(distance_km))
        
        # Calculate original fare
        if distance <= cls.BASE_DISTANCE_KM:
            original_fare = cls.BASE_FARE
            additional_distance = Decimal('0')
            additional_fare = Decimal('0')
        else:
            additional_distance = distance - cls.BASE_DISTANCE_KM
            # Round up additional distance to nearest km
            additional_distance_rounded = Decimal(math.ceil(float(additional_distance)))
            additional_fare = additional_distance_rounded * cls.ADDITIONAL_RATE_PER_KM
            original_fare = cls.BASE_FARE + additional_fare
        
        # Round original fare to nearest 0.50
        original_fare = cls.round_to_nearest_half(original_fare)
        
        # Apply discount if provided
        if discount_rate:
            discount_decimal = Decimal(str(discount_rate))
            discount_amount = original_fare * discount_decimal
            final_fare = original_fare - discount_amount
            final_fare = cls.round_to_nearest_half(final_fare)
        else:
            discount_amount = Decimal('0')
            final_fare = original_fare
        
        return {
            'fare': final_fare,
            'original_fare': original_fare,
            'discount_applied': discount_amount,
            'breakdown': {
                'base_fare': cls.BASE_FARE,
                'base_distance_km': cls.BASE_DISTANCE_KM,
                'additional_distance_km': additional_distance,
                'additional_fare': additional_fare,
                'distance_km': distance,
            }
        }


class GoogleMapsService:
    """Service for Google Maps API integration"""
    
    def __init__(self):
        # Use server API key (no referrer restrictions) for server-side APIs
        api_key = settings.GOOGLE_MAPS_SERVER_API_KEY or settings.GOOGLE_MAPS_API_KEY
        if not api_key:
            raise ValueError("GOOGLE_MAPS_SERVER_API_KEY not configured in settings")
        self.client = googlemaps.Client(key=api_key)  # type: ignore
    
    def get_route_distance(
        self,
        origin: Tuple[float, float],
        destination: Tuple[float, float]
    ) -> Optional[Dict]:
        """
        Get route distance and duration from Google Maps Distance Matrix API
        
        Args:
            origin: Tuple of (latitude, longitude)
            destination: Tuple of (latitude, longitude)
        
        Returns:
            Dict with distance, duration, and route info or None if failed
        """
        try:
            result = self.client.distance_matrix(  # type: ignore
                origins=[origin],
                destinations=[destination],
                mode='driving',
                units='metric',
                departure_time=datetime.now()
            )
            
            if result['status'] != 'OK':
                return None
            
            element = result['rows'][0]['elements'][0]
            
            if element['status'] != 'OK':
                return None
            
            distance_meters = element['distance']['value']
            distance_km = distance_meters / 1000.0
            duration_seconds = element['duration']['value']
            
            return {
                'distance': {
                    'meters': distance_meters,
                    'kilometers': distance_km,
                    'text': element['distance']['text']
                },
                'duration': {
                    'seconds': duration_seconds,
                    'text': element['duration']['text']
                }
            }
        except Exception as e:
            print(f"Google Maps API error: {e}")
            return None
    
    def get_detailed_route(
        self,
        origin: Tuple[float, float],
        destination: Tuple[float, float]
    ) -> Optional[Dict]:
        """
        Get detailed route with polyline from Google Maps Directions API
        
        Args:
            origin: Tuple of (latitude, longitude)
            destination: Tuple of (latitude, longitude)
        
        Returns:
            Dict with polyline and detailed route info or None if failed
        """
        try:
            result = self.client.directions(  # type: ignore
                origin=origin,
                destination=destination,
                mode='driving',
                departure_time=datetime.now()
            )
            
            if not result:
                return None
            
            route = result[0]
            leg = route['legs'][0]
            
            return {
                'polyline': route['overview_polyline']['points'],
                'bounds': route['bounds'],
                'distance': {
                    'meters': leg['distance']['value'],
                    'kilometers': leg['distance']['value'] / 1000.0,
                    'text': leg['distance']['text']
                },
                'duration': {
                    'seconds': leg['duration']['value'],
                    'text': leg['duration']['text']
                },
                'start_address': leg['start_address'],
                'end_address': leg['end_address'],
                'steps': [
                    {
                        'distance': step['distance']['text'],
                        'duration': step['duration']['text'],
                        'instruction': step['html_instructions']
                    }
                    for step in leg['steps']
                ]
            }
        except Exception as e:
            print(f"Google Maps Directions API error: {e}")
            return None


class GPSDistanceCalculator:
    """Calculate distance using Haversine formula (GPS-only fallback)"""
    
    EARTH_RADIUS_KM = 6371.0
    
    @classmethod
    def calculate_distance(
        cls,
        origin: Tuple[float, float],
        destination: Tuple[float, float]
    ) -> float:
        """
        Calculate distance between two GPS coordinates using Haversine formula
        
        Args:
            origin: Tuple of (latitude, longitude)
            destination: Tuple of (latitude, longitude)
        
        Returns:
            Distance in kilometers
        """
        lat1, lon1 = origin
        lat2, lon2 = destination
        
        # Convert to radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        # Haversine formula
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = (
            math.sin(dlat / 2) ** 2 +
            math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        distance = cls.EARTH_RADIUS_KM * c
        
        # Apply road network multiplier (roads are not straight lines)
        # Default multiplier: 1.4 (40% longer than straight line)
        road_multiplier = 1.4
        
        return distance * road_multiplier


def calculate_route_with_fare(
    origin: Tuple[float, float],
    destination: Tuple[float, float],
    discount_card=None,
    use_google_maps: bool = True,
    passenger_type: str = 'REGULAR'
) -> Dict:
    """
    Complete route calculation with fare
    
    Args:
        origin: Tuple of (latitude, longitude)
        destination: Tuple of (latitude, longitude)
        discount_card: Optional DiscountCard model instance
        use_google_maps: Whether to use Google Maps API (fallback to GPS if False)
        passenger_type: Passenger type (REGULAR, SENIOR, PWD, STUDENT) for discount
    
    Returns:
        Dict with route info, distance, and fare calculation
    """
    method_used = 'gps'
    route_data = None
    
    # Try Google Maps first if enabled
    if use_google_maps:
        try:
            gmaps = GoogleMapsService()
            route_data = gmaps.get_detailed_route(origin, destination)
            
            if route_data:
                distance_km = route_data['distance']['kilometers']
                method_used = 'google_maps'
            else:
                # Fallback to GPS
                distance_km = GPSDistanceCalculator.calculate_distance(origin, destination)
        except Exception:
            # Fallback to GPS
            distance_km = GPSDistanceCalculator.calculate_distance(origin, destination)
    else:
        distance_km = GPSDistanceCalculator.calculate_distance(origin, destination)
    
    # Determine discount rate based on passenger type
    discount_rate = None
    discount_info = None
    
    # Apply discount for eligible passenger types (20% discount)
    if passenger_type in ['SENIOR', 'PWD', 'STUDENT']:
        discount_rate = 0.20  # 20% discount
        discount_info = {
            'passenger_type': passenger_type,
            'discount_rate': discount_rate
        }
    
    # If a verified discount card exists, include it in the response
    if discount_card and hasattr(discount_card, 'is_valid') and discount_card.is_valid():
        if discount_info:
            discount_info['card_id'] = discount_card.id
            discount_info['discount_type'] = discount_card.discount_type
            discount_info['id_number'] = discount_card.id_number
    
    # Calculate fare
    fare_result = FareCalculator.calculate_fare(distance_km, discount_rate)
    breakdown = fare_result['breakdown']
    
    return {
        'success': True,
        'method': method_used,
        'route': route_data,
        'distance': {
            'kilometers': distance_km,
            'meters': distance_km * 1000
        },
        'fare': {
            'fare': float(fare_result['fare']),
            'original_fare': float(fare_result['original_fare']),
            'discount_applied': float(fare_result['discount_applied']),
            'breakdown': {
                'base_fare': float(breakdown['base_fare']),
                'base_distance_km': float(breakdown['base_distance_km']),
                'additional_distance_km': float(breakdown['additional_distance_km']),
                'additional_fare': float(breakdown['additional_fare']),
                'distance_km': float(breakdown['distance_km']),
            }
        },
        'discount_info': discount_info
    }
