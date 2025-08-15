# Gutenberg Search Engine

A minimal search engine for Project Gutenberg texts with autocomplete, regex search, and fuzzy matching capabilities.

## Features

- **Autocomplete**: Fast title completion with case-insensitive and accent-insensitive matching using a Trie data structure
- **Regex Search**: Full-text regex pattern matching across book contents
- **Fuzzy Search**: Approximate string matching using Levenshtein distance and BK-tree optimization

## Architecture

- **Backend**: FastAPI with pure Python search algorithms (no external search libraries)
- **Frontend**: React with Vite and Tailwind CSS
- **Data**: Three sample books from Project Gutenberg
- **Core Components**:
  - Text normalization (Unicode, case folding, accent stripping)
  - Tokenization with position tracking
  - Trie for prefix matching
  - BK-tree for fuzzy search optimization
  - Inverted index for full-text search

## Quick Start

1. **Install uv (if not already installed)**:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Install Python dependencies**:
   ```bash
   uv sync
   ```

3. **Download and index sample books**:
   ```bash
   uv run python app/indexer/build_index.py
   ```

4. **Start the backend server**:
   ```bash
   uv run uvicorn app.server.main:app --reload --port 8000
   ```

5. **Install and build the frontend**:
   ```bash
   cd web
   npm install
   npm run build
   ```

6. **Access the application**:
   - Frontend: http://localhost:8000 (served by FastAPI)
   - API docs: http://localhost:8000/docs

## API Endpoints

- `GET /autocomplete?q=<query>&limit=<limit>` - Title autocomplete suggestions
- `GET /search/regex?pattern=<pattern>&case_insensitive=<bool>` - Regex search across content
- `GET /search/fuzzy?term=<term>&k=<distance>` - Fuzzy word matching

## Sample Books

The application indexes three books:
- Pride and Prejudice by Jane Austen
- The Hound of the Baskervilles by Arthur Conan Doyle  
- De la terre � la lune by Jules Verne

## Testing

Run the test suite:
```bash
uv run python tests/test_levenshtein.py
uv run python tests/test_trie.py
uv run python tests/test_bktree.py
uv run python tests/test_integration.py
```

Or with pytest:
```bash
uv run pytest
```

## Development

For development with live reload:
```bash
# Backend
uv run uvicorn app.server.main:app --reload

# Frontend
cd web && npm run dev
```

## Why uv?

This project uses [uv](https://github.com/astral-sh/uv) for Python dependency management:
- **Fast**: 10-100x faster than pip
- **Reliable**: Consistent dependency resolution
- **Modern**: Uses pyproject.toml standard
- **Simple**: Single tool for all Python package management