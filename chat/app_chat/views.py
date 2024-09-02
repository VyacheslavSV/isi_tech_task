from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app_chat.models import Thread, Message
from app_chat.serializers import ThreadSerializer, MessageSerializer


class ThreadViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing thread instances.

    Handles operations related to `Thread` such as creation, retrieval, and deletion.
    Ensures that a thread cannot have more than two participants.
    """
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Create a new thread or return an existing one if a thread with the same participants already exists.

        Participants must be exactly two. If a thread with the given participants already exists,
        it is returned instead of creating a new one.
        """
        participants = request.data.get('participants')
        if participants and len(participants) == 2:
            participants_set = set(participants)
            existing_thread = Thread.objects.annotate(
                participants_count=Count('participants')
            ).filter(participants__in=participants_set).distinct().filter(participants_count=2)

            if existing_thread.exists():
                return Response(self.get_serializer(existing_thread.first()).data, status=status.HTTP_200_OK)

        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path='user-threads')
    def user_threads(self, request):
        """
        Retrieve all threads where the authenticated user is a participant.

        Returns a list of threads associated with the currently authenticated user.
        """
        user = request.user
        threads = Thread.objects.filter(participants=user)
        serializer = self.get_serializer(threads, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing message instances.

    Handles operations related to `Message` such as creation, marking as read, and retrieving unread message counts.
    """

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """
        Automatically set the sender of the message to the currently authenticated user.

        This method is called when creating a new message, ensuring that the `sender` field
        is populated with the user making the request.
        """
        serializer.save(sender=self.request.user)

    @action(detail=True, methods=['post'], url_path='mark-as-read')
    def mark_as_read(self, request, pk=None):
        """
        Mark a specific message as read.

        This action updates the `is_read` field of the message with the given primary key (`pk`).
        """
        message = self.get_object()
        message.is_read = True
        message.save()
        return Response({'status': 'Message marked as read'})

    @action(detail=False, methods=['get'], url_path='unread-count')
    def unread_count(self, request):
        """
        Retrieve the number of unread messages for the authenticated user.

        Counts and returns the number of unread messages for the currently authenticated user.
        """
        user = request.user
        unread_messages_count = Message.objects.filter(thread__participants=user, is_read=False).count()
        return Response({'unread_count': unread_messages_count})
