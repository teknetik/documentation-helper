from elevenlabs import generate, play, voices, set_api_key, stream
import os

# Setting up the api key
set_api_key(os.environ["ELEVENLABS_API_KEY"])


def say(text):
    audio = generate(
        text=text,
        voice="N8SmJJ4vvs5Mz9VaT6u5",
        model="eleven_monolingual_v1",
        # stream=True,
    )

    play(audio)
    #stream(audio)
