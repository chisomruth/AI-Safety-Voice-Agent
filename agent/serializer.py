from pipecat.serializers.base_serializer import FrameSerializer
from pipecat.frames.frames import Frame, AudioRawFrame, InputAudioRawFrame
from .config import config

class SimpleRawFrameSerializer(FrameSerializer):
    
    async def serialize(self, frame: Frame) -> bytes | str | None:
        if isinstance(frame, AudioRawFrame):
            return frame.audio
        return None

    async def deserialize(self, data: bytes | str) -> Frame | None:
        if isinstance(data, (bytes, bytearray)):
            return InputAudioRawFrame(
                audio=data, 
                num_channels=1, 
                sample_rate=16000,
            )
        return None