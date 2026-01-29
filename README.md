# RAG Snip

Минималистичный, но расширяемый RAG-проект для работы с нормативными документами.

Поддерживает:

* разные векторные хранилища
* разные LLM (OpenAI / Ollama / любые совместимые)
* настраиваемые промпты
* гибридный поиск (Vector + BM25)
* Reranker (bge-reranker)
* Query rewrite
* Источники в ответах
* Eval качества

Работает полностью локально с Ollama.

---

## Архитектура пайплайна

```
User question
      ↓
Query rewrite (LLM)
      ↓
Vector search (Chroma)
      ↓
BM25 search
      ↓
Merge candidates
      ↓
Rerank (CrossEncoder)
      ↓
LLM answer + sources
```

---

## Требования

* macOS / Linux
* Python 3.11+
* uv
* Ollama

Установить Ollama и запустить сервис:

```
brew install ollama
brew services start ollama
ollama pull qwen2.5:7b
```

Проверить:

```
curl http://localhost:11434
```

---

## Установка проекта

```
uv venv
source .venv/bin/activate
uv sync
```

---

## Структура проекта

```
rag_snip/
│
├── cli.py
├── configs/
│   └── snip.yaml
│
├── core/
│   ├── embeddings.py
│   ├── llm.py
│   └── prompts.py
│
├── vectorstore/
│   └── build_store.py
│
├── rag/
│   ├── rewrite.py
│   ├── hybrid.py
│   ├── rerank.py
│   └── qa.py
│
└── eval/
    ├── questions.yaml
    └── run_eval.py
```

---

## Где что настраивается

### Модель LLM, embeddings, vectorstore

`configs/snip.yaml`

### Промпты

`core/prompts.py`

### Логика RAG

`rag/`

---

## Индексация документов

Сложить документы в папку `data/` и выполнить:

```
uv run python vectorstore/build_store.py configs/snip.yaml
```

Создаётся база Chroma.

---

## Запрос к системе

```
uv run python cli.py query configs/snip.yaml "создание опорных геодезических сетей"
```

---

## Что происходит при запросе

1. Вопрос переписывается LLM в поисковый вид
2. Идёт векторный поиск по Chroma
3. Параллельно BM25 поиск
4. Кандидаты объединяются
5. Rerank сортирует по релевантности
6. LLM отвечает строго по найденным кускам
7. В ответе указываются источники

---

## Eval качества

Добавить вопросы в:

`eval/questions.yaml`

Запуск:

```
uv run python eval/run_eval.py
```

Позволяет контролировать деградацию качества при изменениях.

---

## Где лежат скачанные модели

### Ollama модели

```
~/.ollama/models
```

### Sentence-transformers и reranker

```
~/.cache/huggingface
```

Очистка:

```
rm -rf ~/.cache/huggingface
```

---

## Частые проблемы

### Каждый раз качается pytorch_model.bin

Не задана переменная кэша. Добавить в `.env`:

```
HF_HOME=~/.cache/huggingface
```

### Mac M1 тормозит

Reranker и embeddings грузят CPU. Первый запуск тяжёлый — дальше работает из кэша.

---

## Масштабирование

Проект из коробки позволяет:

* поменять Chroma на FAISS / Milvus
* поменять Ollama на OpenAI
* менять промпты без правки кода
* добавлять новые этапы поиска

