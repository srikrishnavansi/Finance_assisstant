from pydub import AudioSegment
import io

def ensure_wav_format(audio_bytes):
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
    out_io = io.BytesIO()
    audio.export(out_io, format="wav")
    return out_io.getvalue()
