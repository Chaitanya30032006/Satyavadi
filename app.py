from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import time
import re
from datetime import datetime
import json

app = Flask(__name__, static_folder='static')
CORS(app)

# Configuration
API_KEY = os.environ.get('OPENAI_API_KEY', '')
USE_OPENAI = bool(API_KEY)

# Mock verified sources database (in production, use a real database)
VERIFIED_SOURCES = [
    {
        'title': 'World Health Organization - COVID-19 Information',
        'source': 'WHO',
        'description': 'Official information about COVID-19 from the World Health Organization.',
        'url': 'https://www.who.int/emergencies/diseases/novel-coronavirus-2019'
    },
    {
        'title': 'Centers for Disease Control and Prevention',
        'source': 'CDC',
        'description': 'Trusted health information from the CDC.',
        'url': 'https://www.cdc.gov'
    },
    {
        'title': 'FactCheck.org',
        'source': 'FactCheck.org',
        'description': 'Non-partisan fact-checking organization.',
        'url': 'https://www.factcheck.org'
    },
    {
        'title': 'Snopes',
        'source': 'Snopes',
        'description': 'Fact-checking website for urban legends and misinformation.',
        'url': 'https://www.snopes.com'
    },
    {
        'title': 'PolitiFact',
        'source': 'PolitiFact',
        'description': 'Fact-checking journalism website.',
        'url': 'https://www.politifact.com'
    }
]

# Common misinformation patterns (simplified - in production, use ML models)
MISINFORMATION_PATTERNS = [
    r'\b(cure|miracle|secret|they don\'t want you to know)\b',
    r'\b(guaranteed|100%|proven|scientifically proven)\b',
    r'\b(click here|limited time|act now|urgent)\b',
    r'\b(conspiracy|cover-up|hidden truth)\b',
    r'\b(doctors hate|pharmaceutical companies hide)\b',
]

