import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Gemini API settings
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') or None
    USE_LLM_CLASSIFICATION = os.environ.get('USE_LLM_CLASSIFICATION', 'True').lower() == 'true'
    
    # Database settings
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'question_bank.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    
    # Upload settings
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'pdf'}
    
    # Bloom's Taxonomy Keywords
    BLOOM_KEYWORDS = {
        'Remember': [
            'define', 'list', 'recall', 'identify', 'name', 'state', 'describe',
            'label', 'match', 'memorize', 'recognize', 'select', 'who', 'what',
            'when', 'where', 'write', 'find', 'spell', 'tell', 'show'
        ],
        'Understand': [
            'explain', 'describe', 'summarize', 'interpret', 'classify', 'compare',
            'contrast', 'demonstrate', 'illustrate', 'paraphrase', 'restate',
            'translate', 'discuss', 'express', 'locate', 'report', 'review'
        ],
        'Apply': [
            'apply', 'demonstrate', 'solve', 'use', 'implement', 'execute',
            'carry out', 'employ', 'illustrate', 'operate', 'practice',
            'schedule', 'sketch', 'utilize', 'calculate', 'compute'
        ],
        'Analyze': [
            'analyze', 'compare', 'contrast', 'examine', 'differentiate',
            'distinguish', 'investigate', 'categorize', 'classify', 'deduce',
            'dissect', 'inspect', 'simplify', 'survey', 'test', 'why'
        ],
        'Evaluate': [
            'evaluate', 'justify', 'critique', 'assess', 'argue', 'defend',
            'judge', 'select', 'support', 'value', 'appraise', 'conclude',
            'criticize', 'decide', 'prioritize', 'recommend', 'verify'
        ],
        'Create': [
            'create', 'design', 'develop', 'formulate', 'construct', 'build',
            'compose', 'generate', 'plan', 'produce', 'invent', 'devise',
            'assemble', 'compile', 'integrate', 'modify', 'organize', 'propose'
        ]
    }
    
    # Bloom's Taxonomy Levels (in order)
    BLOOM_LEVELS = ['Remember', 'Understand', 'Apply', 'Analyze', 'Evaluate', 'Create']
    
    # Default Bloom's Distribution (percentages)
    DEFAULT_BLOOM_DISTRIBUTION = {
        'Remember': 20,
        'Understand': 30,
        'Apply': 20,
        'Analyze': 15,
        'Evaluate': 10,
        'Create': 5
    }

    # Department and Exam Settings
    DEPARTMENTS = ['CSE', 'ECE', 'ME', 'CE', 'EEE']
    
    EXAM_TYPES = {
        'Mid': {'marks': 40, 'duration': 120},
        'End': {'marks': 100, 'duration': 180}
    }
