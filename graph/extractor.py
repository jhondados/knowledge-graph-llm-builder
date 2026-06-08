"""LLM-powered entity and relation extractor."""
import json
from typing import List, Tuple
from vertexai.generative_models import GenerativeModel

class GraphExtractor:
    EXTRACT_PROMPT = """
Extract all entities and relationships from the text below.
Return JSON with:
- entities: list of {id, name, type, properties}
- relations: list of {source_id, target_id, relation_type, confidence}
Entity types: PERSON, ORGANIZATION, PRODUCT, LOCATION, CONCEPT, EVENT
Relation types: WORKS_FOR, OWNS, PART_OF, LOCATED_IN, RELATES_TO, COMPETES_WITH
"""
    def __init__(self):
        self.model = GenerativeModel("gemini-1.5-pro-002")

    def extract(self, text: str) -> dict:
        response = self.model.generate_content(
            [self.EXTRACT_PROMPT, f"Text: {text[:8000]}"],
            generation_config={"response_mime_type": "application/json"})
        return json.loads(response.text)

    def batch_extract(self, texts: List[str]) -> List[dict]:
        return [self.extract(t) for t in texts]
