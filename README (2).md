# Atlas - AI-Powered Research Workspace

Atlas is an AI-powered search engine that transforms your query into a user-controlled mini-app workspace. Instead of generating answers, Atlas generates **tools**: source panels, maps, calendars, comparison tables, and evidence-linked suggestions.

## Philosophy

> AI builds the tools. Humans build the answers.

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.9+

### Installation

1. **Install frontend dependencies:**
   ```bash
   npm install
   ```

2. **Install backend dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your API keys
   ```

### Running the Application

1. **Start the backend server:**
   ```bash
   cd backend
   python main.py
   # Or: uvicorn main:app --reload
   ```
   Backend runs on http://localhost:8000

2. **Start the frontend dev server:**
   ```bash
   npm run dev
   ```
   Frontend runs on http://localhost:3000

## Project Structure

```
Atlas_Prep/
├── app/                    # Next.js app directory
│   ├── page.tsx           # Landing/search page
│   ├── workspace/[id]/    # Workspace pages
│   └── layout.tsx         # Root layout
├── backend/               # FastAPI backend
│   ├── main.py           # Main API server
│   └── requirements.txt   # Python dependencies
├── components/            # React components (to be created)
├── public/               # Static assets
└── package.json          # Node.js dependencies
```

## Features

- **Search Engine Landing Page**: Clean, centered search interface
- **Query Classification**: Automatically determines workspace type
- **Dynamic Workspace Generation**: Creates custom layouts based on query
- **User Agency**: Users control sources and saved items
- **Evidence-Linked Suggestions**: All AI suggestions include citations

## Development

See the detailed documentation in `atlas/README.md` for:
- Complete feature specifications
- Build plan and phases
- Prompt engineering guidelines
- API schemas and data models

## Tech Stack

- **Frontend**: Next.js 14, React, TypeScript, Tailwind CSS, Framer Motion
- **Backend**: FastAPI (Python)
- **Storage**: LocalStorage (MVP), Supabase (optional)

## License

MIT
