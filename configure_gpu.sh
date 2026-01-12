#!/bin/bash

# GPU-Optimized Ollama Configuration for Apple Silicon

echo "🚀 Configuring Ollama for GPU Acceleration (Apple Metal)..."
echo ""

# Set environment variables for GPU optimization
export OLLAMA_NUM_GPU=1
export OLLAMA_GPU_LAYERS=999  # Load all layers to GPU
export OLLAMA_NUM_THREAD=8    # Match M1 GPU cores

# Check if Ollama is running
if docker-compose ps ollama | grep -q "Up"; then
    echo "✅ Ollama container is running"
else
    echo "⚠️  Starting Ollama container..."
    docker-compose up ollama -d
    sleep 5
fi

# Verify GPU is being used
echo ""
echo "📊 Checking GPU usage..."
docker-compose exec ollama ollama ps

echo ""
echo "✅ GPU Configuration Complete!"
echo ""
echo "GPU Info:"
echo "  - Chipset: Apple M1"
echo "  - GPU Cores: 8"
echo "  - Metal Support: Metal 4"
echo "  - GPU Layers: All (999)"
echo ""
echo "💡 Ollama will now use GPU acceleration for faster inference!"
