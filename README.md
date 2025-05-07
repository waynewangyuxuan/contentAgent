# Ghibli AI Agent Interface

A beautiful, Ghibli-inspired frontend for AI agent interaction.

## Setup

### Prerequisites

- Node.js (v18+)
- Python 3.8+ with venv
- npm or pnpm

### Installation

1. Clone this repository
2. Set up the backend:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Set up the frontend:
   ```bash
   cd frontend
   npm install
   ```

### Configuration

Create a `.env.local` file in the frontend directory with:
```
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

### Running

1. Start the backend:
   ```bash
   ./run_test_backend.sh
   ```

2. Start the frontend:
   ```bash
   ./run_frontend.sh
   ```

3. Open [http://localhost:3000](http://localhost:3000) in your browser

## API Requirements

The backend must implement two essential endpoints:

1. `GET /status` - Returns server status, available tools, and memory stats:
   ```json
   {
     "status": "active",
     "available_tools": {
       "search": "Search for information online",
       "fetch_content": "Fetch content from a URL"
     },
     "memory_stats": {
       "content_count": 42, 
       "facts_count": 128
     }
   }
   ```

2. `POST /task` - Accepts task requests and returns results:
   ```json
   // Request
   {
     "task": "search for cats",
     "context": {}
   }
   
   // Response
   {
     "plan": {
       "tool_name": "search",
       "parameters": {"query": "cats"}
     },
     "result": {
       "success": true,
       "data": [...]
     },
     "updated_context": {...}
   }
   ```

## Customization

- Tool Icons: Update the `toolIcons` mapping in `tools-panel.tsx`
- Result Display: Modify `ResultContent` in `results-display.tsx` for custom formats
- Styling: Edit colors in `globals.css` and `tailwind.config.ts`