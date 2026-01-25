from typing import List
from pydantic import BaseModel, Field

class RAGContext(BaseModel):
    id: str = Field(description="The id of the product used to answer the question")
    description: str = Field(description="The short description of the product used to answer the question")

class RAGResponse(BaseModel):
    answer: str = Field(description="The answer to the question")
    references: List[RAGContext] = Field(description="List of RAG Context items used to answer the question")