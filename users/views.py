from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.utils import timezone
from django.contrib.auth import get_user_model

from .models import (
    Vehicle, DiscountCard, DiscountUsageLog,
    Incident, FareCalculation
)
from .serializers import (
    UserSerializer, VehicleSerializer, DiscountCardSerializer,
    DiscountCardVerificationSerializer, DiscountUsageLogSerializer,
    IncidentSerializer, IncidentUpdateSerializer, FareCalculationSerializer
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter users based on role"""
        if self.request.user.role in ['ADMIN', 'MODERATOR']:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)


class VehicleViewSet(viewsets.ModelViewSet):
    """ViewSet for Vehicle model"""
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Users can only see their own vehicles"""
        if self.request.user.role in ['ADMIN', 'MODERATOR']:
            return Vehicle.objects.all()
        return Vehicle.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        """Set owner to current user"""
        serializer.save(owner=self.request.user)


class DiscountCardViewSet(viewsets.ModelViewSet):
    """ViewSet for DiscountCard model"""
    queryset = DiscountCard.objects.all()
    serializer_class = DiscountCardSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter based on user role"""
        if self.request.user.role in ['ADMIN', 'MODERATOR']:
            return DiscountCard.objects.all()
        return DiscountCard.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Set user to current user"""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def verify(self, request, pk=None):
        """Verify or reject discount card (admin only)"""
        card = self.get_object()
        serializer = DiscountCardVerificationSerializer(data=request.data)
        
        if serializer.is_valid():
            action_type = serializer.validated_data['action']
            notes = serializer.validated_data.get('notes', '')
            
            if action_type == 'approve':
                card.verification_status = 'APPROVED'
            else:
                card.verification_status = 'REJECTED'
            
            card.verification_notes = notes
            card.verified_at = timezone.now()
            card.verified_by = request.user
            card.save()
            
            return Response(DiscountCardSerializer(card).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def pending(self, request):
        """Get all pending discount cards (admin only)"""
        pending_cards = DiscountCard.objects.filter(verification_status='PENDING')
        serializer = self.get_serializer(pending_cards, many=True)
        return Response(serializer.data)


class DiscountUsageLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for DiscountUsageLog model (read-only)"""
    queryset = DiscountUsageLog.objects.all()
    serializer_class = DiscountUsageLogSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter based on user role"""
        if self.request.user.role in ['ADMIN', 'MODERATOR']:
            return DiscountUsageLog.objects.all()
        return DiscountUsageLog.objects.filter(discount_card__user=self.request.user)


class IncidentViewSet(viewsets.ModelViewSet):
    """ViewSet for Incident model"""
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter based on user role and query params"""
        queryset = Incident.objects.all()
        
        # Filter by status
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)
        
        # Filter by incident type
        type_param = self.request.query_params.get('type')
        if type_param:
            queryset = queryset.filter(incident_type=type_param)
        
        # Regular users can only see their own incidents
        if self.request.user.role not in ['ADMIN', 'MODERATOR']:
            queryset = queryset.filter(user=self.request.user)
        
        return queryset
    
    def perform_create(self, serializer):
        """Set user to current user"""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['patch'], permission_classes=[IsAdminUser])
    def update_status(self, request, pk=None):
        """Update incident status (admin only)"""
        incident = self.get_object()
        serializer = IncidentUpdateSerializer(data=request.data)
        
        if serializer.is_valid():
            if 'status' in serializer.validated_data:
                incident.status = serializer.validated_data['status']
                if incident.status == 'RESOLVED':
                    incident.resolved_at = timezone.now()
                    incident.resolved_by = request.user
            
            if 'priority' in serializer.validated_data:
                incident.priority = serializer.validated_data['priority']
            
            if 'admin_notes' in serializer.validated_data:
                incident.admin_notes = serializer.validated_data['admin_notes']
            
            incident.save()
            return Response(IncidentSerializer(incident).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FareCalculationViewSet(viewsets.ModelViewSet):
    """ViewSet for FareCalculation model"""
    queryset = FareCalculation.objects.all()
    serializer_class = FareCalculationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter based on user role"""
        if self.request.user.role in ['ADMIN', 'MODERATOR']:
            return FareCalculation.objects.all()
        return FareCalculation.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Set user to current user if not provided"""
        if not serializer.validated_data.get('user'):
            serializer.save(user=self.request.user)
        else:
            serializer.save()
