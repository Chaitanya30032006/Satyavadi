# TruthGuard - AI-Powered Misinformation Detection Tool

A ChatGPT-like conversational AI tool that identifies misinformation or harmful content in real-time and provides reliable, verified alternatives. Built for hackathon competition.

## 🚀 Features

- **ChatGPT-like Interface**: Natural conversational interface for interactive fact-checking
- **Real-time Content Analysis**: Instantly analyze text content for misinformation through chat
- **AI-Powered Detection**: Uses OpenAI GPT models with conversation context (with fallback to rule-based analysis)
- **Conversation History**: Maintains context across multiple messages
- **Risk Assessment**: Provides detailed risk scores and factors in chat responses
- **Verified Alternatives**: Suggests trusted sources and verified information
- **Modern Chat UI**: Beautiful, responsive chat interface with message bubbles
- **Fast Processing**: Quick analysis with detailed results

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- (Optional) OpenAI API key for enhanced AI analysis

## 🛠️ Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd Hackathon
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables (optional):**
   
   Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   FLASK_ENV=development
   PORT=5000
   ```
   
   **Note**: The application works without an OpenAI API key using rule-based analysis, but AI analysis provides better results.

## 🎯 Usage

1. **Start the Flask server:**
   ```bash
   python app.py
   ```

2. **Open your browser:**
   Navigate to `http://localhost:5000`

3. **Start chatting:**
   - Type your message or paste content to analyze
   - Press Enter or click Send
   - Get conversational responses with:
     - Real-time misinformation analysis
     - Risk assessment with percentage
     - Risk factors identified
     - Verified alternative sources
     - Natural language explanations
   - Continue the conversation with follow-up questions

## 🏗️ Project Structure

```
Hackathon/
├── app.py                 # Flask backend server
├── index.html            # Main frontend page
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── static/
    ├── css/
    │   └── style.css    # Styling
    └── js/
        └── app.js       # Frontend JavaScript
```

## 🔧 Configuration

### Using OpenAI API (Recommended)

1. Get an API key from [OpenAI](https://platform.openai.com/api-keys)
2. Set it as an environment variable:
   ```bash
   # Windows PowerShell
   $env:OPENAI_API_KEY="your-key-here"
   
   # Windows CMD
   set OPENAI_API_KEY=your-key-here
   
   # macOS/Linux
   export OPENAI_API_KEY=your-key-here
   ```

### Without OpenAI API

The application will automatically use rule-based analysis if no API key is provided. This includes:
- Pattern matching for common misinformation indicators
- Risk scoring based on suspicious language
- Basic content analysis

## 📊 API Endpoints

### POST `/api/chat`
Chat endpoint for conversational misinformation detection (ChatGPT-like).

**Request:**
```json
{
  "message": "Your message or content to analyze...",
  "history": [
    {"role": "user", "content": "Previous message"},
    {"role": "assistant", "content": "Previous response"}
  ]
}
```

**Response:**
```json
{
  "success": true,
  "response": "AI-generated conversational response...",
  "analysis": {
    "is_misinformation": false,
    "risk_score": 0.35,
    "risk_factors": ["Contains 1 suspicious language pattern(s)"],
    "alternatives": [
      {
        "title": "Source Title",
        "source": "Source Name",
        "description": "Description",
        "url": "https://example.com"
      }
    ]
  },
  "processing_time": "1.23s",
  "timestamp": "2024-01-01T12:00:00"
}
```

### POST `/api/analyze`
Legacy endpoint for direct content analysis (backward compatibility).

**Request:**
```json
{
  "content": "Text content to analyze..."
}
```

**Response:**
```json
{
  "success": true,
  "content_length": 150,
  "processing_time": "1.23s",
  "is_misinformation": false,
  "risk_score": 0.35,
  "risk_factors": ["Contains 1 suspicious language pattern(s)"],
  "analysis": "Detailed analysis text...",
  "alternatives": [
    {
      "title": "Source Title",
      "source": "Source Name",
      "description": "Description",
      "url": "https://example.com"
    }
  ],
  "timestamp": "2024-01-01T12:00:00"
}
```

### GET `/api/health`
Health check endpoint.

## 🎨 Features Explained

### Chat Interface
- **Conversational**: Natural back-and-forth conversation like ChatGPT
- **Context Aware**: Remembers previous messages in the conversation
- **Smart Analysis**: Automatically detects when content needs verification
- **Interactive**: Ask follow-up questions and get detailed explanations

### Risk Assessment
- **Low Risk (0-40%)**: Content appears reliable
- **Medium Risk (40-70%)**: Some concerns detected
- **High Risk (70-100%)**: Strong misinformation indicators

### Verified Sources
The system includes a database of trusted sources that can be expanded. Currently includes:
- WHO (World Health Organization)
- CDC (Centers for Disease Control)
- FactCheck.org
- Snopes
- PolitiFact

## 🔒 Security & Privacy

- Content is processed server-side
- No data is stored permanently
- API keys should be kept secure (use environment variables)
- CORS is enabled for development (configure for production)

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
1. Set `FLASK_ENV=production`
2. Use a production WSGI server (e.g., Gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```
3. Configure reverse proxy (nginx/Apache) if needed
4. Set up SSL/TLS certificates

## 🧪 Testing

Test the Chat API directly:
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Is this true: Vaccines cause autism?", "history": []}'
```

Test the legacy Analyze API:
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"content": "Your test content here"}'
```

## 📝 License

This project is created for hackathon purposes. Feel free to use and modify as needed.

## 🤝 Contributing

This is a hackathon project. Contributions and improvements are welcome!

## ⚠️ Disclaimer

This tool is designed to assist in identifying potential misinformation but should not be the sole source of truth verification. Always cross-reference with multiple trusted sources and use critical thinking.

## 🎯 Future Enhancements

- [ ] Integration with more fact-checking APIs
- [ ] Machine learning model training on verified datasets
- [ ] Multi-language support
- [ ] Image/video content analysis
- [ ] Browser extension
- [ ] Real-time social media monitoring
- [ ] User reporting and feedback system
- [ ] Database of known misinformation patterns

---

**Built with ❤️ for the Hackathon**

