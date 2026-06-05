import os
import json
import requests
from twilio.rest import Client
from dotenv import load_dotenv

from pipecat.adapters.schemas.function_schema import FunctionSchema
from pipecat.services.llm_service import FunctionCallParams

load_dotenv()


async def web_search(params: FunctionCallParams):
    query = params.arguments.get("query")
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": os.getenv("SERPER_API_KEY"),
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps({"q": query}))
        response.raise_for_status()
        results = response.json()
        snippets = [obj.get("snippet", "") for obj in results.get("organic", [])[:10]]
        result = {"status": "success", "results": snippets}
    except Exception as e:
        result = {"status": "error", "message": f"Web search failed: {str(e)}"}

    await params.result_callback(result)



async def send_sms(params: FunctionCallParams):
    message = params.arguments.get("message")

    sid = os.getenv("SMS_SID")
    auth_token = os.getenv("SMS_AUTH_TOKEN")
    from_phone = os.getenv("SMS_PHONE_NUMBER")

    if not all([sid, auth_token, from_phone]):
        await params.result_callback({
            "status": "error",
            "message": "SMS credentials are not properly configured.",
        })
        return
    try:
        client = Client(sid, auth_token)
        sms = client.api.messages.create(
            to= +23481#######8,
            from_=from_phone,
            body=message,
        )
        result = {
            "status": "successfully sent",
            "message_id": sms.sid,
            "to": sms.to,
            "from": sms.from_,
            "body": sms.body,
        }
    except Exception as e:
        result = {"status": "error", "message": str(e)}

    await params.result_callback(result)

