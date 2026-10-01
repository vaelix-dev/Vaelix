from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

# Serve the frontend
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Vaelix Core</title>
        <style>
            body { background: #0b0f19; color: white; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .container { width: 80%; max-width: 600px; }
            #chat { height: 400px; border: 1px solid #333; overflow-y: scroll; padding: 10px; margin-bottom: 10px; background: #1a1f2e; }
            input { width: 70%; padding: 10px; }
            button { padding: 10px 20px; cursor: pointer; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2 style="text-align:center;">Vaelix Core</h2>
            <div id="chat"></div>
            <input type="text" id="userInput" placeholder="Type here...">
            <button onclick="sendMessage()">Send</button>
        </div>
        <script>
            async function sendMessage() {
                const input = document.getElementById('userInput');
                const chat = document.getElementById('chat');
                if (!input.value) return;
                
                // Add user message
                chat.innerHTML += `<div><strong>You:</strong> ${input.value}</div>`;
                input.value = '';
                
                // Send to server
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: input.value})
                });
                const data = await response.json();
                
                // Add AI response
                chat.innerHTML += `<div><strong>Vaelix:</strong> ${data.response}</div>`;
                chat.scrollTop = chat.scrollHeight;
            }
        </script>
    </body>
    </html>
    """

@app.post("/chat")
async def chat(request: dict):
    message = request.get("message", "")
    # Simple placeholder response for now - we will add AI logic next
    return {"response": f"You said: {message}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
