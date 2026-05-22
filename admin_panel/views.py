from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from chat.models import ChatSession
from services.bedrock import summarize_and_score

from django.contrib.auth import get_user_model
User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAdminUser])
def list_sessions(request):
    sessions = ChatSession.objects.all().values(
        'id', 'student__username', 'started_at', 'score', 'summary'
    )
    return Response({'sessions': list(sessions)})

@api_view(['POST'])
@permission_classes([IsAdminUser])
def summarize_session(request, session_id):
    session = ChatSession.objects.get(id=session_id)
    messages = list(
        session.messages.order_by('timestamp').values('role', 'content')
    )
    result = summarize_and_score(messages)
    session.summary = result['summary']
    session.score = result['score']
    session.save()
    return Response(result)



@api_view(['GET'])
@permission_classes([IsAdminUser])
def list_users(request):
    search = request.query_params.get('search', '')
    users = User.objects.filter(
        is_staff=False,
        username__icontains=search
    ).values('id', 'username', 'date_joined')
    return Response({'users': list(users)})

@api_view(['GET'])
@permission_classes([IsAdminUser])
def user_sessions(request, username):
    user = User.objects.get(username=username)
    sessions = ChatSession.objects.filter(
        student=user
    ).order_by('-started_at').values(
        'id', 'started_at', 'score', 'summary'
    )
    return Response({
        'username': username,
        'sessions': list(sessions)
    })