import os
from flask import Flask, render_template, request
import boto3
from botocore.exceptions import ClientError
import json
import markdown

# Create a Bedrock Runtime client in the AWS Region you want to use.
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# Set the model ID, e.g., Titan Text Premier.¨
model_id = os.environ["MODEL"]  # e.g. "amazon.titan-text-lite-v1"
# model_id = "amazon.titan-text-lite-v1"
# model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
# model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"
# model_id = "anthropic.claude-v2"
# model_id = "anthropic.claude-v2:1"
# model_id = "anthropic.claude-3-haiku-20240307-v1:0"
# model_id = "ai21.jamba-1-5-mini-v1:0"
# model_id = "meta.llama3-8b-instruct-v1:0"
# model_id = "mistral.mistral-7b-instruct-v0:2"
# model_id = "deepseek.r1-v1:0"
# model_id="amazon.nova-micro-v1:0"

app = Flask(__name__, template_folder="../templates",
            static_folder="../static")

# Read prompts from the prompts.txt file
prompts = []
try:
    with open("../prompts.txt", "r") as file:
        # Skip lines that are empty or comments (starting with //)
        prompts = [line.strip() for line in file if line.strip()
                   and not line.startswith("//")]
except Exception as e:
    print(f"Error reading prompts file: {e}")

# taking the input from the user and returning the response from AWS Bedrock


def chatCompletion(prompt):
    print("prompt: "+prompt)
    # Format the request payload using the model's native structure.
    if model_id == "amazon.titan-text-lite-v1":
        native_request = {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 512,
                "temperature": 0.5,
            },
        }
    elif model_id == "anthropic.claude-3-sonnet-20240229-v1:0" or model_id == "anthropic.claude-3-5-sonnet-20240620-v1:0" or model_id == "anthropic.claude-v2":
        # "anthropic.claude-3-haiku-20240307-v1:0"
        native_request = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 512,
            "temperature": 0.5,
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}],
                }
            ],
        }
    else:
        native_request = {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 512,
                "temperature": 0.5,
            },
        }
        native_request3 = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 512,
            "temperature": 0.5,
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}],
                }
            ],
        }
        native_request4 = {
            "max_tokens": 512,
            "temperature": 0.5,
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}],
                }
            ],
        }
        # amazon.nova-micro-v1:0
        native_request5 = [
            {
                "role": "user",
                "content": [{"text": prompt}],
            }
        ]
        native_request6 = [
            {
                "role": "user",
                "content": [{"text": prompt}],
            }
        ]
        conversation = [
            {
                "role": "user",
                "content": [{"text": prompt}],
            }
        ]

    # Convert the native request to JSON.
    request = json.dumps(native_request)

    try:
        # Invoke the model with the request.
        if model_id == "amazon.titan-text-lite-v1" or model_id == "anthropic.claude-3-sonnet-20240229-v1:0" or model_id == "anthropic.claude-3-5-sonnet-20240620-v1:0" or model_id == "anthropic.claude-v2":
            response = client.invoke_model(modelId=model_id, body=request)
        else:
            response = client.invoke_model(modelId=model_id, body=request)

            # response = client.converse(modelId=model_id, messages=conversation)

            # response = client.converse(
            #    modelId="anthropic.claude-v2",
            #    messages=conversation,
            #    inferenceConfig={"maxTokens":2048,"stopSequences":["\n\nHuman:"],"temperature":1,"topP":1},
            #    additionalModelRequestFields={"top_k":250}
            # )

            # nova models
            # Send the message to the model, using a basic inference configuration.
            # amazon.nova-micro-v1:0
            # response = client.converse(
            #    modelId=model_id,
            #    messages=conversation,
            #    inferenceConfig={"maxTokens": 512, "temperature": 0.5, "topP": 0.9},
            # )
            # Extract and print the response text.
            # response_text = response["output"]["message"]["content"][0]["text"]

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        exit(1)

    # Decode the response body.
    # print(f"response: {response}")
    model_response = json.loads(response["body"].read())

    # Extract and print the response text.

    # "amazon.titan-text-lite-v1"
    if model_id == "amazon.titan-text-lite-v1":
        response_text = model_response["results"][0]["outputText"]
    else:
        # "anthropic.claude-3-haiku-20240307-v1:0"
        response_text = model_response["content"][0]["text"]
        # response_text = model_response["results"][0]["outputText"]

        # response_text = response["output"]["message"]["content"][0]["text"]
        # response_text = response["output"]["message"]["content"][0]["text"]

    print(f"response: {response_text}")

    return response_text


@app.route("/")
def home():
    return render_template("index.html", prompts=prompts)


@app.route("/prompt", methods=["POST"])
def prompt():
    input_prompt = request.form.get("input")
    output_prompt = chatCompletion(input_prompt)
    html_output = markdown.markdown(output_prompt)
    return render_template("index.html", input=input_prompt, output=html_output, prompts=prompts)


# make the server publicly available via port 5002
# flask --app levelsix.py run --host 0.0.0.0 --port 5002
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5002)
