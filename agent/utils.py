from pipecat.adapters.schemas.function_schema import FunctionSchema

web_search_schema = FunctionSchema(
    name="web_search",
    description="Perform a live web search to find real-time information on AI Safety topic.",
    properties={
        "query": {
            "type": "string",
            "description": "The search query string.",
        }
    },
    required=["query"],
)


send_sms_schema = FunctionSchema(
    name="send_sms",
    description="Send an SMS text message, reporting the caller's specified AI harm through a phone number.",
    properties={
        "message": {
            "type": "string",
            "description": "The text message content to send.",
        },
    },
    required=["message"],
)
