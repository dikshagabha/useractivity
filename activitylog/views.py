from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import UserActivityLog
from .serializers import UserActivityLogSerializer
from .permissions import IsOwnerOrAdmin
from django.utils.dateparse import parse_datetime
from django.db.models import Q

class CreateActivityLogView(generics.CreateAPIView):
    queryset = UserActivityLog.objects.all()
    serializer_class = UserActivityLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserActivityLogListView(generics.ListAPIView):
    serializer_class = UserActivityLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        if int(user_id) != self.request.user.id and not self.request.user.is_staff:
            return UserActivityLog.objects.none()
        return UserActivityLog.objects.filter(user__id=user_id)


class AllActivityLogView(generics.ListAPIView):
    serializer_class = UserActivityLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['action']

    def get_queryset(self):
        queryset = UserActivityLog.objects.all()
        timestamp_range = self.request.query_params.get('timestamp__range')
        if timestamp_range:
            try:
                start, end = timestamp_range.split(',')
                queryset = queryset.filter(timestamp__range=[start, end])
            except:
                pass
        return queryset


class UpdateActivityStatusView(generics.UpdateAPIView):
    queryset = UserActivityLog.objects.all()
    serializer_class = UserActivityLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        status_value = request.data.get("status")
        if status_value not in ["PENDING", "IN_PROGRESS", "DONE"]:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        instance.status = status_value
        instance.save()
        return Response(self.get_serializer(instance).data)
