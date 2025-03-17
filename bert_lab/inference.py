from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
import pandas as pd
from transformers import pipeline
import sys
app = FastAPI()
# Load classifier once at startup
classifier = pipeline("text-classification", model="./ecommerce_model", tokenizer="./ecommerce_model")

@app.post("/ask")
async def ask_question(request: Request):
    try:
        # Get user input
        data = await request.json()
        user_input = data.get("question", "")

        # Perform classification
        result = classifier(user_input)
        predicted_label = result[0]['label']
        score = result[0]['score']

        # Map label to category
        label_map = {
            "LABEL_0": "Product Inquiry",
            "LABEL_1": "Order Management",
            "LABEL_2": "Customer Support"
        }

        category = label_map.get(predicted_label, "Unknown Category")

        return HTMLResponse(
            content=f"<div class='response'>{category} (Score: {score:.2f})</div>",
            status_code=200
        )

    except Exception as e:
        return HTMLResponse(content=f"<div class='response'>Error: {str(e)}</div>", status_code=500)
@app.get("/", response_class=HTMLResponse)
async def serve_html():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Chat with AI</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
            }
            textarea, button, .response {
                width: 80%;
                max-width: 500px;
                margin: 10px 0;
            }
            textarea {
                height: 100px;
                padding: 10px;
            }
            button {
                padding: 10px;
                background-color: blue;
                color: white;
                border: none;
                cursor: pointer;
            }
            .response {
                padding: 10px;
                border: 1px solid #ccc;
                background-color: #f9f9f9;
                white-space: pre-wrap;  /* Ensure text is formatted correctly */
                min-height: 50px;
            }
        </style>
    </head>
    <body>
        <h1>DEMO model BERT bert-base-multilingual-cased</h1>
        <h2>มีดาต้าเซตประมาณ 4000 ดาต้าเซต </h2>
        <h1>หัวข้อสนทนาใช้เกณฑ์ในการแยกดังนี้</h1>
        <ul>
            <li><strong>การสนับสนุนลูกค้า (Customer Support)</strong> เป็นหมวดหมู่กว้างที่ครอบคลุมบริการหลายประเภท รวมถึงปัญหาการชำระเงิน (Payment issues) และการสนับสนุนด้านเทคนิค (Technical support)</li>
            <li><strong>การจัดการคำสั่งซื้อ (Order Management)</strong> ครอบคลุมการติดตามคำสั่งซื้อ, การยกเลิก, สถานะคำสั่งซื้อ และรายละเอียดหมายเลขคำสั่งซื้อ</li>
            <li><strong>สอบถามเกี่ยวกับสินค้า (Product Inquiry)</strong> มุ่งเน้นไปที่คำถามเกี่ยวกับตัวสินค้าเองก่อนตัดสินใจซื้อ เช่น คุณลักษณะของสินค้า, ความพร้อมในการจำหน่าย, ราคา, โปรโมชั่น และรายละเอียดสินค้า</li>
        </ul>
        <textarea id="question" placeholder="Type your question..."></textarea>
        <button onclick="askQuestion()">Ask</button>
        <div class="response" id="answer"></div>
        <script>
            async function askQuestion() {
                const question = document.getElementById("question").value;
                if (!question.trim()) return;
                document.getElementById("answer").innerText = "Loading...";

                const response = await fetch("/ask", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ question })
                });

                const result = await response.text();
                document.getElementById('answer').innerHTML = result; // Update the div with the full response
            }
        </script>
    </body>
    </html>
    """
    
    