def analyze_content_with_ai(content):
    """
    Analyze content using AI (OpenAI API or fallback to rule-based)
    """
    if USE_OPENAI:
        try:
            import openai
            openai.api_key = API_KEY
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert fact-checker and misinformation detection system. 
                        Analyze the given content and determine if it contains misinformation, false claims, 
                        or harmful content. Provide a detailed analysis including:
                        1. Whether the content is likely misinformation (true/false)
                        2. Risk score (0-1, where 1 is highest risk)
                        3. Key risk factors
                        4. Detailed analysis of why it might be misinformation
                        5. Suggestions for verified sources
                        
                        Respond in JSON format with: is_misinformation, risk_score, risk_factors (array), 
                        analysis (detailed text), and suggested_topics (array)."""
                    },
                    {
                        "role": "user",
                        "content": f"Analyze this content for misinformation:\n\n{content}"
                    }
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            result_text = response.choices[0].message.content
            
            # Try to parse JSON from response
            try:
                # Extract JSON if wrapped in markdown code blocks
                if '```json' in result_text:
                    json_start = result_text.find('```json') + 7
                    json_end = result_text.find('```', json_start)
                    result_text = result_text[json_start:json_end].strip()
                elif '```' in result_text:
                    json_start = result_text.find('```') + 3
                    json_end = result_text.find('```', json_start)
                    result_text = result_text[json_start:json_end].strip()
                
                ai_result = json.loads(result_text)
                return ai_result
            except json.JSONDecodeError:
                # Fallback to rule-based if JSON parsing fails
                pass
        except Exception as e:
            print(f"OpenAI API error: {e}")
            # Fallback to rule-based analysis
    
    # Rule-based fallback analysis
    return analyze_content_rule_based(content)

def analyze_content_rule_based(content):
    """
    Rule-based content analysis (fallback when AI is not available)
    """
    content_lower = content.lower()
    
    # Check for misinformation patterns
    pattern_matches = sum(1 for pattern in MISINFORMATION_PATTERNS 
                         if re.search(pattern, content_lower, re.IGNORECASE))
    
    # Calculate risk score (0-1)
    risk_score = min(0.3 + (pattern_matches * 0.15), 0.95)
    
    # Determine if misinformation
    is_misinformation = pattern_matches >= 2 or risk_score > 0.6
    
    # Risk factors
    risk_factors = []
    if pattern_matches > 0:
        risk_factors.append(f"Contains {pattern_matches} suspicious language pattern(s)")
    if len(content) < 100:
        risk_factors.append("Very short content (may lack context)")
    if any(word in content_lower for word in ['cure', 'miracle', 'guaranteed']):
        risk_factors.append("Contains unsubstantiated claims")
    if not risk_factors:
        risk_factors.append("No significant risk factors detected")
    
    # Analysis
    analysis = f"""
    Content Analysis Summary:
    
    The content has been analyzed using pattern matching and linguistic analysis.
    {'Potential misinformation indicators were detected.' if is_misinformation else 'No strong indicators of misinformation were found.'}
    
    Key observations:
    - Pattern matches: {pattern_matches}
    - Content length: {len(content)} characters
    - Risk assessment: {'High' if risk_score > 0.6 else 'Medium' if risk_score > 0.4 else 'Low'}
    
    {'⚠️ Warning: This content may contain misinformation. Please verify claims with trusted sources.' if is_misinformation else '✓ This content appears relatively safe, but always verify important claims.'}
    """
    
    return {
        'is_misinformation': is_misinformation,
        'risk_score': risk_score,
        'risk_factors': risk_factors,
        'analysis': analysis.strip(),
        'suggested_topics': extract_topics(content)
    }

def extract_topics(content):
    """
    Extract potential topics from content for finding relevant sources
    """
    topics = []
    content_lower = content.lower()
    
    # Health topics
    if any(word in content_lower for word in ['covid', 'coronavirus', 'vaccine', 'health', 'disease']):
        topics.append('health')
    
    # Science topics
    if any(word in content_lower for word in ['science', 'research', 'study', 'scientist']):
        topics.append('science')
    
    # Politics
    if any(word in content_lower for word in ['politic', 'election', 'government', 'policy']):
        topics.append('politics')
    
    return topics if topics else ['general']

def get_verified_alternatives(topics=None):
    """
    Get verified alternative sources based on topics
    """
    if not topics:
        return VERIFIED_SOURCES[:3]
    
    # Simple topic matching (in production, use better matching)
    relevant_sources = []
    for source in VERIFIED_SOURCES:
        source_lower = source['title'].lower() + ' ' + source['description'].lower()
        if any(topic in source_lower for topic in topics):
            relevant_sources.append(source)
    
    return relevant_sources[:3] if relevant_sources else VERIFIED_SOURCES[:3]

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Chat endpoint for conversational misinformation detection (ChatGPT-like)
    """
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        history = data.get('history', [])
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        if len(message) < 3:
            return jsonify({'error': 'Message too short'}), 400
        
        start_time = time.time()
        
        # Analyze content
        analysis_result = analyze_content_with_ai(message)
        
        # Generate conversational response
        if USE_OPENAI:
            try:
                import openai
                openai.api_key = API_KEY
                
                # Build conversation history
                system_message = {
                    "role": "system",
                    "content": """You are SATYAVADI, a helpful AI assistant that detects misinformation and verifies content. 
                    You provide friendly, conversational responses while analyzing content for misinformation, false claims, hate speech, 
                    fear spreading, violence, manipulation, and political propaganda. Always be helpful, clear, and provide verified sources when possible.
                    Format your responses naturally with markdown when appropriate."""
                }
                
                messages = [system_message]
                messages.extend(history[-10:])  # Keep last 10 messages for context
                messages.append({"role": "user", "content": message})
                
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    temperature=0.7,
                    max_tokens=800
                )
                
                conversational_response = response.choices[0].message.content
            except Exception as e:
                print(f"OpenAI chat error: {e}")
                # Fallback to rule-based conversational response
                conversational_response = generate_conversational_response(message, analysis_result)
        else:
            # Rule-based conversational response
            conversational_response = generate_conversational_response(message, analysis_result)
        
        processing_time = f"{time.time() - start_time:.2f}s"
        
        # Get verified alternatives
        topics = analysis_result.get('suggested_topics', [])
        alternatives = get_verified_alternatives(topics)
        
        # Determine status
        risk_score = analysis_result.get('risk_score', 0.0)
        is_misinformation = analysis_result.get('is_misinformation', False)
        
        if is_misinformation or risk_score > 0.7:
            status = 'Fake'
            status_color = '#ef4444'
        elif risk_score > 0.4:
            status = 'Risky'
            status_color = '#f59e0b'
        elif risk_score > 0.2:
            status = 'Mixed'
            status_color = '#fbbf24'
        else:
            status = 'Verified'
            status_color = '#10b981'
        
        # Detect content types
        content_types = detect_content_types(message)
        
        # Prepare response
        response_data = {
            'success': True,
            'response': conversational_response,
            'analysis': {
                'is_misinformation': is_misinformation,
                'risk_score': risk_score,
                'risk_factors': analysis_result.get('risk_factors', []),
                'alternatives': alternatives,
                'status': status,
                'status_color': status_color,
                'content_types': content_types
            },
            'processing_time': processing_time,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response_data)
    
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

