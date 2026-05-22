import boto3
import json
from dotenv import load_dotenv

load_dotenv()

client = boto3.client(
    service_name='bedrock-runtime',
    region_name='eu-north-1'
)

# MODEL_ID = 'anthropic.claude-haiku-20240307-v1:0'

# MODEL_ID = 'eu.anthropic.claude-haiku-20240307-v1:0'

MODEL_ID = 'eu.anthropic.claude-haiku-4-5-20251001-v1:0'

SYSTEM_PROMPT = """You are a cybersecurity tutor. Your job is to:
1. Teach cybersecurity concepts clearly and simply.
2. Ask follow-up questions to test the student's understanding.
3. Gently correct misconceptions without giving away full answers.
Topics include: networking, encryption, threats, vulnerabilities, best practices."""

def chat(messages: list) -> str:
    try:
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1024,
            "system": SYSTEM_PROMPT,
            "messages": messages
        }
        response = client.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(body)
        )
        return json.loads(response['body'].read())['content'][0]['text']
    except Exception as e:
        
        return "I'm having trouble connecting right now. Please try again in a moment."

def summarize_and_score(messages: list) -> dict:
    try:
        transcript = "\n".join(
            f"[{m['role'].upper()}]: {m['content']}" for m in messages
        )
        prompt = f"""Analyze this cybersecurity tutoring conversation.

        {transcript}

        Respond ONLY in valid JSON like this:
        {{
            "summary": "2-3 sentence summary of what the student discussed",
            "score": <integer 0-100 reflecting cybersecurity knowledge shown>,
            "strengths": ["..."],
            "gaps": ["..."]
        }}"""
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 512,
            "messages": [{"role": "user", "content": prompt}]
        }
        response = client.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(body)
        )
        text = json.loads(response['body'].read())['content'][0]['text']
        text = text.strip()
        if text.startswith('```'):
            text = text.split('\n', 1)[1]
            text = text.rsplit('```', 1)[0]
        return json.loads(text)
    except Exception as e:
        return {
            "summary": "Error generating summary.",
            "score": 0,
            "strengths": [],
            "gaps": []
        }