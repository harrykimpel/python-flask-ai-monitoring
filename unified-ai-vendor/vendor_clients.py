"""
Vendor client abstraction layer for unified AI provider support
Supports: OpenAI, Azure OpenAI, Google Gemini, GitHub Models, AWS Bedrock
"""

import os
from abc import ABC, abstractmethod
from typing import Optional
import json


class VendorClient(ABC):
    """Abstract base class for vendor clients"""

    @abstractmethod
    def chat_completion(self, prompt: str, model: str) -> str:
        """
        Send a prompt to the model and get a response

        Args:
            prompt: The user's input prompt
            model: The model identifier

        Returns:
            The model's response text
        """
        pass

    @abstractmethod
    def get_models(self) -> list:
        """
        Get available models for this vendor

        Returns:
            List of available model identifiers
        """
        pass


class OpenAIClient(VendorClient):
    """OpenAI API client"""

    def __init__(self):
        try:
            from openai import OpenAI

            self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
            self.available = True
        except ImportError:
            self.available = False
            print("OpenAI package not installed")

    def chat_completion(self, prompt: str, model: str) -> str:
        if not self.available:
            return "OpenAI client not available"

        completion = self.client.chat.completions.create(
            model=model, messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content

    def get_models(self) -> list:
        return [
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4-turbo",
            "gpt-4",
            "gpt-3.5-turbo",
        ]


class AzureOpenAIClient(VendorClient):
    """Azure OpenAI API client"""

    def __init__(self):
        try:
            from openai import AzureOpenAI

            self.endpoint = os.environ.get("AZURE_OPENAI_API_ENDPOINT")
            self.api_key = os.environ.get("AZURE_OPENAI_API_KEY")
            self.api_version = os.environ.get(
                "AZURE_OPENAI_API_VERSION", "2024-02-15-preview"
            )

            self.client = AzureOpenAI(
                api_version=self.api_version,
                azure_endpoint=self.endpoint,
                api_key=self.api_key,
            )
            self.available = bool(self.endpoint and self.api_key)
        except ImportError:
            self.available = False
            print("Azure OpenAI package not installed")

    def chat_completion(self, prompt: str, model: str) -> str:
        if not self.available:
            return "Azure OpenAI client not configured"

        completion = self.client.chat.completions.create(
            model=model, messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content

    def get_models(self) -> list:
        # These should match your Azure deployment names
        return [
            "gpt-4o",
            "gpt-4-turbo",
            "gpt-4",
            "gpt-35-turbo",
        ]


class GeminiClient(VendorClient):
    """Google Gemini API client"""

    def __init__(self):
        try:
            import google.generativeai as genai

            api_key = os.environ.get("GEMINI_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
                self.genai = genai
                self.available = True
            else:
                self.available = False
        except ImportError:
            self.available = False
            print("Google Generative AI package not installed")

    def chat_completion(self, prompt: str, model: str) -> str:
        if not self.available:
            return "Gemini client not available"

        model_obj = self.genai.GenerativeModel(model)
        response = model_obj.generate_content(
            prompt,
            generation_config=self.genai.types.GenerationConfig(
                temperature=1.0,
            ),
        )

        response_text = ""
        if response.candidates:
            if response.candidates[0].content.parts:
                if response.candidates[0].content.parts[0].text:
                    response_text = response.candidates[0].content.parts[0].text
        return response_text

    def get_models(self) -> list:
        return [
            "gemini-2.0-flash",
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "gemini-1.0-pro",
        ]


class GitHubModelsClient(VendorClient):
    """GitHub Models API client (OpenAI-compatible)"""

    def __init__(self):
        try:
            from openai import OpenAI

            self.client = OpenAI(
                base_url="https://models.inference.ai.azure.com",
                api_key=os.environ.get("GITHUB_TOKEN"),
            )
            self.available = bool(os.environ.get("GITHUB_TOKEN"))
        except ImportError:
            self.available = False
            print("OpenAI package not installed")

    def chat_completion(self, prompt: str, model: str) -> str:
        if not self.available:
            return "GitHub Models client not configured"

        completion = self.client.chat.completions.create(
            model=model, messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content

    def get_models(self) -> list:
        return [
            "gpt-4o",
            "gpt-4o-mini",
            "claude-3.5-sonnet",
            "claude-3-haiku",
            "meta-llama-3.1-405b-instruct",
            "meta-llama-3.1-70b-instruct",
            "mistral-large",
        ]


class BedrockClient(VendorClient):
    """AWS Bedrock API client"""

    def __init__(self):
        try:
            import boto3

            self.client = boto3.client("bedrock-runtime", region_name="us-east-1")
            self.available = True
        except ImportError:
            self.available = False
            print("Boto3 package not installed")

    def chat_completion(self, prompt: str, model: str) -> str:
        if not self.available:
            return "Bedrock client not available"

        response_text = ""

        try:
            # Handle different model families
            if model.startswith("amazon.titan"):
                native_request = {
                    "inputText": prompt,
                    "textGenerationConfig": {
                        "maxTokenCount": 512,
                        "temperature": 0.5,
                    },
                }
                response = self.client.invoke_model(
                    modelId=model, body=json.dumps(native_request)
                )
                response_body = json.loads(response["body"].read())
                response_text = response_body.get("results", [{}])[0].get("outputText", "")

            elif "claude" in model:
                native_request = {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 512,
                    "messages": [{"role": "user", "content": prompt}],
                }
                response = self.client.invoke_model(
                    modelId=model, body=json.dumps(native_request)
                )
                response_body = json.loads(response["body"].read())
                response_text = response_body.get("content", [{}])[0].get("text", "")

            elif "llama" in model or "mistral" in model:
                native_request = {
                    "prompt": prompt,
                    "max_gen_len": 512,
                    "temperature": 0.5,
                }
                response = self.client.invoke_model(
                    modelId=model, body=json.dumps(native_request)
                )
                response_body = json.loads(response["body"].read())
                response_text = response_body.get("generation", "")

            elif "jamba" in model:
                native_request = {
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 512,
                }
                response = self.client.invoke_model(
                    modelId=model, body=json.dumps(native_request)
                )
                response_body = json.loads(response["body"].read())
                response_text = (
                    response_body.get("choices", [{}])[0].get("message", {}).get("content", "")
                )

            else:
                response_text = "Unknown Bedrock model"

        except Exception as e:
            response_text = f"Error calling Bedrock: {str(e)}"

        return response_text

    def get_models(self) -> list:
        return [
            "amazon.titan-text-lite-v1",
            "amazon.titan-text-express-v1",
            "anthropic.claude-3-5-sonnet-20240620-v1:0",
            "anthropic.claude-3-opus-20240229-v1:0",
            "anthropic.claude-3-sonnet-20240229-v1:0",
            "anthropic.claude-3-haiku-20240307-v1:0",
            "meta.llama3-70b-instruct-v1:0",
            "meta.llama3-8b-instruct-v1:0",
            "mistral.mistral-7b-instruct-v0:2",
            "ai21.jamba-1-5-mini-v1:0",
        ]


class VendorFactory:
    """Factory for creating vendor clients"""

    _clients = {
        "openai": OpenAIClient,
        "azure": AzureOpenAIClient,
        "gemini": GeminiClient,
        "github": GitHubModelsClient,
        "bedrock": BedrockClient,
    }

    @classmethod
    def get_client(cls, vendor: str) -> Optional[VendorClient]:
        """
        Get a client for the specified vendor

        Args:
            vendor: The vendor name (openai, azure, gemini, github, bedrock)

        Returns:
            A VendorClient instance or None if vendor not found
        """
        client_class = cls._clients.get(vendor.lower())
        if client_class:
            return client_class()
        return None

    @classmethod
    def get_vendors(cls) -> list:
        """Get list of available vendors"""
        return list(cls._clients.keys())
