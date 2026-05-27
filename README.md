# RAG_Jango

This repository contains a Django-based Retrieval-Augmented Generation (RAG) backend project.

## Project structure

- `manage.py` — Django CLI
- `rag/` — Django app with services for document loading, chunking, embedding, retrieval
- `rag_backend/` — Django project settings

## Quick start (after clone)

1. Create and activate a virtual environment

   Windows (PowerShell):
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   Windows (cmd):
   ```cmd
   python -m venv .venv
   .\.venv\Scripts\activate.bat
   ```

2. Install dependencies

   - CPU PyTorch (follow https://pytorch.org/get-started/locally/ for the best command)
   - Then:
   ```bash
   pip install -r requirements.txt
   ```

3. Apply migrations and run the development server

```bash
python manage.py migrate
python manage.py runserver
```

4. Optional: Run service scripts (examples)

```bash
# chunking demo
python rag/services/chunking.py
# embedding (will download model)
python rag/services/embedding.py
# retrieval demo
python rag/services/retrieval.py
```

## Notes and troubleshooting

- This project uses `sentence-transformers` and may download models from Hugging Face on first run.
- `faiss` can be platform-dependent; on Windows prefer `faiss-cpu` if available, or follow FAISS installation docs.
- If you see errors importing `fitz`, ensure `PyMuPDF` is installed (`pip install PyMuPDF`) and there is no conflicting package named `fitz` in the environment.

## Environment variables

- If you use Hugging Face private models, set `HF_TOKEN` in your environment before running services needing authentication.

## Licence

Add a license file if you plan to open-source this repository.
