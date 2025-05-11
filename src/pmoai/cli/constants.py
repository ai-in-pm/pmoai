"""Constants for the PMOAI CLI."""

# Project Management Methodologies
PM_METHODOLOGIES = [
    "Agile",
    "Waterfall",
    "Scrum",
    "Kanban",
    "Lean",
    "Six Sigma",
    "PRINCE2",
    "PMI/PMBOK",
    "Hybrid",
    "Custom",
]

# Environment variables for different providers
ENV_VARS = {
    "openai": [
        {
            "prompt": "Enter your OpenAI API key",
            "key_name": "OPENAI_API_KEY",
        }
    ],
    "anthropic": [
        {
            "prompt": "Enter your Anthropic API key",
            "key_name": "ANTHROPIC_API_KEY",
        }
    ],
    "google": [
        {
            "prompt": "Enter your Google API key",
            "key_name": "GOOGLE_API_KEY",
        }
    ],
    "azure_openai": [
        {
            "prompt": "Enter your Azure OpenAI API key",
            "key_name": "AZURE_OPENAI_API_KEY",
        },
        {
            "prompt": "Enter your Azure OpenAI API base",
            "key_name": "AZURE_OPENAI_API_BASE",
        },
        {
            "prompt": "Enter your Azure OpenAI API version",
            "key_name": "AZURE_OPENAI_API_VERSION",
        },
        {
            "prompt": "Enter your Azure OpenAI API deployment name",
            "key_name": "AZURE_OPENAI_API_DEPLOYMENT_NAME",
        },
    ],
    "ollama": [
        {
            "prompt": "Enter your Ollama API base URL (default: http://localhost:11434)",
            "key_name": "OLLAMA_API_BASE",
            "default": True,
            "OLLAMA_API_BASE": "http://localhost:11434",
        }
    ],
    "together": [
        {
            "prompt": "Enter your Together API key",
            "key_name": "TOGETHER_API_KEY",
        }
    ],
    "groq": [
        {
            "prompt": "Enter your Groq API key",
            "key_name": "GROQ_API_KEY",
        }
    ],
    "mistral": [
        {
            "prompt": "Enter your Mistral API key",
            "key_name": "MISTRAL_API_KEY",
        }
    ],
    "anyscale": [
        {
            "prompt": "Enter your Anyscale API key",
            "key_name": "ANYSCALE_API_KEY",
        }
    ],
    "cohere": [
        {
            "prompt": "Enter your Cohere API key",
            "key_name": "COHERE_API_KEY",
        }
    ],
    "huggingface": [
        {
            "prompt": "Enter your HuggingFace API key",
            "key_name": "HUGGINGFACEHUB_API_TOKEN",
        }
    ],
    "replicate": [
        {
            "prompt": "Enter your Replicate API token",
            "key_name": "REPLICATE_API_TOKEN",
        }
    ],
    "perplexity": [
        {
            "prompt": "Enter your Perplexity API key",
            "key_name": "PERPLEXITY_API_KEY",
        }
    ],
    "fireworks": [
        {
            "prompt": "Enter your Fireworks API key",
            "key_name": "FIREWORKS_API_KEY",
        }
    ],
    "deepinfra": [
        {
            "prompt": "Enter your DeepInfra API key",
            "key_name": "DEEPINFRA_API_KEY",
        }
    ],
    "voyage": [
        {
            "prompt": "Enter your Voyage API key",
            "key_name": "VOYAGE_API_KEY",
        }
    ],
    "databricks": [
        {
            "prompt": "Enter your Databricks API key",
            "key_name": "DATABRICKS_API_KEY",
        },
        {
            "prompt": "Enter your Databricks API host",
            "key_name": "DATABRICKS_HOST",
        },
    ],
}

# Models for different providers
MODELS = {
    "openai": [
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4-turbo",
        "gpt-4",
        "gpt-3.5-turbo",
    ],
    "anthropic": [
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307",
        "claude-2.1",
        "claude-2.0",
        "claude-instant-1.2",
    ],
    "google": [
        "gemini-1.5-pro",
        "gemini-1.5-flash",
        "gemini-1.0-pro",
        "gemini-1.0-ultra",
    ],
    "azure_openai": [],
    "ollama": [
        "llama3",
        "llama3:8b",
        "llama3:70b",
        "mistral",
        "mixtral",
        "phi3",
        "phi3:mini",
        "phi3:medium",
        "phi3:small",
        "qwen",
        "qwen:14b",
        "qwen:72b",
        "gemma",
        "gemma:2b",
        "gemma:7b",
        "codellama",
        "codellama:7b",
        "codellama:13b",
        "codellama:34b",
        "llama2",
        "llama2:7b",
        "llama2:13b",
        "llama2:70b",
    ],
    "together": [
        "meta-llama/Llama-3-70b-chat-hf",
        "meta-llama/Llama-3-8b-chat-hf",
        "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "mistralai/Mistral-7B-Instruct-v0.2",
        "togethercomputer/StripedHyena-Nous-7B",
    ],
    "groq": [
        "llama3-70b-8192",
        "llama3-8b-8192",
        "mixtral-8x7b-32768",
        "gemma-7b-it",
    ],
    "mistral": [
        "mistral-large-latest",
        "mistral-medium-latest",
        "mistral-small-latest",
        "open-mixtral-8x7b",
        "open-mistral-7b",
    ],
    "anyscale": [
        "meta-llama/Llama-3-70b-chat-hf",
        "meta-llama/Llama-3-8b-chat-hf",
        "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "mistralai/Mistral-7B-Instruct-v0.2",
    ],
    "cohere": [
        "command-r",
        "command-r-plus",
        "command",
        "command-light",
        "command-nightly",
        "command-light-nightly",
    ],
    "huggingface": [],
    "replicate": [],
    "perplexity": [
        "llama-3-sonar-large-32k-online",
        "llama-3-sonar-small-32k-online",
        "sonar-small-online",
        "sonar-medium-online",
        "sonar-medium-chat",
        "sonar-small-chat",
    ],
    "fireworks": [
        "accounts/fireworks/models/llama-v3-70b-instruct",
        "accounts/fireworks/models/llama-v3-8b-instruct",
        "accounts/fireworks/models/mixtral-8x7b-instruct",
    ],
    "deepinfra": [
        "meta-llama/Llama-3-70b-chat-hf",
        "meta-llama/Llama-3-8b-chat-hf",
        "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "mistralai/Mistral-7B-Instruct-v0.2",
    ],
    "voyage": [
        "voyage-2",
        "voyage-large-2",
    ],
    "databricks": [],
}
