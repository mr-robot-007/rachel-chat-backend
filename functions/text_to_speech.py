import requests
from decouple import config

ELEVEN_LABS_API_KEY = config("ELEVEN_LABS_API_KEY")

# Eleven Labs
# Convert Text to speech
async def convert_text_to_speech(message):
    # print("convert_tts called")
    # Define data/body
    body = {
        "model_id": "eleven_multilingual_v2",
        "text": message,
        "voice_settings": {
            "similarity_boost": 0,
            "stability": 0,
        }
    }
    # Define voice (voice id)
    voice_rachel = "21m00Tcm4TlvDq8ikWAM"

    # Constructing Headers and Endpoints
    headers = {
        "xi-api-key": ELEVEN_LABS_API_KEY,
        "Content-Type": "application/json",
        "accept": "audio/mpeg",
    }

    endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_rachel}"

    # Send request
    try:
        response = requests.post(endpoint, json=body, headers=headers)
    except Exception as e:
        print("exception occured on text_to_speech :35")
        return

    # Handle response
    if response.status_code == 200:
        # print("OK",response.content)
        return response.content
    else:
        # print("NOT OK")
        return 

# model_id:  eleven_multilingual_v2