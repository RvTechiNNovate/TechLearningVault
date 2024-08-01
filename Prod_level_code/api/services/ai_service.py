# api/services/ai_service.py

import httpx
from config.settings import OPENAI_API_KEY
from api.dependencies import HTTPException, status

class AIService:
    async def generate_response(self, query: str, client: httpx.AsyncClient) -> str:
        """
        Generate response using OpenAI API.
        """
        # Example retrieval logic (replace with actual retrieval logic)
        documents = await self.retrieve_documents(query, client)
        context = "\n".join(documents)

        try:
            response = await client.post(
                "https://api.openai.com/v1/engines/text-davinci-003/completions",
                headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
                json={
                    "prompt": f"Context: {context}\n\nQuery: {query}\n\nResponse:",
                    "max_tokens": 150
                }
            )
            response.raise_for_status()
            return response.json()["choices"][0]["text"].strip()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service unavailable")
    
    async def retrieve_documents(self, query: str, client: httpx.AsyncClient) -> list:
        """
        Placeholder retrieval logic for documents.
        """
        # Replace with actual retrieval logic (e.g., database query, external API call)
        return [
            "Document 1: This is a sample document related to the query.",
            "Document 2: Another relevant document content here."
        ]
