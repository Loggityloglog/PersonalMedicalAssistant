# Real-Time Voice Stream Integration with Twilio & Deepgram

## 🧠 Project Summary

This project demonstrates a real-time voice processing pipeline that integrates **Twilio's Media Streams** with **Deepgram's conversational AI** using WebSockets. It is designed to handle live audio input from a Twilio voice call, send it to Deepgram's STS (Streaming Transcription Service) for real-time processing, and return audio responses seamlessly — enabling interactive AI voice agents or assistants.

---

## 🔍 Use Case

This system could be used in:
- AI-powered customer service agents
- Voice-based assistants
- Interactive phone bots
- Real-time transcription or translation tools

---

## ⚙️ Features

- ✅ **WebSocket Server** for handling Twilio Media Streams.
- ✅ **Real-time Audio Forwarding** to Deepgram’s Conversational AI API.
- ✅ **Audio Buffering and Chunking** for consistent voice streaming.
- ✅ **Barge-in Detection** (interrupting agent speech when the user starts talking).
- ✅ **Customizable Config** using a `config.json` file.
- ✅ **.env Integration** for secure API key management.

---

## 🧪 Technologies Used

- **Python 3.10+**
- **AsyncIO** for asynchronous stream handling.
- **WebSockets** for full-duplex communication.
- **Deepgram STS API** for speech understanding.
- **Twilio Programmable Voice** (Media Streams).
- **Base64 encoding** for Twilio media payloads.
- **dotenv** for environment variable loading.

---

## 🧩 Project Structure

```bash
.
├── main.py               # Main application script
├── config.json           # Deepgram configuration for the session
├── .env                  # Contains DEEPGRAM_API_KEY
└── README.md             # Project documentation
```

## 🚀 How It Works

- WebSocket Server starts on localhost:5000 using websockets.serve.

- When a Twilio call connects, it starts sending audio data to the server.

- The server buffers and forwards audio to Deepgram via WebSocket.

- Deepgram responds with generated audio (or events), which is encoded and sent back to Twilio.

- Barge-in is detected and handled, ensuring smooth two-way interaction.


## 🧰 Getting Started
### Prerequisites

- Python 3.10+

- Twilio account with Media Streams enabled

- Deepgram API key

### Configuration
```
git clone https://github.com/Loggityloglog/PersonalMedicalAssistant.git
cd twilio-deepgram-realtime
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### Set up .env
DEEPGRAM_API_KEY=your_deepgram_api_key

### create config.json
## 🧠 Concepts Demonstrated

- Asynchronous WebSocket Coordination

- Audio Stream Handling & Encoding

- Event-Driven Architecture

- API Integration & Authentication

- Separation of Concerns in System Design


## 📈 Why This Project Matters

- This project highlights real-world experience in building scalable, asynchronous systems that interact with external APIs in real time. It demonstrates key backend engineering skills:

- Low-latency streaming

- Voice interaction logic

- Secure credential handling

- Working with WebRTC-style media flows


## 📞 Demo or Integration Support

### For a working demo or assistance with integrating Twilio and Deepgram for live calls, feel free to reach out via LinkedIn or by email.