#!/bin/bash

# Папки кэша HuggingFace и Torch
HF_CACHE="${HF_HOME:-$HOME/.cache/huggingface/transformers}"
TORCH_CACHE="${TORCH_HOME:-$HOME/.cache/torch/sentence_transformers}"

# Список моделей, которые нужно оставить
KEEP_MODELS=("all-MiniLM-L6-v2" "qwen2.5-7b" "custom-model")

echo "Очистка кэша HuggingFace и Torch, оставляем модели: ${KEEP_MODELS[*]}"

# Функция проверки, нужно ли удалить папку
should_delete() {
    local folder="$1"
    for keep in "${KEEP_MODELS[@]}"; do
        if [[ "$folder" == *"$keep"* ]]; then
            return 1 # НЕ удаляем
        fi
    done
    return 0 # Удаляем
}

# HuggingFace
if [ -d "$HF_CACHE" ]; then
    for f in "$HF_CACHE"/*; do
        should_delete "$f" && echo "Удаляем $f" && rm -rf "$f"
    done
fi

# Torch Sentence-Transformers
if [ -d "$TORCH_CACHE" ]; then
    for f in "$TORCH_CACHE"/*; do
        should_delete "$f" && echo "Удаляем $f" && rm -rf "$f"
    done
fi

echo "Очистка завершена."
