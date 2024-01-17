import whisper
import sounddevice as sd
from pydub import AudioSegment
import numpy as np

def record_audio(duration):
    # Record audio from the microphone
    audio_data = sd.rec(int(duration * 44100), samplerate=44100, channels=2, dtype=np.int16)
    sd.wait()

    # Convert the NumPy array to an AudioSegment
    audio_segment = AudioSegment(
        audio_data.tobytes(),
        frame_rate=44100,
        sample_width=audio_data.dtype.itemsize,
        channels=2
    )

    return audio_segment

def save_audio_as_mp3(audio_segment, filename):
    # Save the audio as an MP3 file
    audio_segment.export(filename, format="mp3")

def getAudio():
    # Specify the duration for recording (in seconds)
    recording_duration = 10

    # Record audio
    audio_data = record_audio(recording_duration)

    # Specify the output MP3 file name
    output_filename = "./audio_samples/audio.mp3"

    # Save audio as MP3
    save_audio_as_mp3(audio_data, output_filename)
    model = whisper.load_model("base")
    result = model.transcribe("./audio_samples/audio.mp3")
    return result["text"]