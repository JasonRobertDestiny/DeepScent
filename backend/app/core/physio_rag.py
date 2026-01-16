"""
Physio-RAG Engine: Retrieval-Augmented Generation for physiological corrections.
Uses ChromaDB for vector storage and retrieval of physio-chemical rules.
"""

import json
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

from app.config import settings


@dataclass
class PhysioRule:
    """A physiological correction rule."""
    id: str
    condition: dict
    target: str
    action: str
    factor: Optional[float] = None
    threshold: Optional[dict] = None
    substitute: Optional[dict] = None
    reasoning: str = ""


@dataclass
class RetrievedRule:
    """A rule retrieved from the vector database with relevance score."""
    rule: PhysioRule
    relevance_score: float
    matched_condition: str


class PhysioRAG:
    """
    Physio-RAG Engine for retrieving physiological correction rules.

    Uses ChromaDB for vector similarity search to find relevant rules
    based on user physiological profile.
    """

    def __init__(self):
        self._rules: list[PhysioRule] = []
        self._collection = None
        self._embedder = None
        self._initialized = False

    def initialize(self, use_vector_db: bool = True):
        """
        Initialize the RAG engine.

        Args:
            use_vector_db: Whether to use ChromaDB for vector search.
                          If False, uses simple keyword matching.
        """
        self._load_rules()

        if use_vector_db:
            self._setup_vector_db()

        self._initialized = True

    def _load_rules(self):
        """Load physio rules from JSON file."""
        rules_path = settings.data_dir / "physio_rules.json"

        if not rules_path.exists():
            self._rules = []
            return

        with open(rules_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for rule_data in data.get('rules', []):
            rule = PhysioRule(
                id=rule_data['id'],
                condition=rule_data['condition'],
                target=rule_data['target'],
                action=rule_data['action'],
                factor=rule_data.get('factor'),
                threshold=rule_data.get('threshold'),
                substitute=rule_data.get('substitute'),
                reasoning=rule_data.get('reasoning', '')
            )
            self._rules.append(rule)

    def _setup_vector_db(self):
        """Set up ChromaDB collection with embedded rules."""
        try:
            import chromadb
            from chromadb.config import Settings as ChromaSettings

            # Initialize ChromaDB client
            client = chromadb.Client(ChromaSettings(
                anonymized_telemetry=False,
                is_persistent=False  # In-memory for MVP
            ))

            # Create or get collection
            self._collection = client.get_or_create_collection(
                name=settings.chroma_collection_name,
                metadata={"description": "Physio-chemical rules for perfume formulation"}
            )

            # Embed rules if collection is empty
            if self._collection.count() == 0:
                self._embed_rules()

        except ImportError:
            # Fallback to keyword matching if ChromaDB not available
            self._collection = None

    def _embed_rules(self):
        """Embed rules into the vector database."""
        if not self._collection or not self._rules:
            return

        documents = []
        ids = []
        metadatas = []

        for rule in self._rules:
            # Create searchable document from rule
            condition = rule.condition
            doc = f"{condition.get('parameter', '')} {condition.get('operator', '')} {condition.get('value', '')} "
            doc += f"Target: {rule.target}. Action: {rule.action}. "
            doc += rule.reasoning

            documents.append(doc)
            ids.append(rule.id)
            metadatas.append({
                "target": rule.target,
                "action": rule.action,
                "parameter": condition.get('parameter', ''),
                "factor": str(rule.factor) if rule.factor else ""
            })

        self._collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )

    def query(self, user_profile: dict, n_results: int = 5) -> list[RetrievedRule]:
        """
        Query for relevant physio rules based on user profile.

        Args:
            user_profile: Dict with keys like 'ph', 'skin_type', 'temperature', 'allergies'
            n_results: Maximum number of rules to return

        Returns:
            List of RetrievedRule objects sorted by relevance
        """
        if not self._initialized:
            self.initialize()

        # Build query string from profile
        query_parts = []
        if 'ph' in user_profile:
            query_parts.append(f"pH {user_profile['ph']}")
        if 'skin_type' in user_profile:
            query_parts.append(f"skin type {user_profile['skin_type']}")
        if 'temperature' in user_profile:
            query_parts.append(f"temperature {user_profile['temperature']}")
        if 'allergies' in user_profile:
            for allergy in user_profile.get('allergies', []):
                query_parts.append(f"allergy {allergy}")

        query_text = " ".join(query_parts)

        if self._collection:
            return self._vector_query(query_text, n_results)
        else:
            return self._keyword_query(user_profile, n_results)

    def _vector_query(self, query_text: str, n_results: int) -> list[RetrievedRule]:
        """Query using ChromaDB vector similarity."""
        results = self._collection.query(
            query_texts=[query_text],
            n_results=n_results
        )

        retrieved = []
        for i, rule_id in enumerate(results['ids'][0]):
            rule = self._get_rule_by_id(rule_id)
            if rule:
                distance = results['distances'][0][i] if results['distances'] else 1.0
                relevance = 1.0 / (1.0 + distance)  # Convert distance to relevance
                retrieved.append(RetrievedRule(
                    rule=rule,
                    relevance_score=relevance,
                    matched_condition=query_text
                ))

        return retrieved

    def _keyword_query(self, user_profile: dict, n_results: int) -> list[RetrievedRule]:
        """Fallback keyword-based matching when vector DB not available."""
        matched = []

        for rule in self._rules:
            condition = rule.condition
            param = condition.get('parameter', '')
            operator = condition.get('operator', '')
            value = condition.get('value')

            # Check if rule condition matches user profile
            if param in user_profile:
                user_value = user_profile[param]

                matches = False
                relevance = 0.5  # Base relevance for keyword match

                if operator == '<' and isinstance(user_value, (int, float)):
                    matches = user_value < value
                elif operator == '>' and isinstance(user_value, (int, float)):
                    matches = user_value > value
                elif operator == '==':
                    matches = user_value == value
                elif operator == 'contains' and isinstance(user_value, list):
                    matches = value in user_value

                if matches:
                    relevance = 0.9  # High relevance for exact match
                    matched.append(RetrievedRule(
                        rule=rule,
                        relevance_score=relevance,
                        matched_condition=f"{param} {operator} {value}"
                    ))

        # Sort by relevance and limit
        matched.sort(key=lambda x: x.relevance_score, reverse=True)
        return matched[:n_results]

    def _get_rule_by_id(self, rule_id: str) -> Optional[PhysioRule]:
        """Get a rule by its ID."""
        for rule in self._rules:
            if rule.id == rule_id:
                return rule
        return None

    def get_applicable_rules(self, user_profile: dict) -> list[PhysioRule]:
        """
        Get all rules that apply to a user profile (exact condition matching).

        Args:
            user_profile: User physiological data

        Returns:
            List of applicable PhysioRule objects
        """
        if not self._initialized:
            self.initialize()

        applicable = []

        for rule in self._rules:
            condition = rule.condition
            param = condition.get('parameter', '')
            operator = condition.get('operator', '')
            value = condition.get('value')

            if param not in user_profile:
                continue

            user_value = user_profile[param]

            if operator == '<' and isinstance(user_value, (int, float)) and user_value < value:
                applicable.append(rule)
            elif operator == '>' and isinstance(user_value, (int, float)) and user_value > value:
                applicable.append(rule)
            elif operator == '==' and user_value == value:
                applicable.append(rule)
            elif operator == 'contains' and isinstance(user_value, list) and value in user_value:
                applicable.append(rule)

        return applicable


# Singleton instance
physio_rag = PhysioRAG()
