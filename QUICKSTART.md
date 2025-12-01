# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: (Optional) Set OpenAI API Key
For enhanced AI analysis, set your OpenAI API key:
```bash
# Windows PowerShell
$env:OPENAI_API_KEY="your-key-here"

# Windows CMD
set OPENAI_API_KEY=your-key-here

# macOS/Linux
export OPENAI_API_KEY=your-key-here
```

**Note:** The app works without an API key using rule-based analysis!

### Step 3: Run the Server
```bash
python app.py
```

Then open **http://localhost:5000** in your browser!

## 🎯 Using the Application

1. **Start Chatting**: Type your message or paste content to verify
2. **Send Message**: Press Enter or click the Send button
3. **Get Response**: Receive conversational analysis with risk assessment, alternatives, and explanations
4. **Continue Conversation**: Ask follow-up questions or verify more content

## 📝 Example Conversations

Try these example messages:

**Content Analysis:**
```
Can you verify this: The World Health Organization recommends regular handwashing to prevent the spread of diseases. This is based on extensive scientific research.
```

**Misinformation Check:**
```
Is this true: Doctors don't want you to know this secret cure! Click here now for guaranteed results!
```

**Questions:**
```
What is misinformation?
How can I verify if a news article is reliable?
What are some trusted sources for health information?
```

## 🛠️ Troubleshooting

**Port already in use?**
```bash
# Change port in app.py or set environment variable
set PORT=5001
python app.py
```

**Module not found?**
```bash
pip install -r requirements.txt
```

**Need help?** Check the full README.md for detailed documentation.

