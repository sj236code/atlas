# Atlas Setup Guide

## Prerequisites

- Node.js 18+ and npm
- Python 3.9+
- Gemini API Key (get one at https://makersuite.google.com/app/apikey)

## Setup Instructions

### 1. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

Or if using a virtual environment:

```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the `backend` directory:

```bash
cd backend
# Copy the example file
cp ../.env.example .env
```

Edit `backend/.env` and add your Gemini API key:

```
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 3. Install Frontend Dependencies

```bash
# From the atlas directory (root of the project)
npm install
```

### 4. Configure Frontend Environment

The frontend `.env.local` file is already created with the backend URL. If you need to change it:

```bash
# Edit .env.local
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

## Running the Application

### Start the Backend Server

```bash
cd backend
python main.py
```

Or with uvicorn:

```bash
cd backend
uvicorn main:app --reload
```

The backend will run on http://localhost:8000

### Start the Frontend Server

In a new terminal:

```bash
# From the atlas directory
npm run dev
```

The frontend will run on http://localhost:3000

## Testing the Connection

1. Open http://localhost:3000 in your browser
2. Enter a query like "Plan a Japan trip focused on food & affordability"
3. Click Search
4. The frontend will call the backend API to create a workspace
5. You should see the workspace page with AI-generated suggestions

## Troubleshooting

### Backend not connecting
- Make sure the backend is running on port 8000
- Check that CORS is enabled (it should be by default)
- Verify your `.env` file has the correct `GEMINI_API_KEY`

### Frontend can't reach backend
- Check that `NEXT_PUBLIC_BACKEND_URL` in `.env.local` matches your backend URL
- Make sure both servers are running
- Check browser console for CORS errors

### Gemini API errors
- Verify your API key is correct
- Check that you have API quota available
- Look at backend console for error messages

## API Endpoints

- `POST /api/workspace/create` - Creates a new workspace from a query
- `POST /api/workspace/classify` - Classifies a query into a workspace type
- `POST /api/workspace/schema` - Generates workspace schema
- `POST /api/workspace/suggestions` - Generates AI suggestions
