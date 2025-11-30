# Architecture & Implementation Summary

## Project Overview

The **Unified AI Vendor Assistant** is a Flask-based web application that consolidates multiple AI vendor integrations (OpenAI, Azure OpenAI, Google Gemini, GitHub Models, AWS Bedrock) into a single interface with dynamic vendor and model selection.

## Visual System Architecture

### Application Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      Flask Web Application                       │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   User Interface (HTML)                  │  │
│  │  ┌────────────────┐  ┌───────────────────┐              │  │
│  │  │ Vendor Select  │  │ Model Select      │              │  │
│  │  │  (Dropdown)    │  │  (Dynamic Update) │              │  │
│  │  └────────────────┘  └───────────────────┘              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           ▲  │                                  │
│                Form Submit │  │ AJAX Model Update              │
│                           │  │                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  Flask Routes (app.py)                   │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐        │  │
│  │  │    /     │  │ /prompt  │  │ /api/models      │        │  │
│  │  │  (GET)   │  │  (POST)  │  │ /api/prompt      │        │  │
│  │  └──────────┘  └──────────┘  └──────────────────┘        │  │
│  └────────────┬──────────────────────────────────────────────┘  │
│               │                                                  │
│               ▼                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         VendorFactory & Client Selection                 │  │
│  └────────────┬──────────────────────────────────────────────┘  │
│               │                                                  │
│  ┌────────────┼─────────────────┬──────────┬──────────────┐    │
│  │            │                 │          │              │    │
│  ▼            ▼                 ▼          ▼              ▼    │
│ OpenAI    Azure OpenAI       Gemini    GitHub          Bedrock│
│ Client     Client             Client    Models          Client│
│            │                            Client                 │
│  ┌─────────┴────────────────────────────────────────────────┐  │
│  │ External API Calls to Vendors                            │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Class Hierarchy

```
VendorClient (Abstract Base Class)
    │
    ├─ OpenAIClient
    ├─ AzureOpenAIClient
    ├─ GeminiClient
    ├─ GitHubModelsClient
    └─ BedrockClient

VendorFactory
    └─ Creates and manages client instances
```

## File Structure

```
unified-ai-vendor/
├── app.py                 # Main Flask application (150 lines)
├── vendor_clients.py      # Vendor abstraction layer (350+ lines)
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variable template
├── run.sh                # Setup and run script
├── README.md             # Comprehensive documentation
├── QUICKSTART.md         # Quick start guide
├── index.html            # Unified template (kept for reference)
└── (uses ../templates/unified-index.html for actual template)
```

## Core Components

### 1. vendor_clients.py - Vendor Abstraction Layer

**Abstract Base Class**
- `VendorClient`: Abstract class defining the interface

**Concrete Implementations**
- `OpenAIClient`: OpenAI API (6 models)
- `AzureOpenAIClient`: Azure OpenAI (4 models)
- `GeminiClient`: Google Gemini (4 models)
- `GitHubModelsClient`: GitHub Models (7 models)
- `BedrockClient`: AWS Bedrock (10+ models)

**Factory Pattern**
- `VendorFactory`: Creates vendor clients and maintains registry

**Key Features**
- Abstracted `chat_completion()` method
- Dynamic `get_models()` method per vendor
- Error handling and availability checking
- Support for different request/response formats per vendor

### 2. app.py - Flask Application

**Routes**
- `GET /` - Home page with vendor/model selectors
- `POST /prompt` - Form-based prompt submission
- `GET /api/vendors` - JSON endpoint for all vendors
- `GET /api/models` - JSON endpoint for specific vendor models
- `POST /api/prompt` - JSON-based API for prompt processing

**Features**
- Automatic model list updates based on vendor selection
- Markdown rendering of responses
- Error handling with user-friendly messages
- Session management
- Support for both form and API-based interactions

### 3. unified-index.html - Frontend UI

**Components**
- Vendor dropdown selector
- Dynamic model dropdown (updates on vendor change)
- Textarea for prompt input
- Sample prompts list (clickable)
- Response display area with markdown rendering
- Responsive Bootstrap-based design

**Features**
- Real-time vendor availability status
- Loading animation while processing
- Vendor badge in response header
- Mobile-responsive layout
- Bootstrap 5.3 styling
- Custom gradient background

## Key Design Patterns

### 1. Abstract Factory Pattern
- `VendorClient` abstract base class
- Concrete implementations for each vendor
- `VendorFactory` for client instantiation

### 2. Strategy Pattern
- Different `chat_completion()` implementations per vendor
- Different `get_models()` implementations per vendor

### 3. Dependency Injection
- Vendor clients injected into routes
- Environment variables passed to clients

## Supported Vendors & Models

### OpenAI (6 models)
- gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-4, gpt-3.5-turbo

### Azure OpenAI (4 models)
- gpt-4o, gpt-4-turbo, gpt-4, gpt-35-turbo

### Google Gemini (4 models)
- gemini-2.0-flash, gemini-1.5-pro, gemini-1.5-flash, gemini-1.0-pro

