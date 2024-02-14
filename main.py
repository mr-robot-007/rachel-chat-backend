# source venv/Scripts/activate
# uvicorn main:app
# uvicorn main:app --reload
# pip install -r requirements.txt


# Main imports
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware



# Custom function imports
from functions.openai_requests import convert_audio_to_text, get_chat_response
from functions.database import store_messages, reset_messages
from functions.text_to_speech import convert_text_to_speech

# initiate app

app = FastAPI()

# CORS - Origins
origins = [
    'http://localhost:5173',
    'http://localhost:5174',
    'http://localhost:4173',
    'http://localhost:4174',
    'http://localhost:3000',
    '*'
]


# CORS - Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# check health
@app.get("/health")
async def check_health():
    return {"message": "healthy"}

# Reset Messages
@app.get("/reset")
async def reset_converstaion():
    reset_messages();
    return {"message": "converstion reset"}

# Get audio
# @app.get("/post-audio-get/")
# async def get_audio():
#     print('get_audio called')

#     # Get saved audio
#     audio_input = open("voice.mp3","rb");

#     # Decode Audio
#     # message_decoded = convert_audio_to_text(audio_input)
#     message_decoded = "Hi,  I am Anuj. How are you?"
#     # print(message_decoded)

#     # Gaurd: Ensure message decoded
#     if not message_decoded:
#         return HTTPException(status_code=400, detail="Failed to decode audio")
    
#     # Get ChatGPT response
#     chat_response = get_chat_response(message_decoded)

#     # Gaurd: Ensure chat response
#     if not chat_response:
#         return HTTPException(status_code=400, detail="Failed to get chat response")

#     # Store messages
#     store_messages(message_decoded,chat_response)

#     # print(chat_response)

#     # Convert chat response to audio
#     audio_output = await convert_text_to_speech(chat_response)

#     # Gaurd: Ensure get audio response
#     if not audio_output:
#         return HTTPException(status_code=400, detail="Failed to get Eleven labs audio response")

    
#     # Create a generator that yield chucks of data
#     def iterfile():
#         yield audio_output
    
#     # Return audio file
#     return StreamingResponse(iterfile(),media_type="audio/mpeg")

#     # return


# Post bot response
# Note: Not playing in browser when using post request
@app.post("/post-audio")
async def post_audio(file: UploadFile = File(...)):
    # print('get_audio called')

    # # Get saved audio

    # Save file from frontend
    with open(file.filename,"wb") as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename,"rb")

    # Decode Audio
    message_decoded = convert_audio_to_text(audio_input)
    # print(message_decoded)

    # Gaurd: Ensure message decoded
    if not message_decoded:
        return HTTPException(status_code=400, detail="Failed to decode audio")
    
    # Get ChatGPT response
    chat_response = get_chat_response(message_decoded)

    # Gaurd: Ensure chat response
    if not chat_response:
        return HTTPException(status_code=400, detail="Failed to get chat response")

    # Store messages
    store_messages(message_decoded,chat_response)

    # print(chat_response)

    # Convert chat response to audio
    audio_output = await convert_text_to_speech(chat_response)

    # Gaurd: Ensure get audio response
    if not audio_output:
        return HTTPException(status_code=400, detail="Failed to get Eleven labs audio response")

    
    # Create a generator that yield chucks of data
    def iterfile():
        yield audio_output
    
    # Return audio file
    return StreamingResponse(iterfile(),media_type="application/octet-stream")

    # return