print("Import library")
from fastapi import FastAPI, File, UploadFile, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import whisper
import torch
# from TTS.api import TTS

# Import shared models first to initialize them
print("Loading shared models...")
import shared_models

# Import RAG inference modules (will use shared models)
from rag_inference_gdm import qa_chain as qa_chain_gdm, compression_retriever as compression_retriever_gdm, related_question_chain as related_question_chain_gdm
from rag_inference_ckd import qa_chain as qa_chain_ckd, compression_retriever as compression_retriever_ckd, related_question_chain as related_question_chain_ckd
from rag_inference_ppd import qa_chain as qa_chain_ppd, compression_retriever as compression_retriever_ppd, related_question_chain as related_question_chain_ppd

from opencc import OpenCC
import uuid
import edge_tts
import base64
import random
import time
from typing import Optional

print("Finish import")
myuuid = uuid.uuid4()
app = FastAPI()

UPLOAD_FOLDER = "temp"
AUDIO_CLONE = "static"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
#init model here
print("init model")
asr_model = whisper.load_model("medium")
# device = "cuda" if torch.cuda.is_available() else "cpu"
# tts = TTS(model_name="tts_models/zh-CN/baker/tacotron2-DDC-GST").to(device)
cc = OpenCC('s2twp')
print("Finish init model")
def llm_inference_gdm(user_query):
    """GDM (妊娠期糖尿病) inference"""
    question = user_query
    answer = qa_chain_gdm.invoke(question)
    return answer

def llm_inference_ckd(user_query):
    """CKD (慢性腎臟病) inference"""
    question = user_query
    answer = qa_chain_ckd.invoke(question)
    return answer

def llm_inference_ppd(user_query):
    """PPD (產後憂鬱症) inference"""
    question = user_query
    answer = qa_chain_ppd.invoke(question)
    return answer

def llm_inference(user_query, model_type="gdm"):
    """通用inference函數，根據model_type選擇對應的模型"""
    if model_type == "ckd":
        return llm_inference_ckd(user_query)
    elif model_type == "ppd":
        return llm_inference_ppd(user_query)
    else:  # 預設使用 gdm
        return llm_inference_gdm(user_query)

def load_questions():
    with open('questions.txt', 'r', encoding='utf-8') as f:
        questions = [line.strip() for line in f if line.strip()]
    return questions


@app.post("/upload")
async def upload_audio(audio: UploadFile = File(...)):
    if not audio:
        raise HTTPException(status_code=400, detail="沒有音訊檔案")

    # Save uploaded file
    filename = audio.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    with open(filepath, "wb") as buffer:
        content = await audio.read()
        buffer.write(content)

    result = asr_model.transcribe(filepath, language="zh")
    
    # Bạn có thể gọi ASR để chuyển đổi giọng nói thành văn bản ở đây
    # ví dụ: result = my_asr(filepath)
    answer = cc.convert(result['text'])
    return {"text": answer}

@app.get("/ping")
async def ping():
    return {"status": "healthy"}

@app.post("/ask")
async def ask(
    question: str = Form(...),
    role: str = Form(default="unknown"),
    model_type: str = Form(default="gdm"),
    responseWithAudio: str = Form(default="false")
):
    print(f"Question: {question}, Role: {role}, Model: {model_type}, Audio: {responseWithAudio}")
    if not question:
        raise HTTPException(status_code=400, detail="請輸入問題")

    start_time = time.time()
    answer = llm_inference(question, model_type)
    end_time = time.time() - start_time
    print("LLM:",end_time)
    start_time = time.time()
    answer = cc.convert(answer)
    end_time = time.time() - start_time
    print("Convert:",end_time)
    start_time = time.time()
    if responseWithAudio == "true":
        if role == "doctor":
            voices = "zh-CN-YunyangNeural"
        else:
           voices = "zh-CN-XiaoxiaoNeural"
        myuuid = uuid.uuid4()
        audio_name = str(myuuid) + '.mp3'
        filepath = os.path.join(UPLOAD_FOLDER, audio_name)
        tts = edge_tts.Communicate(
                text=answer,
                voice=voices)
        await tts.save(filepath)
        # return JSONResponse({"answer": answer, "audio": audio, "filepath": filepath})
        with open(filepath, 'rb') as audio_file:
            audio_data = audio_file.read()
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        end_time = time.time() - start_time
        print("Audio:",end_time)
        return JSONResponse({"answer": answer, "audio_base64": audio_base64})
    else:
        return JSONResponse({"answer": answer})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5012, debug=True)
