# 🎙️ Dhanush AI

### Real-Time Voice AI Assistant powered by Gemini Live API

**Dhanush AI** is a local, browser-based real-time voice assistant that lets you have natural voice conversations with AI directly from your browser.

Speak naturally in **English, Telugu, or a mix of both** — Dhanush AI automatically follows the language you're using during the conversation.

🔐 Your permanent Gemini API key stays securely on the **Python backend**. The browser receives only a **short-lived, single-use authentication token** for the Live API session.

---

## ✨ Features

| Feature                         | Description                                         |
| ------------------------------- | --------------------------------------------------- |
| 🎙️ **Real-Time Voice**         | Talk naturally with Gemini using your microphone    |
| 🌐 **Multilingual**             | English, Telugu, or natural English + Telugu        |
| ⚡ **Low-Latency Conversation**  | Uses Gemini Live API for real-time interaction      |
| 🔐 **Secure API Key**           | Your permanent Gemini key never reaches the browser |
| 🎟️ **Ephemeral Tokens**        | Browser sessions use short-lived, single-use tokens |
| 🔄 **Automatic Model Fallback** | Automatically tries supported Live models           |
| 🖥️ **Browser-Based**           | No desktop application required                     |
| 🎧 **Microphone Support**       | Works with your Windows default audio device        |
| 🩺 **Health Endpoint**          | Quickly check whether the server is running         |
| 🪶 **Lightweight**              | Python backend + simple browser frontend            |

---

## 🧠 How Dhanush AI Works

```text
             🎤 Your Voice
                   │
                   ▼
        ┌─────────────────────┐
        │   Chrome / Edge     │
        │    Dhanush AI UI    │
        └──────────┬──────────┘
                   │
                   │ Request temporary token
                   ▼
        ┌─────────────────────┐
        │    Python Server    │
        │       FastAPI       │
        └──────────┬──────────┘
                   │
             🔐 API Key
                   │
                   ▼
             Gemini API
                   │
          🎟️ Ephemeral Token
                   │
                   ▼
        ┌─────────────────────┐
        │ Gemini Live API     │
        │ Real-Time WebSocket │
        └──────────┬──────────┘
                   │
                   ▼
              🔊 AI Voice
```

### 🔒 Security Design

Your permanent API key is **never embedded in the frontend**.

The flow is:

```text
.env
 │
 ▼
Python Server
 │
 │ Creates temporary token
 ▼
Browser
 │
 │ Uses temporary token
 ▼
Gemini Live API
```

The browser does **not** receive your permanent `GEMINI_API_KEY`.

---

# 🚀 Requirements

Before starting, make sure you have:

* 🪟 Windows 10 or Windows 11
* 🐍 Python **3.10+**
* 🔑 Google Gemini API key with Live API access
* 🌐 Current **Google Chrome** or **Microsoft Edge**
* 🌍 Internet connection
* 🎤 Working microphone

Python should be available through the `py` command in PowerShell.

---

# ⚡ Quick Start

## 1️⃣ Install Python

Download Python from:

https://www.python.org/downloads/windows/

During installation, enable the **Python Launcher** if the installer provides that option.

Verify:

```powershell
py --version
```

You should see something similar to:

```text
Python 3.x.x
```

---

## 2️⃣ Extract the Project

Extract:

```text
dhanush_gemini_web_voice_agent.zip
```

For example:

```text
C:\Users\YourName\Downloads\dhanush_gemini_web_voice_agent
```

Open PowerShell and enter the project:

```powershell
cd "$HOME\Downloads\dhanush_gemini_web_voice_agent"
```

---

## 3️⃣ Create a Virtual Environment

```powershell
py -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then:

```powershell
.\.venv\Scripts\Activate.ps1
```

> 💡 You can also skip activation and directly use `.venv\Scripts\python.exe`.

---

# 📦 4️⃣ Install Dependencies

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install the project dependencies:

```powershell
python -m pip install -r requirements.txt
```

---

# 🔑 5️⃣ Configure Gemini API

Create your `.env` file:

```powershell
Copy-Item .env.example .env
```

Open it:

```powershell
notepad .env
```

Add your Gemini API key:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

### Optional model configuration

```env
GEMINI_MODEL=gemini-3.8-live
GEMINI_AUTO_FALLBACK=true
```

⚠️ **Never commit `.env` to GitHub.**

Your API key should remain private.

---

# ▶️ 6️⃣ Start Dhanush AI

Run:

```powershell
python -m uvicorn server:app --host 127.0.0.1 --port 8000
```

Or simply double-click:

```text
run.bat
```

The automatic launcher can create the virtual environment and install dependencies.

---

# 🌐 7️⃣ Open Dhanush AI

Open Chrome or Edge:

**http://127.0.0.1:8000**

Then:

1. Click **Start**
2. Allow microphone access
3. Start speaking
4. Speak English, Telugu, or both naturally
5. Click **Stop** when finished

🎉 You're now talking with Dhanush AI.

---

# 🤖 Supported Gemini Live Models

When automatic fallback is enabled, Dhanush AI tries the configured model first.

Default fallback order:

```text
1. gemini-3.8-live
2. gemini-3.1-flash-live-preview
3. gemini-2.5-flash-native-audio-preview-12-2025
```

Duplicate model names are automatically removed.

The interface displays the model that successfully connected.

### Automatic fallback behavior

Fallback occurs only when the selected model is:

* unavailable
* not found
* unsupported

Errors such as:

* authentication failures
* network problems
* microphone problems

are shown directly instead of silently switching models.

Disable fallback with:

```env
GEMINI_AUTO_FALLBACK=false
```

Then only:

```env
GEMINI_MODEL=your-model-name
```

will be attempted.

> ⚠️ Gemini Live models must be available for your Google API project and account.

---

# 🗣️ Language Support

Dhanush AI does **not force a single output language**.

The assistant is instructed to follow the user's current language.

For example:

### English

> "Can you explain machine learning?"

### Telugu

> "Machine learning అంటే ఏమిటి?"

### Natural mixed conversation

> "Machine learning అంటే basically computer data నుంచి patterns నేర్చుకోవడం."

Dhanush AI can naturally follow language changes during the conversation.

---

# 🔐 Privacy & Security

Dhanush AI is designed so that your permanent API key stays on the backend.

### Your API key:

```text
.env
   ↓
