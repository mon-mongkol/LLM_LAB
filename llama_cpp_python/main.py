from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from langchain.prompts import PromptTemplate
from langchain_community.llms import LlamaCpp
import sys
app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

template = """Question: {question}

Answer: Let's work this out in a step by step way to be sure we have the right answer."""

prompt = PromptTemplate.from_template(template)

llm = LlamaCpp(
    model_path="llama-3.1-8b-instruct-q6_k.gguf",
    temperature=0.6,
    max_tokens=200,
    top_p=1,
    verbose=True,
)

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    try:

        response = llm.generate([prompt.format(question=request.question)])
        answer = response.generations[0][0].text.strip()

        return HTMLResponse(content=f"<div class='response'>{answer}</div>", status_code=200)
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
        <h1>DEMO Chat with AI LlamaCpp gguf with python</h1>
        <h2>model name : Unsloth_Llama-3.1-8B-Instruct-Q6_K-GGUF </h2>
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
