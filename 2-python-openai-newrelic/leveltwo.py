# import the New Relic Python Agent
import newrelic.agent
import os
from openai import OpenAI
from flask import Flask, render_template, request
import markdown

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

app = Flask(__name__)

# initialize the New Relic Python agent
newrelic.agent.initialize('newrelic.ini')

def chatCompletion(prompt):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.8,
        max_tokens=256,
        messages=[
            {"role": "user", "content": prompt}
        ])
    return completion.choices[0].message.content

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/prompt", methods=["POST"])
def prompt():
    input_prompt = request.form.get("input")
    output_prompt = chatCompletion(input_prompt)
    html_output = markdown.markdown(output_prompt)
    return render_template("index.html", output=html_output)

# make the server publicly available via port 5004
# flask --app levelsix.py run --host 0.0.0.0 --port 5004
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5004)
