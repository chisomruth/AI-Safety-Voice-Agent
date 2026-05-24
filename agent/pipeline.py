from loguru import logger
from starlette.websockets import WebSocket

from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.frames.frames import LLMRunFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask
from pipecat.processors.aggregators.llm_context import LLMContext
from pipecat.processors.aggregators.llm_response_universal import (
    LLMContextAggregatorPair,
    LLMUserAggregatorParams,
)
from pipecat.services.google.gemini_live.vertex.llm import GeminiLiveVertexLLMService
from pipecat.transports.websocket.fastapi import (
    FastAPIWebsocketParams,
    FastAPIWebsocketTransport,
)
from pipecat.turns.user_mute import FirstSpeechUserMuteStrategy

from .config import config
from .serializer import SimpleRawFrameSerializer

async def run_agent(websocket: WebSocket) -> None:
    transport = FastAPIWebsocketTransport(
        websocket=websocket,
        params=FastAPIWebsocketParams(
            audio_in_enabled=True,
            audio_out_enabled=True,
            add_wav_header=False,
            serializer=SimpleRawFrameSerializer(),
        ),
    )


    llm = GeminiLiveVertexLLMService(
        project_id=config.project_id,
        location=config.project_location,
        settings=GeminiLiveVertexLLMService.Settings(
            model=config.gemini_model,
            voice=config.gemini_voice,    
            system_instruction=config.system_prompt 
        )
    )


    context = LLMContext()
    user_aggregator, assistant_aggregator = LLMContextAggregatorPair(
        context,
        user_params=LLMUserAggregatorParams(
            user_mute_strategies=[FirstSpeechUserMuteStrategy()],
        ),
    )

    pipeline = Pipeline([
        transport.input(),
        user_aggregator,
        llm,                  
        transport.output(),
        assistant_aggregator,
    ])

    task = PipelineTask(
        pipeline,
        params=PipelineParams(
            allow_interruptions=True,
            enable_metrics=True,
        )
    )

    runner = PipelineRunner(handle_sigint=False)

    @transport.event_handler("on_client_connected")
    async def on_client_connected(transport, client):
        logger.info("Client connected")
        context.add_message({
            "role": "developer",
            "content": (
                "The call has successfully connected. Please proactively introduce yourself "
                "as an AI Safety Agent designed to help report AI harms. "
            ),
        })
        await task.queue_frames([LLMRunFrame()])

    @transport.event_handler("on_client_disconnected")
    async def on_client_disconnected(transport, client):
        logger.info("Client disconnected.")
        await task.cancel()

    await runner.run(task)