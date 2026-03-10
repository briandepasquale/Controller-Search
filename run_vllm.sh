#!/bin/bash
# Starts a local vLLM server on a GPU node.
# Run this in a separate terminal on your GPU node before launching the notebook.
#
# Usage on BU SCC:
#   1. Get a GPU node:  qrsh -l gpus=1 -P depaqlab -l h_rt=4:00:00
#   2. On that node:    bash run_vllm.sh
#   3. Note the hostname (e.g. scc-na1.scc.bu.edu) and forward the port to your
#      local/login session if needed:
#        ssh -L 8000:localhost:8000 <gpu-hostname>
#   4. In the notebook, VLLM_API_BASE is already set to http://localhost:8000/v1

set -e

# ── Config ────────────────────────────────────────────────────────────────────
MODEL="deepseek-ai/DeepSeek-R1-Distill-Qwen-32B"
PORT=8000

# Load HF token from .env so we can pull gated models (Llama requires agreement)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/.env" ]; then
    export $(grep -v '^#' "$SCRIPT_DIR/.env" | xargs)
fi
export HF_TOKEN

# Load Python 3.12 + CUDA (required on BU SCC)
module load python3/3.12.4 cuda/12.2 2>/dev/null && echo "Modules loaded" || echo "Warning: could not load modules"

# Activate the project venv
source "$SCRIPT_DIR/.venv/bin/activate"

# Install vLLM if not already present (must run on GPU node with CUDA)
python3 -c "import vllm" 2>/dev/null || pip install -q vllm

echo "Starting vLLM server: $MODEL on port $PORT"
echo "GPU: $(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null || echo 'unknown')"

CUDA_VISIBLE_DEVICES=0,1 HF_HOME=/projectnb/depaqlab/bddepasq/hf_cache \
python3 -m vllm.entrypoints.openai.api_server \
    --model "$MODEL" \
    --port "$PORT" \
    --tensor-parallel-size 2 \
    --dtype auto \
    --max-model-len 8192