def generate_conversational_response(message, analysis_result):
    """
    Generate a conversational response based on analysis
    """
    risk_score = analysis_result.get('risk_score', 0.0)
    is_misinformation = analysis_result.get('is_misinformation', False)
    risk_factors = analysis_result.get('risk_factors', [])
    
    if is_misinformation or risk_score > 0.7:
        response = f"⚠️ **High Risk Detected**\n\nI've analyzed your message and found strong indicators of potential misinformation.\n\n"
        if risk_factors:
            response += f"**Key concerns:**\n"
            for factor in risk_factors:
                response += f"- {factor}\n"
        response += f"\n**Risk Level:** {int(risk_score * 100)}% (High)\n\n"
        response += "I recommend verifying this information with trusted sources before sharing or acting on it."
    elif risk_score > 0.4:
        response = f"⚠️ **Moderate Risk Detected**\n\nI've reviewed your message and found some concerning patterns.\n\n"
        if risk_factors:
            response += f"**Concerns identified:**\n"
            for factor in risk_factors:
                response += f"- {factor}\n"
        response += f"\n**Risk Level:** {int(risk_score * 100)}% (Medium)\n\n"
        response += "Please verify this information with reliable sources."
    else:
        response = f"✅ **Low Risk**\n\nI've analyzed your message and it appears relatively safe.\n\n"
        response += f"**Risk Level:** {int(risk_score * 100)}% (Low)\n\n"
        response += "However, always verify important claims with trusted sources."
    
    return response

def detect_content_types(content):
    """
    Detect different types of harmful content
    """
    content_lower = content.lower()
    content_types = {
        'fear_spreading': {
            'detected': any(word in content_lower for word in ['panic', 'fear', 'danger', 'threat', 'crisis', 'emergency', 'warning']),
            'confidence': 0.5 if any(word in content_lower for word in ['panic', 'fear', 'danger']) else 0.3
        },
        'hate_speech': {
            'detected': any(word in content_lower for word in ['hate', 'attack', 'enemy', 'destroy']),
            'confidence': 0.4
        },
        'violence': {
            'detected': any(word in content_lower for word in ['violence', 'attack', 'kill', 'harm', 'destroy']),
            'confidence': 0.5 if any(word in content_lower for word in ['kill', 'harm']) else 0.3
        },
        'manipulation': {
            'detected': any(word in content_lower for word in ['manipulate', 'trick', 'deceive', 'lie']),
            'confidence': 0.4
        },
        'political_propaganda': {
            'detected': any(word in content_lower for word in ['propaganda', 'conspiracy', 'cover-up', 'hidden truth']),
            'confidence': 0.5 if any(word in content_lower for word in ['conspiracy', 'cover-up']) else 0.3
        }
    }
    return content_types

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    Main API endpoint for content analysis
    """
    try:
        data = request.get_json()
        content = data.get('content', '').strip()
        
        if not content:
            return jsonify({'error': 'No content provided'}), 400
        
        if len(content) < 10:
            return jsonify({'error': 'Content too short'}), 400
        
        start_time = time.time()
        
        # Analyze content
        analysis_result = analyze_content_with_ai(content)
        
        processing_time = f"{time.time() - start_time:.2f}s"
        
        # Get verified alternatives
        topics = analysis_result.get('suggested_topics', [])
        alternatives = get_verified_alternatives(topics)
        
        # Prepare response
        response = {
            'success': True,
            'content_length': len(content),
            'processing_time': processing_time,
            'is_misinformation': analysis_result.get('is_misinformation', False),
            'risk_score': analysis_result.get('risk_score', 0.0),
            'risk_factors': analysis_result.get('risk_factors', []),
            'analysis': analysis_result.get('analysis', ''),
            'alternatives': alternatives,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
    
    except Exception as e:
        print(f"Error in analyze endpoint: {e}")
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'healthy',
        'ai_enabled': USE_OPENAI,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)

