#!/bin/bash

# Define the Ollama API base URL
export OLLAMA_API_BASE=http://localhost:11434

# Ensure Ollama is running and has the models pulled
echo "Checking models..."
ollama pull qwen2.5-coder:7b
ollama pull qwen2.5-coder:14b

# Aider works better with a larger context window for local models.
# We set the 'ollama_chat' prefix to tell aider to use the chat API.
# The 'architect' mode uses 14b for planning and 7b for writing.

# Check if environment variables are set
AIDER_MODEL=${AIDER_MODEL:-"ollama_chat/qwen2.5-coder:14b"}
AIDER_EDITOR_MODEL=${AIDER_EDITOR_MODEL:-"ollama_chat/qwen2.5-coder:7b"}

aider \
  --model $AIDER_MODEL \
  --editor-model $AIDER_EDITOR_MODEL \
  --architect \
  --map-tokens 1024 \
  --cache-prompts \
  --no-stream
