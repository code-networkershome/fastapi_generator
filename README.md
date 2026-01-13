# FastAPI Generator

An AI-powered tool that generates production-ready FastAPI projects from natural language descriptions.

## Features

- **AI-Powered Analysis**: Describe your project idea, and the AI extracts a structured specification (CPS).
- **Dynamic Code Generation**: Automatically generates project files tailored to your requirements.
- **Multi-Module Support**: Creates separate API modules based on your domain (e.g., users, billing, analytics).
- **RAG Support**: Specialized templates for Retrieval-Augmented Generation projects.
- **Review & Fix**: Iterate on generated code with natural language feedback.
- **ZIP Export**: Download your complete project as a ZIP file.

## Deployment on Vercel

This project is configured for deployment on Vercel as a unified full-stack application.

### Prerequisites

- Node.js 18+
- Python 3.11
- Vercel CLI (`npm i -g vercel`)

### Environment Variables

Configure the following in your Vercel project settings:

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key for LLM operations | Yes |
| `GENERATOR_API_KEY` | Secret key for the unified `/api/v1/generate` endpoint | No (default: `fastapi-gen-secret`) |

### Project Structure

```
/
├── src/                 # Next.js frontend (App Router)
├── api/                 # FastAPI backend (Python Serverless)
│   ├── index.py         # Main entry point
│   ├── generator/       # Code generation logic
│   ├── extraction/      # LLM-based CPS extraction
│   ├── templates/       # Jinja2 templates
│   └── requirements.txt # Python dependencies
├── vercel.json          # Vercel configuration
└── package.json         # Node.js dependencies
```

### Deployment Steps

1. **Clone the repository**
2. **Install Vercel CLI**: `npm i -g vercel`
3. **Link to Vercel**: `vercel link`
4. **Set environment variables**: `vercel env add OPENAI_API_KEY`
5. **Deploy**: `vercel --prod`

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/analyze` | POST | Analyze project idea |
| `/api/generate` | POST | Generate code from CPS |
| `/api/refine` | POST | Refine code with feedback |
| `/api/export` | POST | Export project as ZIP |
| `/api/v1/generate` | POST | Unified generation (requires `X-Api-Key` header) |

### Limitations

> [!WARNING]
> - **Stateless**: Vercel Serverless Functions do not persist files between requests.
> - **Execution Limits**: LLM calls must complete within Vercel's time limits (typically 10-60 seconds).
> - **RAG Workloads**: Heavy RAG workloads require external vector databases (e.g., Pinecone, Qdrant Cloud).

## Local Development

```bash
# Install frontend dependencies
npm install

# Run Next.js dev server
npm run dev

# In another terminal, run the backend
cd api && pip install -r requirements.txt
uvicorn api.index:app --reload --port 8000
```

## License

MIT
