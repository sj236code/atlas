# Troubleshooting Guide

## Issue: Nothing happens when I search

### Step 1: Check if Backend is Running

1. Open a terminal and check if the backend is running:
   ```bash
   # Check if port 8000 is in use
   # Windows PowerShell:
   netstat -ano | findstr :8000
   
   # Or check if Python process is running
   ```

2. Start the backend if it's not running:
   ```bash
   cd backend
   python main.py
   ```

   You should see:
   ```
   INFO:     Started server process
   INFO:     Uvicorn running on http://0.0.0.0:8000
   ```

### Step 2: Check Browser Console

1. Open your browser's Developer Tools (F12)
2. Go to the Console tab
3. Try searching again
4. Look for error messages

Common errors:
- **CORS error**: Backend CORS not configured correctly
- **Network error**: Backend not running or wrong URL
- **500 error**: Backend API error (check backend console)

### Step 3: Check Backend Console

Look at the terminal where your backend is running. You should see:
- `Creating workspace for query: [your query]`
- `Classifying query...`
- `Classification result: ...`
- etc.

If you see errors, check:
- Is `GEMINI_API_KEY` set correctly in `backend/.env`?
- Is the API key valid?
- Are there any Python errors?

### Step 4: Test Backend Directly

Open a new terminal and test the backend:

```bash
# Test if backend is responding
curl http://localhost:8000/

# Should return: {"message":"Atlas API is running"}

# Test workspace creation
curl -X POST http://localhost:8000/api/workspace/create \
  -H "Content-Type: application/json" \
  -d '{"query": "test query"}'
```

### Step 5: Check Environment Variables

**Backend** (`backend/.env`):
```
GEMINI_API_KEY=your_actual_key_here
GEMINI_MODEL=gemini-1.5-flash
```

**Frontend** (`.env.local`):
```
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

### Step 6: Common Issues

1. **Backend not running**: Start it with `python backend/main.py`
2. **Wrong port**: Make sure backend is on 8000 and frontend knows about it
3. **API key missing**: Add `GEMINI_API_KEY` to `backend/.env`
4. **CORS issues**: Backend should allow `http://localhost:3000`
5. **Network error**: Check firewall/antivirus blocking localhost connections

### Step 7: Enable Debugging

The code now includes console.log statements. Check:
- Browser console (F12 → Console tab)
- Backend terminal output

If you see specific errors, share them for help debugging!
