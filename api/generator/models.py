from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class Features(BaseModel):
    chat: bool = False
    rag: bool = False
    streaming: bool = False
    embeddings: bool = False

class Endpoint(BaseModel):
    path: str
    method: Literal["GET", "POST"]
    uses_llm: bool

class Auth(BaseModel):
    type: Literal["none", "api_key", "jwt"]

class CPS(BaseModel):
    project_name: str
    description: str
    llm_provider: Literal["openai"]
    model: Optional[str] = None
    embedding_model: Optional[str] = None
    vector_store: Optional[str] = None
    mode: Literal["general", "rag_only"] = "general"
    features: Features
    endpoints: List[Endpoint]
    auth: Auth
    modules: List[str] = []
