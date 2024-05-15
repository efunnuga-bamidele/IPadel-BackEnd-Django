from rest_framework import viewsets, permissions
from django.http import JsonResponse
from .serializers import MatchSerializer
from .models import Match
from rest_framework.decorators import action
from rest_framework import status
import random
from django.http import JsonResponse


def generate_reference(length=20):
    return ''.join(random.SystemRandom().choice([chr(i) for i in range(97, 123)] + [str(i) for i in range(20)]) for _ in range(length))


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all().order_by('id')
    serializer_class = MatchSerializer

    def get_permissions(self):
        if self.action == 'list':
            return []
        return [permissions.IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        data = request.data
        data['bookedBy'] = user.email
        data['referenceId'] = generate_reference()

        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            self.perform_create(serializer)
            return JsonResponse({'success': True, 'error': False, 'message': 'Match booking placed successfully', 'data': serializer.data, "status": status.HTTP_200_OK})
        return JsonResponse({'success': False, 'error': True, 'message': "Match booking failed", "status": status.HTTP_400_BAD_REQUEST, 'data': {}})

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse({'success': True, 'error': False, 'message': 'Match booking removed successfully', "status": status.HTTP_200_OK})

    # Custom action to retrieve by referenceId
    @action(detail=False, methods=['get'])
    def retrieve_by_referenceId(self, request):
        referenceId = request.query_params.get('referenceId', None)
        if referenceId is not None:
            records = Match.objects.filter(referenceId=referenceId)

            if len(records) > 0:
                serializer = self.get_serializer(records, many=True)
                return JsonResponse({'success': True, 'error': False, 'message': 'Match retrieved successfully', 'data': serializer.data, "status": status.HTTP_200_OK})
            return JsonResponse({'success': False, 'error': True, 'message': "Match record not found", "status": status.HTTP_400_BAD_REQUEST, 'data': {}})

        else:
            return JsonResponse({'success': False, 'error': True, 'message': "Match reference Id not found", "status": status.HTTP_400_BAD_REQUEST, 'data': {}})
    # get match where club name, date, and status is open

    @action(detail=False, methods=['get'])
    def retrieve_by_condition(self, request):
        clubName = request.query_params.get('club_name', None)
        matchDate = request.query_params.get('match_date', None)
        matchStatus = request.query_params.get('match_status', None)
        if None not in (clubName, matchDate, matchStatus):
            records = Match.objects.filter(
                date=matchDate, status=matchStatus, court=clubName)

            if len(records) > 0:
                serializer = self.get_serializer(records, many=True)
                return JsonResponse({'success': True, 'error': False, 'message': 'Match retrieved successfully', 'data': serializer.data, "status": status.HTTP_200_OK})
            return JsonResponse({'success': True, 'error': False, 'message': "Match record not found", "status": status.HTTP_200_OK, 'data': []})

        else:
            return JsonResponse({'success': False, 'error': True, 'message': "Match reference Id not found", "status": status.HTTP_400_BAD_REQUEST, 'data': {}})