Python Server
   ↓
Temporary Live Token
   ↓
Browser
```

The browser never receives the permanent Gemini API key.

The `/token` endpoint creates a temporary token constrained by:

* one Live model
* one use
* short session-start window

### Audio recordings

Dhanush AI does **not write audio recordings to disk**.

---

# 🩺 Server Health Check

While the server is running, open:

```text
http://127.0.0.1:8000/health
```

A healthy server returns:

```json
{
  "status": "ok"
}
```

This is useful when debugging whether the Python backend is running correctly.

---

# 🛠️ Troubleshooting

## ❌ Missing API Key

Make sure `.env` exists in the same project directory as `server.py`.

It should contain:

```env
GEMINI_API_KEY=your_actual_key
```

Restart the server after changing `.env`.

---

## 🎤 Microphone Permission Denied

In Chrome or Edge:

1. Open the site
2. Click the permissions icon near the address bar
3. Allow **Microphone**
4. Reload the page
5. Click **Start**

Also check:

```text
Windows Settings
→ Privacy & security
→ Microphone
```

Make sure microphone access is enabled.

---

## 🔊 Wrong Audio Device

Set your preferred microphone as the Windows default:

```text
Settings
→ System
→ Sound
→ Input
```

Then reload Dhanush AI and start a new session.

---

## 🌐 WebSocket Connection Error

Make sure:

* Python server is still running
* You're using the same localhost URL
* Internet access is available
* Firewall/network settings allow the connection
* Gemini Live API is available for your account

You can also check the browser Developer Console for additional details.

After fixing the problem, click **Start** again.

---

## 🤖 Gemini Model Unavailable

Check that:

* Your API key is valid
* Gemini Live API access is enabled
* The selected model is available to your project
* Your Google API environment supports the selected Live model

If automatic fallback is enabled, the UI shows which model successfully connected.

Text-only Gemini models are **not** used as Live API fallbacks.

---

## 📦 Python Installation Error

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Then:

```powershell
python -m pip install -r requirements.txt
```

Also verify:

```powershell
python --version
```

Python 3.10 or newer is recommended.

If you're behind a corporate proxy or restricted network, configure pip for that environment.

---

# 🔌 Port 8000 Already in Use

If port `8000` is already occupied, use another port:

```powershell
python -m uvicorn server:app --host 127.0.0.1 --port 8001
```

Then open:

```text
http://127.0.0.1:8001
```

The browser still communicates with Gemini Live directly for the voice session.

---

# 📁 Project Structure

```text
dhanush_gemini_web_voice_agent/
│
├── server.py
├── requirements.txt
├── .env.example
├── .env
├── run.bat
│
└── static/
    └── index.html
```

### Main components

**`server.py`**

Python/FastAPI backend responsible for:

* serving the web application
* protecting the Gemini API key
* generating temporary Live API tokens
* model selection and fallback

**`static/index.html`**

Browser interface responsible for:

* microphone access
* voice interaction
* Live API connection
* Start/Stop controls
* displaying connection/model status

**`.env`**

Private configuration containing your Gemini API key.

---

# 🚀 Future Ideas

Dhanush AI can be extended into a complete personal AI voice platform.

Possible additions:

* 📞 AI phone-call testing
* 📝 Automatic conversation transcripts
* 💾 Conversation history
* 🧠 Long-term AI memory
* 🔍 Web search
* 📄 Document Q&A
* 🖥️ Desktop automation
* 🗣️ Custom voice/personality
* 👥 Multiple AI agents
* 📊 Call analytics
* 🎧 Audio recording controls
* 📈 Customer-support dashboard
* 🌐 Multi-language support

---

# ❤️ Why Dhanush AI?

Dhanush AI is built around a simple idea:

> **Talk to AI naturally — without treating it like a text box.**

It combines a lightweight Python backend, browser-based voice interaction, and Gemini's real-time capabilities into a simple local application.

---

## ⭐ Project

**Dhanush AI**

Built with:

* 🐍 Python
* ⚡ FastAPI
* 🌐 HTML / JavaScript
* 🎙️ Gemini Live API
* 🔐 Ephemeral authentication
* 🌎 Chrome / Microsoft Edge

---

## 📜 License

Add your preferred license here, for example:

```text
MIT License
```

---

### 💡 If you like the project

⭐ Star the repository
🍴 Fork the project
🐛 Report bugs
💡 Suggest features
🤝 Contribute improvements

**Built with ❤️ by Dhanush**
