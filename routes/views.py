from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Route
from .serializers import RouteSerializer, RouteCalculationSerializer
from fares.fare_calculator import calculate_route_with_fare
from users.models import DiscountCard


class RouteViewSet(viewsets.ModelViewSet):
    """ViewSet for Route model"""
    queryset = Route.objects.filter(is_active=True)
    serializer_class = RouteSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['transport_type', 'origin', 'destination', 'is_active']


@api_view(['POST'])
@permission_classes([AllowAny])
def calculate_route(request):
    """
    Calculate route and fare using Google Maps
    POST /api/routes/calculate
    {
        "origin": [latitude, longitude],
        "destination": [latitude, longitude],
        "user_id": optional_user_id,
        "use_google_maps": true,
        "passenger_type": "REGULAR|SENIOR|PWD|STUDENT"
    }
    """
    serializer = RouteCalculationSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    origin = tuple(serializer.validated_data['origin'])
    destination = tuple(serializer.validated_data['destination'])
    use_google_maps = serializer.validated_data.get('use_google_maps', True)
    user_id = serializer.validated_data.get('user_id')
    passenger_type = serializer.validated_data.get('passenger_type', 'REGULAR')
    
    # Get discount card if user is provided (for logging purposes)
    discount_card = None
    if user_id:
        try:
            discount_card = DiscountCard.objects.filter(
                user_id=user_id,
                is_active=True,
                verification_status='APPROVED'
            ).first()
        except Exception:
            pass
    
    # Calculate route and fare
    try:
        result = calculate_route_with_fare(
            origin=origin,
            destination=destination,
            discount_card=discount_card,
            use_google_maps=use_google_maps,
            passenger_type=passenger_type
        )
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
