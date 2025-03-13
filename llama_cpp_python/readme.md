ตัวอย่างทดสอบรัน olama cpp ด้วย python จากไฟล์ GGUF โดยตรง ทดสอบแล้วใช้ได้แค่ python 3.8
ดาว์โหลดไฟล์GGUF ไปวางไว้ในโปรเจคก่อน ใช้ docker compose ครับ  https://huggingface.co/Triangle104/Unsloth_Llama-3.1-8B-Instruct-Q6_K-GGUF/tree/main

uvicorn gui:app --host 0.0.0.0 --port 5555 --reload