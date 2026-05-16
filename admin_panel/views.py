from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from chat.models import ChatSession
from services.bedrock import summarize_and_score

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