### GitHub Models (7 models)
- gpt-4o, gpt-4o-mini, claude-3.5-sonnet, claude-3-haiku, meta-llama, mistral-large

### AWS Bedrock (10+ models)
- Amazon Titan, Anthropic Claude (3 versions), Meta Llama, Mistral, AI21 Jamba

## Environment Variables

```env
# OpenAI
OPENAI_API_KEY=sk-...

# Azure
AZURE_OPENAI_API_ENDPOINT=https://...
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_MODEL_NAME=gpt-4o
AZURE_OPENAI_DEPLOYMENT_NAME=...

# Gemini
GEMINI_API_KEY=...

# GitHub
GITHUB_TOKEN=ghp_...

# AWS (via aws configure or environment)
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
```

## API Endpoints

### Get All Vendors and Models
```
GET /api/vendors
Response: {
  "openai": {
    "models": [...],
    "available": true
  },
  ...
}
```

### Get Models for Vendor
```
GET /api/models?vendor=openai
Response: {
  "vendor": "openai",
  "models": [...],
  "available": true
}
```

### Submit Prompt (JSON API)
```
POST /api/prompt
Content-Type: application/json

{
  "vendor": "openai",
  "model": "gpt-4o-mini",
  "input": "What is AI?"
}

Response: {
  "vendor": "openai",
  "model": "gpt-4o-mini",
  "input": "What is AI?",
  "output": "AI is..."
}
```

## Error Handling

- **Vendor Not Available**: Shows availability status in UI
- **Missing API Key**: Graceful error message
- **Invalid Model**: API returns 400 error
- **API Failures**: Catches exceptions and returns friendly messages
- **Form Validation**: Client-side and server-side validation

## Extensibility

### Adding a New Vendor

1. Create class extending `VendorClient`:
```python
class NewVendorClient(VendorClient):
    def chat_completion(self, prompt: str, model: str) -> str:
        # Implementation
        pass
    
    def get_models(self) -> list:
        return ["model1", "model2"]
```

2. Register in `VendorFactory`:
```python
VendorFactory._clients['newvendor'] = NewVendorClient
```

3. Add environment variables to `.env.example`

4. Test and update documentation

## Security Considerations

- API keys stored in `.env` (not in code)
- `.env` excluded from version control
- Environment variables passed securely to clients
- No sensitive data logged or displayed
- HTTPS recommended for production

## Performance Characteristics

- **Startup Time**: ~1-2 seconds
- **Response Time**: Depends on vendor API (typically 1-30 seconds)
- **Memory Usage**: ~50MB at idle
- **Concurrent Requests**: Flask dev server handles 1 at a time
  (use Gunicorn/uWSGI for production)

## Deployment Recommendations

### Development
```bash
python app.py
```

### Production
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker
- Create Dockerfile with Python 3.9+
- Install dependencies from requirements.txt
- Mount .env file
- Expose port 5000

### Cloud Platforms
- Azure App Service
- AWS App Runner
- Google Cloud Run
- Heroku (with Procfile)

## Testing

### Manual Testing
1. Start app: `python app.py`
2. Test each vendor with different models
3. Verify markdown rendering
4. Test API endpoints with curl
5. Check error handling

### Automated Testing (Future)
- Unit tests for vendor clients
- Integration tests for routes
- API contract tests

## Monitoring & Observability

### Logging
- Vendor selection logged
- API calls logged
- Errors logged with stack traces

### Metrics (Future)
- Request count per vendor
- Response time per vendor
- Error rate per vendor
- Model usage statistics

### Integration Points
- New Relic (mentioned in requirements)
- CloudWatch (AWS)
- Application Insights (Azure)
- Stackdriver (GCP)

## Limitations & Future Enhancements

### Current Limitations
- Single-threaded Flask development server
- No request/response history
- No rate limiting
- No authentication
- Limited error recovery

### Future Enhancements
1. **User Accounts**: Session management, history
2. **Streaming Responses**: Server-sent events for long responses
3. **Cost Tracking**: Monitor API usage and costs
4. **Advanced Filtering**: Filter models by cost, capability, etc.
5. **Batch Processing**: Submit multiple prompts at once
6. **Custom System Prompts**: Allow user-defined system context
7. **Model Fine-tuning**: Track and manage fine-tuned models
8. **Analytics Dashboard**: Visualize usage patterns

## Version History

- **v1.0** (Current): Multi-vendor unified interface with dropdown selectors
  - 5 vendors (OpenAI, Azure, Gemini, GitHub, Bedrock)
  - 30+ models total
  - Dynamic model selection
  - REST API support
  - Responsive web UI

## Support & Documentation

- **README.md**: Comprehensive guide and troubleshooting
- **QUICKSTART.md**: 5-minute setup guide
- **API Examples**: REST API usage examples in README
- **Code Comments**: Inline documentation in source code
- **Environment Setup**: .env.example with all configuration options
