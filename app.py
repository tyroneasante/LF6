from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# List to store the chat history
chatHistory = []

# Configure root route to handle both GET and POST requests
@app.route("/", methods=["GET", "POST"])
def index():
    # Handling GET request to display the chat history
    if request.method == "GET":
        return render_template("index.html", chat=chatHistory)
    # Handling POST request to process user input and get chatbot response
    elif request.method == "POST":
        # Getting JSON data from the request
        postRequestData = request.get_json()
        prompt = postRequestData['prompt']

        # Configuring parameters for the OpenAI Chat API
        url = 'http://localhost:11434/api/chat'
        model = 'llama2:13b'

        # Add context inbetween every prompt, so llama doesnt forget
        context = """
        You are a customer service bot, that is only able to answer questions about how to fix problems related to the internet.
        If a question is not related to internet, you answer with the following text: 'I'm sorry, i can only answer questions related to internet.'
        """

        chatHistory.append({'role': 'system', 'content': context})
        # Adding user's prompt to the chat history
        chatHistory.append({'role': 'user', 'content': prompt})

        # Parameters for the Chat API request
        requestParams = {
            'model': model,
            'messages': [{'role': 'system', 'content': context}] + chatHistory,
            'stream': False
        }

        # Making a POST request to the llama2 API
        responseJSON = requests.post(url, json=requestParams)

        # Getting content from llama2 response
        responseText = json.loads(responseJSON.text)['message']['content']

        # Adding assistant's response to the chat history
        chatHistory.append({'role': 'assistant', 'content': responseText})

        # Returning the updated chat history as a JSON response
        return jsonify(chatHistory)