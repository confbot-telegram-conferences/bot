from app.core.file import File
from app.core.context import Context


class VoiceAudioMixin:
    def get_voice_audio(self, context: Context):
        file: File = context.get_voice()
        # if not file:
        #     file = context.get_audio()
        return file
