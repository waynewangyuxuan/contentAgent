# agent/context/memory.py

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
import chromadb
from chromadb.config import Settings

class Memory:
    def __init__(self, persist_directory: str = "data/chroma"):
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        self.client = chromadb.Client(Settings(
            persist_directory=str(self.persist_directory),
            anonymized_telemetry=False
        ))
        
        # Create or get collections
        self.content_collection = self.client.get_or_create_collection("content")
        self.facts_collection = self.client.get_or_create_collection("facts")
        
    def store_content(self, content: str, metadata: Dict[str, Any]) -> None:
        """Store content with associated metadata."""
        self.content_collection.add(
            documents=[content],
            metadatas=[metadata],
            ids=[f"content_{len(self.content_collection.get()['ids'])}"]
        )
        
    def store_fact(self, fact: str, source: str, topic: str) -> None:
        """Store a fact with its source and topic."""
        self.facts_collection.add(
            documents=[fact],
            metadatas=[{"source": source, "topic": topic}],
            ids=[f"fact_{len(self.facts_collection.get()['ids'])}"]
        )
        
    def retrieve_relevant_content(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Retrieve content relevant to the query."""
        results = self.content_collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return [
            {"content": doc, "metadata": meta}
            for doc, meta in zip(results["documents"][0], results["metadatas"][0])
        ]
        
    def retrieve_relevant_facts(self, topic: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Retrieve facts relevant to a topic."""
        results = self.facts_collection.query(
            query_texts=[topic],
            n_results=n_results,
            where={"topic": topic}
        )
        return [
            {"fact": doc, "source": meta["source"]}
            for doc, meta in zip(results["documents"][0], results["metadatas"][0])
        ]
        
    def load_from_json(self, file_path: str) -> None:
        """Load content and facts from a JSON file."""
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        for content in data.get("content", []):
            self.store_content(content["text"], content["metadata"])
            
        for fact in data.get("facts", []):
            self.store_fact(fact["text"], fact["source"], fact["topic"])
            
    def save_to_json(self, file_path: str) -> None:
        """Save content and facts to a JSON file."""
        content_data = self.content_collection.get()
        facts_data = self.facts_collection.get()
        
        data = {
            "content": [
                {"text": doc, "metadata": meta}
                for doc, meta in zip(content_data["documents"], content_data["metadatas"])
            ],
            "facts": [
                {"text": doc, "source": meta["source"], "topic": meta["topic"]}
                for doc, meta in zip(facts_data["documents"], facts_data["metadatas"])
            ]
        }
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)