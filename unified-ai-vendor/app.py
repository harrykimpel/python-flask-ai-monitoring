"""
Unified AI Vendor Flask Application
Integrates multiple AI vendors with a unified interface
"""

# import the New Relic Python Agent
import newrelic.agent
from dotenv import load_dotenv
import os
import markdown
from flask import Flask, render_template, request, jsonify
from vendor_clients import VendorFactory

# initialize the New Relic Python agent
newrelic.agent.initialize('newrelic.ini')

# Initialize Flask app
app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

# Load environment variables from .env file
load_dotenv()

# Global vendor factory instance
vendor_factory = VendorFactory()


def get_vendor_info():
    """Get available vendors and their models"""
    vendors = {}
    for vendor_name in vendor_factory.get_vendors():
        client = vendor_factory.get_client(vendor_name)
        if client:
            vendors[vendor_name] = {
                "models": client.get_models(),
                "available": client.available
            }
    return vendors


# Read prompts from the prompts.txt file
prompts = []
try:
    with open("../prompts.txt", "r") as file:
        # Skip lines that are empty or comments (starting with //)
        prompts = [line.strip() for line in file if line.strip()
                   and not line.startswith("//")]
except Exception as e:
    print(f"Error reading prompts file: {e}")


@app.route("/")
def home():
    """Render home page with vendor and model options"""
    vendor_info = get_vendor_info()
    return render_template(
        "unified-index.html",
        vendors=vendor_info,
        prompts=prompts,
        default_vendor="openai",
        default_model="gpt-4o-mini"
    )


@app.route("/api/vendors", methods=["GET"])
def get_vendors():
    """API endpoint to get all available vendors and their models"""
    vendor_info = get_vendor_info()
    return jsonify(vendor_info)


@app.route("/api/models", methods=["GET"])
def get_models():
    """API endpoint to get models for a specific vendor"""
    vendor = request.args.get("vendor", "openai").lower()
    client = vendor_factory.get_client(vendor)

    if client:
        return jsonify({
            "vendor": vendor,
            "models": client.get_models(),
            "available": client.available
        })
    else:
        return jsonify({
            "error": f"Unknown vendor: {vendor}"
        }), 400


@app.route("/prompt", methods=["POST"])
def prompt():
    """Handle prompt submission and return AI response"""
    try:
        input_prompt = request.form.get("input", "")
        vendor = request.form.get("vendor", "openai").lower()
        model = request.form.get("model", "")

        if not input_prompt:
            return render_template(
                "unified-index.html",
                error="Please enter a prompt",
                vendors=get_vendor_info(),
                prompts=prompts,
                selected_vendor=vendor,
                selected_model=model
            )

        if not model:
            return render_template(
                "unified-index.html",
                error="Please select a model",
                vendors=get_vendor_info(),
                prompts=prompts,
                selected_vendor=vendor
            )

        # Get the appropriate client
        client = vendor_factory.get_client(vendor)

        if not client:
            return render_template(
                "unified-index.html",
                error=f"Unknown vendor: {vendor}",
                vendors=get_vendor_info(),
                prompts=prompts,
                selected_vendor=vendor,
                selected_model=model
            )

        if not client.available:
            return render_template(
                "unified-index.html",
                error=f"{vendor} client is not available. Please check your API keys and dependencies.",
                vendors=get_vendor_info(),
                prompts=prompts,
                selected_vendor=vendor,
                selected_model=model
            )

        # Get the response from the selected vendor
        print(f"Using vendor: {vendor}, model: {model}")
        output = client.chat_completion(input_prompt, model)

        # Convert markdown to HTML if needed
        html_output = markdown.markdown(output)

        return render_template(
            "unified-index.html",
            input=input_prompt,
            output=html_output,
            vendors=get_vendor_info(),
            prompts=prompts,
            selected_vendor=vendor,
            selected_model=model
        )

    except Exception as e:
        print(f"Error processing prompt: {str(e)}")
        return render_template(
            "unified-index.html",
            error=f"Error processing request: {str(e)}",
            vendors=get_vendor_info(),
            prompts=prompts
        ), 500


@app.route("/api/prompt", methods=["POST"])
def api_prompt():
    """API endpoint for prompt processing (JSON-based)"""
    try:
        data = request.get_json()
        input_prompt = data.get("input", "")
        vendor = data.get("vendor", "openai").lower()
        model = data.get("model", "")

        if not input_prompt:
            return jsonify({"error": "Prompt is required"}), 400

        if not model:
            return jsonify({"error": "Model is required"}), 400

        # Get the appropriate client
        client = vendor_factory.get_client(vendor)

        if not client:
            return jsonify({"error": f"Unknown vendor: {vendor}"}), 400

        if not client.available:
            return jsonify({
                "error": f"{vendor} client is not available. Please check your API keys."
            }), 503

        # Get the response
        output = client.chat_completion(input_prompt, model)

        return jsonify({
            "vendor": vendor,
            "model": model,
            "input": input_prompt,
            "output": output
        })

    except Exception as e:
        print(f"Error in API prompt: {str(e)}")
        return jsonify({
            "error": f"Error processing request: {str(e)}"
        }), 500


if __name__ == "__main__":
    # Run the Flask app
    app.run(host="0.0.0.0", debug=True, port=5002)
