# AI Safety Call Agent

A real-time voice agent for verbally reporting AI harms, bias, discrimination, existential risks, and system failures. Built with [Pipecat](https://pipecat.ai), Google Gemini Live (Vertex AI), and FastAPI.

---

## Overview

This AI Safety Call Agent allows users to **speak directly** to an AI agent over a WebSocket connection and report instances of AI-related harm. The agent guides callers through structured data collection, can search the web for AI safety resources, and sends an SMS summary of the report, to a regulation body, at the end of the call.

---

## Features

- **Real-time speech-to-speech** ; powered by Google Gemini Live via Vertex AI, fully native audio)
- **Live web search** ; retrieves AI safety compliance resources and organization contacts via Serper API
- **SMS reporting** ; sends a structured harm report via sms at the end of each call
- **Low-latency streaming** ; WebSocket-based transport with interruption support

---

## Tech Stack

| Layer | Technology |
|---|---|
| Voice AI | Google Gemini Live (`gemini-live-2.5-flash-native-audio`) via Vertex AI |
| Agent Framework | [Pipecat](https://github.com/pipecat-ai/pipecat) v1.2+ |
| API Server | FastAPI + Uvicorn |
| Web Search | [Serper API](https://serper.dev) |
| SMS | [Twilio](https://twilio.com) |

---

## Project Structure

```
├── main.py               # FastAPI app, WebSocket endpoints
├── agent/
│   ├── pipeline.py      
│   ├── config.py        
│   ├── serializer.py
│   ├── utils.py 
│   └── tools.py     
├── requirements.txt
├── aimodel.py
├── .gitignore
└── .env
```

---

## Setup

### 1. Prerequisites to set up locally

- Python 3.11+
- [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) installed
- A GCP project with **Vertex AI API** enabled
- Twilio account
- Serper API key

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```dotenv
# Google Cloud
PROJECT_ID=your-gcp-project-id
PROJECT_LOCATION=project-location

# Gemini model settings
GEMINI_MODEL=gemini-model
GEMINI_VOICE=agent-voice

# Agent identity
BOT_NAME=specified_agent_name
SYSTEM_PROMPT=...

# Twilio
SMS_SID=your_twilio_account_sid
SMS_AUTH_TOKEN=your_twilio_auth_token
SMS_PHONE_NUMBER=+123.....

# Serper
SERPER_API_KEY=your_serper_api_key

# HOST
PORT=desired port

```

### 4. Authenticate with Google Cloud

```bash
gcloud auth application-default login
```


### 5. Run the server

```bash
python main.py
```

Server starts at `http://0.0.0.0:8000`.

---

## API Endpoints

| Endpoint | Protocol | Description |
|---|---|---|
| `GET /health` | HTTP | Health check |
| `WS /ws` | WebSocket | Gemini Live voice agent |

---

## How It Works

1. A client connects via WebSocket to `/ws`
2. The agent introduces itself and begins guiding the caller
3. The caller verbally describes an AI harm incident
4. The agent collects: AI system name, scenario, specific harm.
5. If needed, the agent searches the web for relevant AI safety organizations or compliance resources
6. At the end of the call, the agent sends an SMS summary of the report via Twilio, to an AI Safety org.

---

## Tools

### `web_search`
Searches the web in real time using Serper (Google Search API). Used when the caller needs AI safety resources, compliance guidance, or organization details.

### `send_sms`
Sends a structured SMS report via Twilio summarising the harm case — including the AI system involved, the scenario, and the harm described.

---

## License

MIT License

Copyright (c) 2026 Chisom Chibuike

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.