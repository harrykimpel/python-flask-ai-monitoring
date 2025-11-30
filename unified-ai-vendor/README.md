# Unified AI Vendor Assistant

A Flask-based web application that provides a unified interface to interact with multiple AI vendors including OpenAI, Azure OpenAI, Google Gemini, GitHub Models, and AWS Bedrock. Users can easily switch between different AI vendors and models through an intuitive dropdown interface.

## Features

- **Multi-Vendor Support**: OpenAI, Azure OpenAI, Google Gemini, GitHub Models, AWS Bedrock
- **Dynamic Model Selection**: Automatically updates available models based on selected vendor
- **Unified Interface**: Single web UI for all AI vendors
- **Sample Prompts**: Pre-configured prompts for quick testing
- **Markdown Rendering**: Responses are rendered as formatted HTML
- **REST API**: JSON-based endpoints for programmatic access
- **Error Handling**: Graceful error messages when vendors are unavailable
- **Responsive Design**: Works on desktop and mobile devices

## Directory Structure

```
unified-ai-vendor/
├── app.py                 # Main Flask application
├── vendor_clients.py      # AI vendor client abstractions
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment configuration
├── README.md             # This file
├── index.html            # Main HTML template (in ../templates/)
└── static/               # Static assets (CSS, JS) in parent directory
```

## Installation

### 1. Clone or Download the Repository

```bash
cd unified-ai-vendor
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Then edit `.env` and add your API keys:

```env
# OpenAI
OPENAI_API_KEY=sk-...

# Azure OpenAI
AZURE_OPENAI_API_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-key...
AZURE_OPENAI_MODEL_NAME=gpt-4o
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment

# Google Gemini
GEMINI_API_KEY=your-key...

# GitHub Models
GITHUB_TOKEN=ghp_...

# AWS Bedrock
# Configure via AWS CLI: aws configure
# Or set environment variables:
# export AWS_ACCESS_KEY_ID=...
# export AWS_SECRET_ACCESS_KEY=...
```

## Usage

### Running the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Web Interface

1. **Select a Vendor**: Choose your AI vendor from the dropdown
2. **Select a Model**: Pick a model for the selected vendor (options update automatically)
3. **Enter Your Prompt**: Type your question or use a sample prompt
4. **Submit**: Click the Submit button to get a response

### API Endpoints

#### Get All Vendors and Models

```bash
curl http://localhost:5000/api/vendors
```

Response:

```json
{
  "openai": {
    "models": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"],
    "available": true
  },
  "gemini": {
    "models": ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash", "gemini-1.0-pro"],
    "available": true
  },
  ...
}
```

#### Get Models for Specific Vendor

```bash
curl "http://localhost:5000/api/models?vendor=openai"
```

#### Submit Prompt (JSON API)

```bash
curl -X POST http://localhost:5000/api/prompt \
  -H "Content-Type: application/json" \
  -d '{
    "vendor": "openai",
    "model": "gpt-4o-mini",
    "input": "What is AI?"
  }'
```

Response:

```json
{
  "vendor": "openai",
  "model": "gpt-4o-mini",
  "input": "What is AI?",
  "output": "Artificial Intelligence (AI) is..."
}
```

## Vendor Configuration

### OpenAI

**Required:** `OPENAI_API_KEY`

Get your API key from: <https://platform.openai.com/api-keys>

Available Models:

- gpt-4o
- gpt-4o-mini
- gpt-4-turbo
- gpt-4
- gpt-3.5-turbo

### Azure OpenAI

**Required:**

- `AZURE_OPENAI_API_ENDPOINT`
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_MODEL_NAME`
- `AZURE_OPENAI_DEPLOYMENT_NAME`

Setup: <https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/create-resource>

Available Models:

- gpt-4o
- gpt-4-turbo
- gpt-4
- gpt-35-turbo

### Google Gemini

**Required:** `GEMINI_API_KEY`

Get your API key from: <https://aistudio.google.com/app/apikeys>

Available Models:

- gemini-2.0-flash
- gemini-1.5-pro
- gemini-1.5-flash
- gemini-1.0-pro

### GitHub Models

**Required:** `GITHUB_TOKEN`

Create a token at: <https://github.com/settings/tokens>

Available Models:

- gpt-4o
- gpt-4o-mini
- claude-3.5-sonnet
- claude-3-haiku
- meta-llama-3.1-405b-instruct
- meta-llama-3.1-70b-instruct
- mistral-large

### AWS Bedrock

**Required:** AWS credentials configured

Setup: <https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html>

```bash
aws configure
```

Available Models:

- amazon.titan-text-lite-v1
- amazon.titan-text-express-v1
- anthropic.claude-3-5-sonnet-20240620-v1:0
- anthropic.claude-3-opus-20240229-v1:0
- anthropic.claude-3-sonnet-20240229-v1:0
- anthropic.claude-3-haiku-20240307-v1:0
- meta.llama3-70b-instruct-v1:0
- meta.llama3-8b-instruct-v1:0
- mistral.mistral-7b-instruct-v0:2
- ai21.jamba-1-5-mini-v1:0

## Architecture

### vendor_clients.py

Provides abstraction layer for all AI vendors:

- `VendorClient`: Abstract base class
- `OpenAIClient`: OpenAI API client
- `AzureOpenAIClient`: Azure OpenAI client
- `GeminiClient`: Google Gemini client
- `GitHubModelsClient`: GitHub Models client
- `BedrockClient`: AWS Bedrock client
- `VendorFactory`: Factory pattern for client instantiation

### app.py

Flask application with routes:

- `GET /`: Home page with vendor/model selectors
- `POST /prompt`: Form-based prompt submission
- `GET /api/vendors`: List all vendors and models
- `GET /api/models`: Get models for a specific vendor
- `POST /api/prompt`: JSON-based prompt submission

## Troubleshooting

### Vendor Shows as "Unavailable"

1. Check that the required API key is set in `.env`
2. Verify the required Python package is installed:
   - OpenAI: `pip install openai`
   - Gemini: `pip install google-generativeai`
   - Bedrock: `pip install boto3`

### Models Not Appearing

1. Ensure you've selected a vendor first
2. Check that the vendor is available (not showing as unavailable)
3. Verify the API credentials are correct

### Authentication Errors

1. Check API keys are correctly set in `.env`
2. Verify keys have proper permissions
3. For AWS Bedrock, run `aws configure` with valid credentials

### "Error processing request"

Check the Flask console output for detailed error messages. Common causes:

- Missing API key
- Invalid model name for the vendor
- API rate limiting
- Network connectivity issues

## Extending with New Vendors

To add a new AI vendor:

1. Create a new class in `vendor_clients.py` that extends `VendorClient`
2. Implement `chat_completion()` and `get_models()` methods
3. Register in `VendorFactory._clients` dictionary
4. Add environment variables to `.env.example`
5. Update this README with vendor configuration

Example:

```python
class NewVendorClient(VendorClient):
    def __init__(self):
        # Initialize your client
        pass
    
    def chat_completion(self, prompt: str, model: str) -> str:
        # Send prompt and return response
        pass
    
    def get_models(self) -> list:
        # Return list of available models
        return ["model1", "model2"]
```

Then register it:

```python
VendorFactory._clients['newvendor'] = NewVendorClient
```

## License

This project is part of the New Relic DevRel AI samples collection.

## Support

For issues or questions, refer to the main repository documentation.
