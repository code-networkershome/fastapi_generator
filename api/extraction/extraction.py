import json
import os
from typing import Dict, Any
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key or api_key == "your_api_key_here":
    print("WARNING: OPENAI_API_KEY is not set or still has the placeholder value in .env")

client = AsyncOpenAI(api_key=api_key if api_key != "your_api_key_here" else "MISSING")

EXTRACTION_PROMPT = """
Extract the information explicitly stated.
If a value is not present, infer a reasonable default based on context (especially for project_name and description).
For boolean features, default to false unless implied.
Output strictly valid JSON matching the CPS schema.

CPS Schema:
{
  "project_name": "string",
  "description": "string",
  "llm_provider": "openai",
  "model": "string | null",
  "embedding_model": "string | null",
  "vector_store": "string | null",
  "mode": "general | rag_only",
  "features": {
    "chat": boolean,
    "rag": boolean,
    "streaming": boolean,
    "embeddings": boolean
  },
  "endpoints": [
    {
      "path": "string",
      "method": "GET | POST",
      "uses_llm": boolean
    }
  ],
  "auth": {
    "type": "none | api_key | jwt"
    },
   "modules": ["string"]
 }
 
 User Input:
 {text}
 
 Instruction:
 - Identify logical domains or modules based on requirements (e.g., "users", "billing", "analytics").
 - List them in the "modules" array.
 - Ensure project_name and description are professional.
 """

async def extract_cps(text: str) -> Dict[str, Any]:
    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a structured data extractor."},
                {"role": "user", "content": EXTRACTION_PROMPT.replace("{text}", text)}
            ],
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        # Fallback or error handling
        return {"error": str(e)}

async def refine_code(cps: Dict[str, Any], files: Dict[str, str], feedback: str) -> Dict[str, Any]:
    try:
        prompt = f"""
        You are an expert full-stack AI engineer. 
        A user has generated a FastAPI project and has some feedback or discovered bugs.
        
        Current project specification (CPS):
        {json.dumps(cps, indent=2)}
        
        Current generated files:
        {json.dumps(files, indent=2)}
        
        User Feedback/Issues:
        {feedback}
        
        Instruction:
        - Analyze the feedback and the current code.
        - Fix any bugs mentioned or implied.
        - Implement requested changes.
        - Return a complete JSON object where keys are the file paths and values are the NEW content for those files.
        - Include ALL files in the output (except unchanged binary files if any) to maintain a complete project state.
        - Return ONLY the JSON object.
        """
        
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a code refiner and bug fixer. Always return a full file map in valid JSON format."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}
