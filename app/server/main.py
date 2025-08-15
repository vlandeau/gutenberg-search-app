from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Any
from .deps import engine
import pathlib

app = FastAPI(title="Gutenberg Mini-Search")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AutocompleteOut(BaseModel):
    suggestions: List[str]


@app.get("/autocomplete", response_model=AutocompleteOut)
def autocomplete(q: str = Query(..., min_length=1), limit: int = 10):
    return {"suggestions": engine.autocomplete(q, limit)}


@app.get("/search/regex")
def regex(pattern: str, case_insensitive: bool = True) -> Dict[str, Any]:
    return engine.search_regex(pattern, case_insensitive)


@app.get("/search/fuzzy")
def fuzzy(term: str, k: int = 1) -> Dict[str, List[Dict[str, Any]]]:
    return {"results": engine.search_fuzzy(term, k)}


web_dir = pathlib.Path(__file__).resolve().parents[1].parent / "web" / "dist"
if web_dir.exists():
    app.mount("/", StaticFiles(directory=web_dir, html=True), name="static")
