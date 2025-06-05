# ---------------------------------------- Install Node.js for the Front End ----------------------------------
# https://nodejs.org/en
# C:\Program Files\nodejs\

# From PowerShell, run the following command (This creates a folder chat-frontend with everything React needs):
# Change directories to the root folder of your project where you want to create the React app.
#   *cd "C:\Users\Laptop\Desktop\Coding\LLM\Personal Projects\LLM - Code Commenter"
# Run the following command to create a new React app:
#   *npx create-react-app chat-frontend
#   *cd chat-frontend
#   *npm install axios


# The dictory structure should look like this:
# my-project/
# ├── backend/
# │   └── App.py        # Python backend (Flask)
# ├── .env              # Environment variables LLM API credentials 
# ├── requirements.txt  # Python dependencies
# ├── chat-frontend/
# │   ├── package.json  # React app configuration
# │   └── src/  
# │       ├── App.js    # React frontend (JavaScript)
# │       └── App.css   # CSS styles for the frontend
# └── README.md


# ------------------------------------ Installations ----------------------------------
# pip install boto3 
# pip install flask
# pip install flask-cors
# pip install pandas
# pip install python-dotenv


# ------------------------------------ Packages ----------------------------------
import anthropic
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os




# ------------------------------------ Configure AWS Bedrock Model & Keys ----------------------------------
# https://console.aws.amazon.com/
# Request access to the Bedrock service in your AWS account.

# Get the access and secret keys from your AWS account.
#   *Go to the IAM dashboard
#   *Click Services → Search for IAM → Open Users.
#   *Create a new user or select an existing user.
#   *Select your user → Security credentials tab.
#   *Click Create access key (Located at the top right under the Summary section).
#   *Copy the Access key ID and Secret access key → Select 'Application runniing on an AWS compute service'
#   *Store the keys in the .env file 


# ------------------------------------ Load Environment Variables ----------------------------------
env_path = r"C:\Users\Laptop\Desktop\Coding\LLM\Personal Projects\Environment Variables\project.env"
load_dotenv(dotenv_path=env_path, override=True)

aws_access_key = os.getenv("AWS_ACCESS_KEY")
aws_secret_key = os.getenv("AWS_SECRET_KEY")
# Default to "us-east-1" if not set in .env file
aws_region = os.getenv("AWS_REGION", "us-east-1")

if not aws_access_key or not aws_secret_key:
    raise ValueError("Missing AWS credentials in .env file")

openai_api_key = os.getenv('OPENAI_API_KEY')            # https://openai.com/api/
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')      # https://console.anthropic.com/ 
google_api_key = os.getenv('GOOGLE_API_KEY')            # https://ai.google.dev/gemini-api
huggingface_token = os.getenv('HUGGINGFACE_TOKEN')      # https://huggingface.co/settings/tokens

print("Checking API Keys...\n")
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:10]}")
else:
    print("OpenAI API Key not set")
    
if anthropic_api_key:
    print(f"Anthropic API Key exists and begins {anthropic_api_key[:10]}")
else:
    print("Anthropic API Key not set")

if google_api_key:
    print(f"Google API Key exists and begins {google_api_key[:10]}")
else:
    print("Google API Key not set")

if huggingface_token:
    print(f"Hugging Face Token exists and begins {huggingface_token[:10]}")
else:
    print("Hugging Face Token not set")
print("\n------------------------------------\n")


# ------------------------------------ Connect to API Platforms ----------------------------------
openai = OpenAI()
claude = anthropic.Anthropic()
# OPENAI_MODEL = "gpt-4o"
# CLAUDE_MODEL = "claude-3-5-sonnet-20240620"

# Lower cost models:
OPENAI_MODEL = "gpt-4o-mini"
CLAUDE_MODEL = "claude-3-haiku-20240307"

# Code Qwen model
code_qwen = "Qwen/CodeQwen1.5-7B-Chat"

# Login to Hugging Face and configure the Inference Endpoint
# Get the Hugging Face endpoint URLs for the models
CODE_QWEN_URL = "https://qe1ht18838pdue80.us-east-1.aws.endpoints.huggingface.cloud"



# ------------------------------------ Bot Configuration ----------------------------------
# Store per-bot chat history in memory
chat_histories = {
    "gpt-4": [],
    "claude": [],
    "mixtral": []
}

def get_system_message(language):
    """
    This function generates a system message for the LLM to rewrite Python code in the specified language.
    It includes instructions for the LLM to focus on performance and correctness,
    ensuring that the rewritten code produces identical output in the fastest possible time.
    Args:
        language (str): The target programming language for the optimization.
    Returns:
        str: A formatted system message that includes instructions for the LLM.
    """
    return f"""
    You are a programming assistant and will be given code to help fix or troubleshoot. Respond in markdown 
    code blocks with the specified language showing suggested changes or suggestions.  At the bottom of your
    response, always include the full code with the changes you made embedded in one code block so that it
    can be copied and pasted directly into the code editor.
    """


