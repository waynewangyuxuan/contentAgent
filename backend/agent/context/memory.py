# agent/context/memory.py

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
import chromadb
from chromadb.config import Settings
from datetime import datetime

class Memory:
    _instance = None
    
    def __new__(cls, persist_directory: str = "data/chroma"):
        if cls._instance is None:
            cls._instance = super(Memory, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, persist_directory: str = "data/chroma"):
        if self._initialized:
            return
            
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        self.client = chromadb.Client(Settings(
            persist_directory=str(self.persist_directory),
            anonymized_telemetry=False
        ))
        
        # Create or get collections
        self.content_collection = self.client.get_or_create_collection("content")
        self.facts_collection = self.client.get_or_create_collection("facts")
        
        self._initialized = True
        
    def generate_metadata(
        self,
        source: str,
        content_type: str,
        title: Optional[str] = None,
        url: Optional[str] = None,
        task: Optional[str] = None,
        tool: Optional[str] = None,
        additional_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate standardized metadata for content storage.
        
        Args:
            source: Where the content came from (e.g., "web_fetch", "tweet", "search")
            content_type: Type of content (e.g., "article", "tweet", "fact")
            title: Title of the content (if applicable)
            url: Source URL (if applicable)
            task: Task that generated this content
            tool: Tool that generated this content
            additional_metadata: Any additional metadata fields
            
        Returns:
            Dictionary with standardized metadata structure
        """
        metadata = {
            "timestamp": datetime.utcnow().isoformat(),
            "source": source,
            "content_type": content_type,
            "version": "1.0"  # Metadata schema version
        }
        
        # Add optional fields if provided
        if title:
            metadata["title"] = title
        if url:
            metadata["url"] = url
        if task:
            metadata["task"] = task
        if tool:
            metadata["tool"] = tool
            
        # Merge any additional metadata
        if additional_metadata:
            metadata.update(additional_metadata)
            
        return metadata
        
    def store_content(self, content: str, metadata: Dict[str, Any]) -> None:
        """Store content with associated metadata."""
        # Ensure metadata has required fields
        if "source" not in metadata or "content_type" not in metadata:
            raise ValueError("Metadata must include 'source' and 'content_type' fields")
            
        self.content_collection.add(
            documents=[content],
            metadatas=[metadata],
            ids=[f"content_{len(self.content_collection.get()['ids'])}"]
        )
        
    def store_fact(self, fact: str, source: str, topic: str) -> None:
        """Store a fact with its source and topic."""
        metadata = self.generate_metadata(
            source=source,
            content_type="fact",
            title=topic
        )
        self.facts_collection.add(
            documents=[fact],
            metadatas=[metadata],
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