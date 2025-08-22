import asyncio
import base64
import json
import websockets
import os
from dotenv import load_dotenv

load_dotenv()

# Connect the websocket
def sts_connect():
    api_key = os.getenv("DEEPGRAM_API_KEY")
    if not api_key:
        raise Exception("Fix your api for deepgram")

    sts_ws = websockets.connect(
        "wss://agent.deepgram.com/v1/agent/converse",
        subprotocols=["token", api_key]
    )
    return sts_ws

    # Load our config file
def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

# This is going to handle if the user starts talking while the agent is speaking
async def handle_barge_in(decoded, twilio_ws, streamsid):
    if decoded["type"] == "UserStartedSpeaking":
        clear_message = {
            "event": "clear",
            "streamSid": streamsid
        }
        await twilio_ws.send(json.dumps(clear_message))

async def handle_text_message(decoded, twilio_ws, sts_ws, streamsid):
    await handle_barge_in(decoded, twilio_ws, streamsid)

async def sts_sender(sts_ws, audio_queue):
    print("sts_sender starting")
    while True:
        # as soon as we get the audio, we send it straight to deepgram
        chunk = await audio_queue.get()
        await sts_ws.send(chunk)

async def sts_receiver(sts_ws, twilio_ws, streamsid_queue):
    print("sts_receiver starting")

    streamsid = await streamsid_queue.get()

    async for message in sts_ws:
        if type(message) is str:
            decoded = json.loads(message)
            await handle_text_message(decoded, twilio_ws, sts_ws, streamsid)
            continue

        # Decode the message gotten from deepgram
        raw_mulaw = message
        media_message = {
            "event": "media",
            "streamSid": streamsid,
            "media": {"payload": base64.b64encode(raw_mulaw).decode("ascii")}
        }

        # Twilio will just speak this
        await twilio_ws.send(json.dumps(media_message))

async def twilio_receiver(twilio_ws, audio_queue, streamsid_queue):
    # 160 is the bitrate, 20 is the chunk size. So we get the total amount of size here
    BUFFER_SIZE = 20 * 160

    inbuffer = bytearray(b"")

    # Go over each of the messages
    async for message in twilio_ws:
        try:
            data = json.loads(message)
            event = data["event"]
            # This is the start event - we get the streamid and add it to the queue
            if event == "start":
                print("get our streamsid")
                start = data["start"]
                streamsid = start["streamSid"]
                streamsid_queue.put_nowait(streamsid)
            # If we are connected, great. Do nothing
            elif event == "connected":
                continue
            # if we got some media, we are going to add that voice data to our buffer
            elif event == "media":
                media = data["media"]
                chunk = base64.b64decode(media["payload"])

                if media["track"] == "inbound":
                    inbuffer.extend(chunk)
            # If the user has stopped talking
            elif event == "stop":
                break
            # Logic for ending the buffer
            while len(inbuffer) >= BUFFER_SIZE:
                chunk = inbuffer[:BUFFER_SIZE]
                audio_queue.put_nowait(chunk)
                inbuffer = inbuffer[BUFFER_SIZE:]
        except:
            print("Some error in buffering the twilio voice data")

async def twilio_handler(twilio_ws):
    # Storing all the audio we need to respond to
    audio_queue = asyncio.Queue()
    # The current streams we have from twilio
    streamsid_queue = asyncio.Queue()

    async with sts_connect() as sts_ws:
        # Load the config message and send it to deepgram
        config_message = load_config()
        print("config message: ", config_message)
        await sts_ws.send(json.dumps(config_message))

        # always run our sender,
        await asyncio.wait(
           [
               asyncio.ensure_future(sts_sender(sts_ws, audio_queue)),
               asyncio.ensure_future(sts_receiver(sts_ws, twilio_ws, streamsid_queue)),
               asyncio.ensure_future(twilio_receiver(twilio_ws, audio_queue, streamsid_queue))
           ]
        )

        # Now we can close the websocket
        await twilio_ws.close()


async def main():
    await websockets.serve(twilio_handler, "localhost", 5000)
    print("started the server now")
    await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())