# ------------------------------------ Messages for LLM ----------------------------------
def messages_for(user_message):
    """
    This function generates a list of messages for the LLM, including a system message and a user prompt.
    Args:
        python_code (str): The Python code to be rewritten in the target language.
        language (str): The target programming language for the optimization.
    Returns:
        list: A list of dictionaries representing the messages for the LLM.
    """

    return [
        {"role": "system", "content": get_system_message()},
        {"role": "user", "content": user_message}
    ]


# ------------------------------------ Claude Prompt ----------------------------------
# def optimize_gpt(model, python_code, language):
#     """
#     This function optimizes Python code by sending it to the OpenAI API for rewriting in the specified language.
#     It streams the response from the API and prints it to the console in real-time.
#     Args:
#         python_code (str): The Python code to be optimized.
#         language (str): The target programming language for the optimization.
#     Returns:
#         None
#     """
    
#     stream = openai.chat.completions.create(
#         model=model,  
#         messages=messages_for(python_code, language),
#         stream=True # Enable streaming to get real-time response and make it look more human-like
#     )
#     reply = ""
#     # Iterate through the streamed response and print each fragment to make it look more human-like
#     for chunk in stream:
#         fragment = chunk.choices[0].delta.content or ""
#         reply += fragment
#         print(fragment, end='', flush=True)
#     write_output(reply, language)



# def call_gpt(model, system_instruction, chat_history):
#     """
#     Call OpenAI GPT with the given system instruction and pass in conversation history.  
#     Every call to GPT requires the full history because each call is stateless or 
#     independent. The model does not remember the previous conversation.  The history is 
#     passed in as a list of dictionaries.  Each dictionary contains the role (user or
#     assistant) and the content of the message.
#     """
#     # Example message format for ChatGPT passing in it's full conversation history:
#     # messages = [
#     #     {"role": "system", "content": "You are a friendly assistant that answers questions clearly."},
#     #     {"role": "user", "content": "Hi there!"},
#     #     {"role": "assistant", "content": "Hello! How can I help you today?"},
#     #     {"role": "user", "content": "What's the capital of France?"},
#     #     {"role": "assistant", "content": "The capital of France is Paris."},
#     #     {"role": "user", "content": "Can you tell me a fun fact about it?"}
#     # ]

#     # "system" - Sets behavior, tone, or persona of the assistant. 
#     # "user" - Represents the input from the human user.  In this case, the human will be Google's 'Gemini' bot.
#     # "assistant" - The model's (ChatGPT's) responses to the user.

#     messages = [{"role": "system", "content": system_instruction}]
#     messages.extend(chat_history)
#     completion = openai.chat.completions.create(
#         model=model, 
#         messages=messages
#     )

#     # Return the assistant's response which is at index 0
#     return completion.choices[0].message.content.strip()





















# ------------------------------------ Output Response ----------------------------------
app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "http://localhost:3000"}})



@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '').strip()
    selected_bot = data.get('bot', '').strip().lower()

    if not user_message:
        return jsonify({'error': 'Empty message'}), 400
    if not selected_bot:
        return jsonify({'error': 'Bot name is required'}), 400
    if selected_bot not in chat_histories:
        return jsonify({'error': f"Unknown bot: {selected_bot}"}), 400

    try:
        chat_histories[selected_bot].append({"role": "user", "content": user_message})

        if selected_bot == "gpt-4":
            messages = [{"role": "system", "content": "You are a helpful assistant."}] + chat_histories[selected_bot]
            response = openai.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages
            )
            reply = response.choices[0].message.content.strip()

        elif selected_bot == "claude":
            # Claude: pass structured messages
            response = claude.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=1000,
                temperature=0.7,
                messages=chat_histories[selected_bot]
            )
            reply = response.content[0].text.strip()

        elif selected_bot == "qwen":
            import requests
            hf_headers = {
                "Authorization": f"Bearer {huggingface_token}",
                "Content-Type": "application/json"
            }
            full_prompt = "\n".join([f"{m['role']}: {m['content']}" for m in chat_histories[selected_bot]])
            hf_payload = {
                "inputs": full_prompt,
                "parameters": {"max_new_tokens": 200}
            }

            hf_response = requests.post(CODE_QWEN_URL, headers=hf_headers, json=hf_payload)
            print("HF raw response:", hf_response.text)
            reply = hf_response.json().get('generated_text', 'No reply from model.')

        else:
            return jsonify({'error': f"Bot not implemented: {selected_bot}"}), 400

        chat_histories[selected_bot].append({"role": "assistant", "content": reply})
        return jsonify({'reply': reply})

    except Exception as e:
        import traceback
        traceback.print_exc()  # Logs full error in terminal
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)