# agent/context/memory.py

import json
import os

KNOWLEDGE_FILE = os.path.join("data", "knowledge.json")

def get_knowledge_snippet(query: str, max_results: int = 2) -> list[dict]:
    """
    Return a list of knowledge entries that fuzzily match the query.
    Currently uses simple keyword matching.
    """
    if not os.path.exists(KNOWLEDGE_FILE):
        print("[memory] No knowledge base found.")
        return []

    with open(KNOWLEDGE_FILE, "r") as f:
        knowledge = json.load(f)

    query_lower = query.lower()
    matches = []

    for entry in knowledge:
        if query_lower in entry["topic"].lower() or query_lower in entry["summary"].lower():
            matches.append(entry)

    return matches[:max_results]