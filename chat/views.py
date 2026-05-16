from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import ChatSession, Message
from services.bedrock import chat as bedrock_chat

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_session(request):
    session = ChatSession.objects.create(student=request.user)
    return Response({'session_id': session.id}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request, session_id):
    session = ChatSession.objects.get(id=session_id, student=request.user)
    user_text = request.data['content']

    # Save student message
    Message.objects.create(session=session, role='user', content=user_text)

    # Build full history
    history = list(
        session.messages.order_by('timestamp').values('role', 'content')
    )

    # Call Bedrock
    reply = bedrock_chat(history)

    # Save Claude's reply
    Message.objects.create(session=session, role='assistant', content=reply)

    return Response({'reply': reply})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_history(request, session_id):
    session = ChatSession.objects.get(id=session_id, student=request.user)
    messages = session.messages.order_by('timestamp').values('role', 'content', 'timestamp')
    return Response({'messages': list(messages)})