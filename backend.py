import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import sqlite3
import io
from PIL import Image
from gtts import gTTS
import base64
from typing import Optional

# 1. Load Environment Variables (Secure API Key)
load_dotenv()

# 2. Initialize Application
app = FastAPI(title="Bharat Nexus Enterprise API")

# 3. Add CORS Middleware (Crucial for HTML/JS Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all HTML files to connect
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

DB_NAME = "bharat_nexus_history.db"

# 4. Database Initialization
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT,
            response TEXT,
            mode TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

# 5. Gemini API Keys (Fetching securely from .env)
api_key = os.getenv("GEMINI_API_KEY")
GEMINI_KEYS = [api_key] if api_key else []

# 6. Core AI Execution Logic with Fallback
def execute_with_gemini_fallback(content_payload):
    if not GEMINI_KEYS:
        raise HTTPException(status_code=500, detail="API Key is missing. Check your .env file.")
        
    last_error = None
    for idx, key in enumerate(GEMINI_KEYS):
        if not key or not key.strip():
            continue
        try:
            genai.configure(api_key=key.strip())
            
            # Using the latest supported Flash model
            model = genai.GenerativeModel('gemini-3.6-flash')
            
            response = model.generate_content(content_payload)
            return response.text
        except Exception as e:
            error_str = str(e)
            last_error = error_str
            if "429" in error_str or "Quota" in error_str:
                continue
            else:
                raise HTTPException(status_code=500, detail=f"AI Error: {error_str}")
                
    raise HTTPException(status_code=429, detail=f"All API keys exhausted. Last Error: {last_error}")

# 7. Main Query Endpoint
@app.post("/api/v1/query")
async def process_multimodal_query(
    prompt: str = Form(...),
    language: str = Form("English"),
    mode: str = Form("search"),
    file: Optional[UploadFile] = File(None)
):
    try:
        # Route logic based on mode
        if mode == "lok":
            system_prompt = f"You are Bharat Lok-Sevak. Help citizens with government schemes and grievances in {language}. User Query: {prompt}"
        elif mode == "ai":
            system_prompt = f"You are Bharat AI, a smart reasoning assistant. Respond in {language}. User Query: {prompt}"
        else:
            system_prompt = f"Provide a detailed search report in {language} for: '{prompt}'"

        content = [system_prompt]

        # Handle File Uploads (Images/PDFs)
        if file and file.filename:
            file_bytes = await file.read()
            if file.filename.lower().endswith(".pdf"):
                content.append({"mime_type": "application/pdf", "data": file_bytes})
            else:
                image = Image.open(io.BytesIO(file_bytes))
                content.append(image)

        # Generate AI Response
        ai_response = execute_with_gemini_fallback(content)

        # Save to History
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO history (query, response, mode) VALUES (?, ?, ?)", (prompt, ai_response, mode))
        conn.commit()
        conn.close()

        return {"status": "success", "response": ai_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 8. Text-to-Speech Endpoint
@app.post("/api/v1/tts")
async def text_to_speech_conversion(prompt: str = Form(...), language: str = Form("English")):
    try:
        lang_code = "hi" if language == "हिन्दी" else "en"
        tts = gTTS(text=prompt[:600], lang=lang_code, slow=False)
        audio_io = io.BytesIO()
        tts.write_to_fp(audio_io)
        audio_io.seek(0)
        audio_base64 = base64.b64encode(audio_io.read()).decode("utf-8")
        return {"status": "success", "audio_base64": audio_base64}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 9. History Retrieval Endpoint
@app.get("/api/v1/history")
def get_history():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, query, response, mode FROM history ORDER BY id DESC LIMIT 15")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "query": r[1], "response": r[2], "mode": r[3]} for r in rows]