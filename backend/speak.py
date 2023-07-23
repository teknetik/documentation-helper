from elevenlabs import generate, play, voices, set_api_key, stream
import os

# Setting up the api key
set_api_key(os.environ["ELEVENLABS_API_KEY"])


def say(text):
    audio = generate(
        text=text,
        voice="s9nNtTrRlYmeRAQ4QVnO",
        model="eleven_monolingual_v1",
        # stream=True,
    )

    play(audio)
    #stream(audio)

if __name__ == "__main__":
    print(voices())