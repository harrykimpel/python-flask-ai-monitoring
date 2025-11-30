# Quick Start Guide - Unified AI Vendor Assistant

## 5-Minute Setup

### Step 1: Navigate to the Directory
```bash
cd unified-ai-vendor
```

### Step 2: Run the Setup Script
```bash
./run.sh
```

This will:
- Create a Python virtual environment
- Install all dependencies
- Create a `.env` file from the template
- Exit and wait for configuration

### Step 3: Configure Your API Keys

Edit the `.env` file and add your API keys:

```bash
# For OpenAI
OPENAI_API_KEY=sk-... (from https://platform.openai.com/api-keys)

# For Google Gemini
GEMINI_API_KEY=... (from https://aistudio.google.com/app/apikeys)

# For GitHub Models
GITHUB_TOKEN=ghp_... (from https://github.com/settings/tokens)

# For Azure OpenAI (optional)
AZURE_OPENAI_API_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_MODEL_NAME=gpt-4o
AZURE_OPENAI_DEPLOYMENT_NAME=...

# For AWS Bedrock (optional)
# Run: aws configure
```

### Step 4: Start the Application
```bash
./run.sh
```

Open http://localhost:5000 in your browser!

## Usage

1. **Select a Vendor** - Choose from: OpenAI, Azure, Gemini, GitHub, Bedrock
2. **Pick a Model** - Models update automatically based on vendor
3. **Enter Your Question** - Type or select from sample prompts
4. **Click Submit** - Get instant AI responses

## Key Features

- 🔄 Switch between AI vendors instantly
- 🚀 Multiple models per vendor
- 📝 Pre-configured sample prompts
- 📱 Responsive mobile design
- 💬 Real-time markdown rendering
- 🔌 REST API for programmatic access

## API Examples

### Get All Vendors
```bash
curl http://localhost:5000/api/vendors
```

### Submit a Prompt (JSON)
```bash
curl -X POST http://localhost:5000/api/prompt \
  -H "Content-Type: application/json" \
  -d '{
    "vendor": "openai",
    "model": "gpt-4o-mini",
    "input": "What is AI?"
  }'
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Vendor shows "Unavailable" | Check your .env file has the correct API key |
| "ModuleNotFoundError" | Run `pip install -r requirements.txt` again |
| Port 5000 already in use | Edit app.py and change port number at the bottom |
| Models not showing | Make sure vendor is selected and available |

## Supported Vendors

### OpenAI ⭐
- Models: GPT-4o, GPT-4, GPT-3.5-Turbo
- Key: OPENAI_API_KEY

### Google Gemini ✨
- Models: Gemini 2.0 Flash, 1.5 Pro, 1.5 Flash
- Key: GEMINI_API_KEY

### GitHub Models 🐙
- Models: GPT-4o, Claude 3.5, Meta Llama, Mistral
- Key: GITHUB_TOKEN

### Azure OpenAI ☁️
- Models: GPT-4o, GPT-4-Turbo
- Keys: AZURE_OPENAI_* environment variables

### AWS Bedrock 🔥
- Models: Claude, Llama, Mistral, Titan
- Setup: `aws configure`

## Next Steps

- Customize the prompt templates in `../prompts.txt`
- Add your own vendor integrations in `vendor_clients.py`
- Deploy to production (see README.md for details)
- Integrate with New Relic for observability

For detailed documentation, see `README.md`
