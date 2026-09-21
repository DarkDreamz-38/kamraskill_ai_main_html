# Preview Server Setup

## How to reproduce the artifacts

The frontend has been converted to pure HTML/CSS/JS. The key files are:
- `frontend/public/quiz.html` - Quiz page (all features included)
- `frontend/public/quiz-result.html` - Results page

## How to run the server

### Frontend (static files)
```powershell
python -m http.server 8080 --directory frontend\public
```
Or for development:
```powershell
npm run dev
```
(from the `frontend` directory)

### Backend (API)
```powershell
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Ports
- Frontend: 8080 (static HTML) or 3000 (Next.js dev)
- Backend: 8000

### CORS Configuration
The backend CORS is configured to allow:
- http://localhost:3000
- http://localhost:8080
