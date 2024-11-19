from flask import Flask, request, jsonify
import ollama

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Prompt and Answer</title>
        <style>
            /* General styling */
            body {
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 700px;
                margin: 50px auto;
                background: #ffffff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            h2 {
                text-align: center;
                color: #333333;
            }
            textarea {
                width: 100%;
                height: 100px;
                padding: 10px;
                font-size: 1rem;
                border: 1px solid #ccc;
                border-radius: 5px;
                resize: none;
                margin-top: 10px;
            }
            input[type="button"] {
                display: block;
                margin: 20px auto;
                width: 150px;
                background-color: #007bff;
                color: #ffffff;
                font-size: 1rem;
                font-weight: bold;
                border: none;
                border-radius: 5px;
                padding: 10px;
                cursor: pointer;
                transition: background-color 0.3s ease;
                text-align: center;
            }
            input[type="button"]:hover {
                background-color: #0056b3;
            }
            .response-box {
                margin-top: 20px;
                padding: 15px;
                background: #f9f9f9;
                border-radius: 5px;
                border: 1px solid #ddd;
                font-size: 1rem;
                color: #333;
                white-space: pre-line;
                display: none;
            }
            .spinner {
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
                font-size: 1rem;
                color: #555;
            }
            .spinner div {
                width: 12px;
                height: 12px;
                border-radius: 50%;
                background-color: #007bff;
                animation: bounce 1.4s infinite ease-in-out both;
            }
            .spinner div:nth-child(1) { animation-delay: -0.32s; }
            .spinner div:nth-child(2) { animation-delay: -0.16s; }
            .spinner div:nth-child(3) { animation-delay: 0s; }

            @keyframes bounce {
                0%, 80%, 100% {
                    transform: scale(0);
                } 40% {
                    transform: scale(1);
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Let's solve your coding problem</h2>
            <textarea id="prompt" rows="4" placeholder="Type your prompt here..."></textarea>
            <input type="button" value="Submit" onclick="sendPrompt()">
            <div id="response" class="response-box">
                <div class="spinner" style="display: none;" id="spinner">
                    <div></div>
                    <div></div>
                    <div></div>
                    <span>Processing...</span>
                </div>
            </div>
        </div>

        <script>
            function sendPrompt() {
                const prompt = document.getElementById("prompt").value;
                const responseBox = document.getElementById("response");
                const spinner = document.getElementById("spinner");

                // Hide response and show spinner
                responseBox.style.display = "none";
                spinner.style.display = "flex";
                responseBox.style.display = "block";

                fetch("/generate", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ prompt })
                })
                .then(response => response.json())
                .then(data => {
                    spinner.style.display = "none"; // Hide spinner
                    responseBox.textContent = data.response || "No response received.";
                })
                .catch(error => {
                    spinner.style.display = "none"; // Hide spinner
                    responseBox.textContent = "Error: " + error.message;
                });
            }
        </script>
    </body>
    </html>
    """

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"response": "Prompt is empty."})

    # Generate response using Ollama
    try:
        response = ollama.generate(
            model="qwen2.5-coder:7b",
            prompt=f"Respond to this prompt: {prompt}"
        )
        return jsonify({"response": response.get("response", "No response generated.")})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
