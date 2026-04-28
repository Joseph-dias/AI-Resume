# AI-Resume

An intelligent AI-powered resume chatbot that presents your professional background to recruiters, hiring managers, and professional contacts using retrieval-augmented generation (RAG) and conversational AI.

## Overview

**AI-Resume** is a FastAPI-based web application that leverages the XAI (x.ai) SDK to create an interactive chat interface about your resume and professional profile. The AI agent intelligently retrieves information from your resume document collection and searches public profiles to provide accurate, evidence-based responses about your experience, skills, and background.

### Key Features

- **Resume-Aware Chat Interface**: Ask questions about the candidate's experience, skills, education, and projects
- **Retrieval-Augmented Generation (RAG)**: Searches your resume document collection using hybrid search (keyword + semantic)
- **Verified Information**: Cross-references public profiles (LinkedIn, GitHub, Stack Overflow) when needed
- **Streaming Responses**: Real-time chat responses streamed to the frontend for better UX
- **Stateful Conversations**: Maintains chat history within a session for coherent multi-turn interactions
- **Smart Tool Integration**: Uses collections search for resume data and controlled web search for public profiles

## Project Structure

```
AI-Resume/
├── app.py                 # FastAPI application with REST endpoints
├── resume_chat.py         # ResumeChat class with AI logic and system prompt
├── requirements.txt       # Python dependencies
├── .env.example          # Environment configuration template
├── .gitignore            # Git ignore rules
└── static/               # Frontend assets (index.html, CSS, JS)
```

## Prerequisites

- Python 3.9+
- XAI SDK credentials
- An XAI collection with your resume/profile data

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Joseph-dias/AI-Resume.git
   cd AI-Resume
   ```

2. **Create a virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your XAI_COLLECTION_ID
   ```

## Configuration

Create a `.env` file in the project root with:

```
XAI_COLLECTION_ID=your_collection_id_here
```

The `XAI_COLLECTION_ID` is the ID of your document collection in the XAI system that contains your resume and professional documents.

## Usage

1. **Start the server**
   ```bash
   uvicorn app:app --reload
   ```

2. **Access the application**
   - Open your browser to `http://localhost:8000`
   - Start chatting with the AI about your resume

## API Endpoints

### `POST /api/chat`
Send a chat message and receive a complete response.

**Request:**
```json
{
  "message": "What are your main technical skills?"
}
```

**Response:**
```json
{
  "response": "Joey brings expertise in [technical skills from resume]..."
}
```

### `POST /api/chat/stream`
Send a chat message and receive the response as a Server-Sent Event (SSE) stream for real-time display.

**Request:**
```json
{
  "message": "Tell me about your experience with Python"
}
```

**Response:** Streaming text chunks as they're generated

### `POST /api/reset`
Clear the conversation history and start fresh.

**Response:**
```json
{}
```

### `GET /`
Serves the frontend HTML interface.

## How It Works

### ResumeChat Class

The `ResumeChat` class (`resume_chat.py`) manages the AI interaction:

1. **Initialization**: Sets up the AI chat with two tools:
   - **Collections Search**: Retrieves information from your resume documents (hybrid search: keyword + semantic)
   - **Web Search**: Fetches data from approved domains (LinkedIn, GitHub, Stack Overflow, 16personalities.com)

2. **System Prompt**: A detailed instruction set that:
   - Defines the AI's role as your professional advocate
   - Specifies when and how to use each tool
   - Handles sensitive topics (salary, weaknesses, candidate comparisons)
   - Incorporates personality context (INTJ type, Working Geniuses framework)

3. **Chat Methods**:
   - `ask()`: Get a complete response to a question
   - `stream()`: Get responses as an iterator of text chunks
   - `reset()`: Clear conversation history

### FastAPI Application

The `app.py` file provides:
- REST API endpoints for chat interactions
- Server-Sent Events streaming for real-time responses
- Static file serving for the frontend
- Asynchronous request handling

## Dependencies

- **xai-sdk**: XAI API client for AI chat and tools
- **fastapi**: Modern web framework for building APIs
- **uvicorn**: ASGI web server for running FastAPI
- **python-dotenv**: Environment variable management
- **pydantic**: Data validation using Python type annotations

## Customization

### Modify the System Prompt

Edit the `self._system_message` in `resume_chat.py` to:
- Change the AI's tone or personality
- Add new public profiles to reference
- Update handling of sensitive topics
- Add personality frameworks or additional context

### Change the AI Model

In `resume_chat.py`, modify the `model` parameter in `ResumeChat`:
```python
resume = ResumeChat(client, collection_id=os.environ["XAI_COLLECTION_ID"], model="grok-4")
```

### Update Frontend

Place your HTML, CSS, and JavaScript files in the `static/` directory. The app will serve `static/index.html` at the root endpoint.

## Typical Conversation Topics

The AI excels at answering questions like:

- "What is your professional background?"
- "What are your technical skills?"
- "Tell me about your experience with [specific technology]"
- "What projects have you worked on?"
- "What is your educational background?"
- "How would you approach [problem type]?"
- "What is your personality type?" (integrates MBTI/Working Geniuses context)

The AI politely declines questions unrelated to the candidate's professional background.

## Development

To run in development mode with auto-reload:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## License

This project is open source and available under the MIT License.

## Author

[Joseph Dias](https://github.com/Joseph-dias)

- LinkedIn: https://www.linkedin.com/in/joseph-dias-49b20ab2/
- GitHub: https://github.com/Joseph-dias

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## Support

For issues or questions, please open an issue on the [GitHub repository](https://github.com/Joseph-dias/AI-Resume/issues).
