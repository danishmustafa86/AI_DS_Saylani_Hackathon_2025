# 🎓 AI Campus Admin Agent

> An intelligent AI-powered campus administration system built with FastAPI, LangGraph, and OpenAI GPT-4, designed for the **Saylani Hackathon 2025 - AI/DS AI Campus** project.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.114.2-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2.45-FF6B6B?style=flat)](https://langchain.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-6.0+-47A248?style=flat&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?style=flat&logo=openai)](https://openai.com/)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [API Documentation](#-api-documentation)
- [Usage Examples](#-usage-examples)
- [Authentication](#-authentication)
- [AI Agent Capabilities](#-ai-agent-capabilities)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Overview

**AI Campus Admin Agent** is a cutting-edge, intelligent campus management system that combines the power of AI agents with traditional administration tools. Built for the **Saylani Hackathon 2025**, this system leverages **LangGraph**, **OpenAI GPT-4o-mini**, and **RAG (Retrieval Augmented Generation)** to provide a conversational interface for managing students, accessing university information, and performing administrative tasks.

The system acts as an intelligent assistant that can:
- 📊 Manage student records (CRUD operations)
- 💬 Answer questions about UAF University using RAG
- 🔍 Search the web for real-time information
- 🎤 Support voice interactions (speech-to-text and text-to-speech)
- 📧 Send automated email notifications
- 📈 Generate analytics and insights
- 🔐 Secure authentication with JWT tokens

---

## 🎯 Problem Statement

Traditional campus administration systems face several challenges:

### **1. Fragmented Information**
- Student data, university information, and administrative tasks are scattered across multiple systems
- No unified interface for accessing information
- Time-consuming manual queries and searches

### **2. Limited Accessibility**
- Administrative staff must navigate complex interfaces
- Students struggle to find university information
- No conversational interface for natural queries

### **3. Inefficient Operations**
- Manual student record management
- Lack of real-time analytics
- No automated notification systems
- Limited integration with modern AI tools

### **4. Poor User Experience**
- Steep learning curve for new users
- No voice interaction support
- Limited multi-modal capabilities

---

## ✨ Key Features

### 🤖 **Intelligent AI Agent**
- **LangGraph-powered Agent**: React-style agent with tool calling capabilities
- **Conversational Interface**: Natural language interaction for all operations
- **Context Awareness**: Maintains conversation history and context
- **Multi-tool Orchestration**: Automatically selects and uses appropriate tools

### 👨‍🎓 **Student Management**
- ➕ Add new students with validation
- 🔍 Search and retrieve student information
- ✏️ Update student records
- 🗑️ Delete student records
- 📊 List all students with filtering
- 📈 Department-wise analytics
- 🆕 Recently onboarded students tracking

### 🏛️ **UAF University Knowledge Base**
- **RAG (Retrieval Augmented Generation)**: Answers questions about UAF University
- **Web Search Integration**: Falls back to DuckDuckGo for real-time information
- **Scraped Data**: Pre-loaded knowledge base from UAF website
- **Intelligent Filtering**: Only answers UAF-related queries

### 💬 **Advanced Chat System**
- **Streaming Responses**: Real-time token-by-token responses
- **Chat History**: Persistent conversation storage in MongoDB
- **Session Management**: User-specific chat sessions
- **Authenticated Chat**: Secure chat endpoints with JWT
- **Voice Chat**: Speech-to-text and text-to-speech support

### 🎤 **Voice Capabilities**
- **Speech Recognition**: Convert voice input to text
- **Text-to-Speech**: ElevenLabs integration for natural voice responses
- **Multiple Voices**: Configurable voice selection
- **Real-time Processing**: Fast voice-to-text conversion

### 🔐 **Authentication & Authorization**
- **JWT Token Authentication**: Secure token-based auth
- **User Registration**: Signup with email validation
- **Password Security**: Bcrypt hashing with salt rounds
- **Role-Based Access Control**: Admin vs regular user permissions
- **Protected Endpoints**: Secure routes with authentication middleware

### 📊 **Analytics & Reporting**
- Total student count
- Department-wise distribution
- Recent onboarding trends
- Active students tracking (last 7 days)
- Comprehensive analytics dashboard

### 📧 **Email Notifications**
- SMTP integration for email sending
- Automated notifications for student operations
- Admin alerts for CRUD operations
- Configurable email templates

### 🌐 **Web Search Integration**
- DuckDuckGo search for general queries
- Fallback mechanism for knowledge base gaps
- Real-time information retrieval

---

## 🛠️ Technology Stack

### **Backend Framework**
| Technology | Version | Purpose |
|------------|---------|---------|
| **FastAPI** | 0.114.2 | Modern, high-performance web framework |
| **Uvicorn** | 0.30.6 | ASGI server with WebSocket support |
| **Python** | 3.11+ | Core programming language |

### **AI & Machine Learning**
| Technology | Version | Purpose |
|------------|---------|---------|
| **OpenAI GPT-4o-mini** | Latest | Language model for intelligent responses |
| **LangChain** | 0.3.9 | Framework for building LLM applications |
| **LangGraph** | 0.2.45 | Agent orchestration and workflow management |
| **ElevenLabs** | 1.6.2 | Text-to-speech voice synthesis |
| **SpeechRecognition** | 3.10.4 | Speech-to-text conversion |

### **Database**
| Technology | Version | Purpose |
|------------|---------|---------|
| **MongoDB** | 6.0+ | NoSQL database for flexible data storage |
| **Motor** | 3.6.0 | Async MongoDB driver for Python |

### **Authentication & Security**
| Technology | Version | Purpose |
|------------|---------|---------|
| **python-jose** | 3.3.0 | JWT token generation and validation |
| **passlib** | 1.7.4 | Password hashing with bcrypt |
| **email-validator** | 2.2.0 | Email address validation |

### **API & Integration**
| Technology | Version | Purpose |
|------------|---------|---------|
| **SSE-Starlette** | 2.1.2 | Server-Sent Events for streaming |
| **httpx** | 0.27.2 | HTTP client for async requests |
| **duckduckgo-search** | 6.3.0 | Web search capabilities |

### **Data Validation**
| Technology | Version | Purpose |
|------------|---------|---------|
| **Pydantic** | 2.9.2 | Data validation and settings management |
| **pydantic-settings** | 2.5.2 | Environment configuration |

### **Development Tools**
| Technology | Version | Purpose |
|------------|---------|---------|
| **Poetry** | Latest | Dependency management |
| **python-dotenv** | 1.0.1 | Environment variable management |
| **Black** | 24.8.0 | Code formatting |
| **Ruff** | 0.6.9 | Fast Python linter |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend Application                     │
│                    (React/Vue/Next.js - Separate)                │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP/REST API
                         │ WebSocket/SSE
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI Backend (main.py)                   │
│  ┌───────────────┐  ┌───────────────┐  ┌──────────────────┐   │
│  │   Auth Router │  │  Chat Router  │  │  Student Router  │   │
│  │  (JWT/OAuth)  │  │  (Streaming)  │  │   (CRUD APIs)    │   │
│  └───────┬───────┘  └───────┬───────┘  └────────┬─────────┘   │
│          │                   │                    │              │
│  ┌───────▼───────────────────▼────────────────────▼─────────┐  │
│  │              Services Layer (services/)                   │  │
│  │  • auth.py        • chat_history.py    • students.py    │  │
│  │  • users.py       • voice.py                             │  │
│  └────────────────────┬──────────────────────────────────────┘  │
│                       │                                          │
│  ┌────────────────────▼─────────────────────────────────────┐  │
│  │          LangGraph AI Agent (agent/graph.py)             │  │
│  │  ┌──────────────────────────────────────────────────┐   │  │
│  │  │   React Agent with Tool Calling (create_react)   │   │  │
│  │  └────────┬─────────────────────────────────────────┘   │  │
│  │           │                                               │  │
│  │  ┌────────▼─────────────────────────────────────────┐   │  │
│  │  │              Tools (agent/tools.py)               │   │  │
│  │  │  • Student CRUD Tools                            │   │  │
│  │  │  • Analytics Tools                               │   │  │
│  │  │  • UAF Knowledge Search (RAG)                    │   │  │
│  │  │  • Web Search Tool                               │   │  │
│  │  │  • Email Tool                                    │   │  │
│  │  │  • Campus Info Tools                             │   │  │
│  │  └──────────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                       │                                          │
│  ┌────────────────────▼─────────────────────────────────────┐  │
│  │      RAG Agent (agent/ragagent.py) - UAF Knowledge      │  │
│  │  ┌──────────────┐    ┌──────────────┐                  │  │
│  │  │  Knowledge   │    │  Web Search  │                  │  │
│  │  │  Base (JSON) │    │  (DuckDuckGo)│                  │  │
│  │  └──────────────┘    └──────────────┘                  │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      MongoDB Database                            │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  students   │  │  chat_history│  │  users               │  │
│  │  collection │  │  collection  │  │  collection          │  │
│  └─────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

        ┌─────────────────────────────────────────┐
        │      External Services & APIs           │
        ├─────────────────────────────────────────┤
        │  • OpenAI GPT-4o-mini (LLM)            │
        │  • ElevenLabs (Text-to-Speech)         │
        │  • DuckDuckGo (Web Search)             │
        │  • SMTP Server (Email)                  │
        └─────────────────────────────────────────┘
```

### **Agent Workflow (LangGraph)**

```
User Query → LangGraph Agent (create_react_agent)
                    ↓
            [System Message]
                    ↓
        ┌───────────────────────┐
        │   Tool Selection      │ ← GPT-4o-mini decides which tool(s)
        │   (by LLM)            │   to use based on user query
        └──────┬────────────────┘
               │
               ├──→ Student CRUD Tools (if student data query)
               ├──→ Analytics Tools (if analytics query)
               ├──→ UAF RAG Tool (if UAF university query)
               │     └──→ Knowledge Base Search
               │     └──→ Web Search Fallback
               ├──→ Web Search (if general query)
               ├──→ Email Tool (if notification needed)
               └──→ Campus Info Tools (cafeteria, library, events)
                    ↓
            [Tool Execution]
                    ↓
            [LLM Generates Response]
                    ↓
            [Stream to User / Save to Chat History]
```

---

## 📁 Project Structure

```
backend/
├── 📄 main.py                      # FastAPI application entry point
├── 📄 settings.py                  # Configuration and environment settings
├── 📄 db.py                        # MongoDB connection manager
├── 📄 schemas.py                   # Pydantic models for API validation
├── 📄 pyproject.toml               # Poetry dependencies and project metadata
├── 📄 env.example                  # Environment variables template
├── 📄 AUTH_README.md               # Authentication system documentation
├── 📄 add_sample_students.py       # Script to populate sample student data
│
├── 📁 agent/                       # AI Agent implementation
│   ├── 📄 __init__.py
│   ├── 📄 graph.py                 # LangGraph agent orchestration
│   ├── 📄 tools.py                 # Agent tools (student, analytics, search)
│   └── 📄 ragagent.py              # RAG agent for UAF knowledge base
│
├── 📁 models/                      # Database models
│   ├── 📄 __init__.py
│   ├── 📄 student.py               # Student data models
│   └── 📄 user.py                  # User authentication models
│
├── 📁 routers/                     # API route handlers
│   ├── 📄 __init__.py
│   ├── 📄 auth.py                  # Authentication endpoints (login, signup)
│   ├── 📄 chat.py                  # Chat and streaming endpoints
│   ├── 📄 students.py              # Student CRUD endpoints
│   └── 📄 analytics.py             # Analytics and reporting endpoints
│
├── 📁 services/                    # Business logic layer
│   ├── 📄 __init__.py
│   ├── 📄 auth.py                  # JWT and password utilities
│   ├── 📄 users.py                 # User database operations
│   ├── 📄 students.py              # Student database operations
│   ├── 📄 chat_history.py          # Chat history management
│   └── 📄 voice.py                 # Voice processing (STT/TTS)
│
├── 📁 scripts/                     # Utility scripts
│   ├── 📄 create_admin.py          # Create admin user
│   └── 📄 seed_mongo.py            # Seed database with sample data
│
└── 📁 uaf_data/                    # UAF University knowledge base
    ├── 📄 ragagent.py              # Standalone RAG agent
    └── 📄 uaf_scraped_data.json    # Scraped UAF university data
```

---

## 🚀 Installation

### **Prerequisites**

Before you begin, ensure you have the following installed:

- **Python 3.11 or higher**
- **MongoDB 6.0+** (local or MongoDB Atlas)
- **Poetry** (Python dependency manager)
- **Git**

### **Step 1: Clone the Repository**

```bash
git clone https://github.com/your-username/ai-campus-admin-agent.git
cd ai-campus-admin-agent/backend
```

### **Step 2: Install Poetry (if not already installed)**

```bash
# macOS/Linux
curl -sSL https://install.python-poetry.org | python3 -

# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

### **Step 3: Install Dependencies**

```bash
poetry install
```

This will create a virtual environment and install all required dependencies from `pyproject.toml`.

### **Step 4: Set Up Environment Variables**

```bash
# Copy the example environment file
cp env.example .env
```

Edit the `.env` file with your actual configuration values (see [Configuration](#-configuration) section).

### **Step 5: Start MongoDB**

**Option A: Local MongoDB**
```bash
# macOS (with Homebrew)
brew services start mongodb-community

# Linux
sudo systemctl start mongod

# Windows
# Start MongoDB service from Services app
```

**Option B: MongoDB Atlas (Cloud)**
- Create a free cluster at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- Get your connection string
- Update `MONGODB_URI` in `.env`

### **Step 6: Create Admin User (Optional)**

```bash
poetry run python scripts/create_admin.py
```

This creates an admin user with:
- **Username**: `admin`
- **Email**: `admin@campus.edu`
- **Password**: `admin123` (⚠️ **Change in production!**)

### **Step 7: Seed Sample Data (Optional)**

```bash
poetry run python add_sample_students.py
```

### **Step 8: Run the Application**

```bash
# Development mode (with auto-reload)
poetry run python main.py

# Or using Uvicorn directly
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

---

## ⚙️ Configuration

### **Environment Variables**

Create a `.env` file in the `backend/` directory with the following variables:

```env
# =============================================================================
# APPLICATION SETTINGS
# =============================================================================
ENVIRONMENT=development
API_PORT=8000
SECRET_KEY=your-super-secret-key-change-this-in-production

# =============================================================================
# AI SERVICES
# =============================================================================
# OpenAI API Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here
AGENT_MODEL=gpt-4o-mini

# ElevenLabs API Configuration (for voice features)
ELEVENLABS_API_KEY=your-elevenlabs-api-key-here

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================
# MongoDB Connection
MONGODB_URI=mongodb://localhost:27017
MONGO_URI=mongodb://localhost:27017
MONGODB_DB=ai_campus

# For MongoDB Atlas (cloud):
# MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
# MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/

# =============================================================================
# EMAIL CONFIGURATION (SMTP)
# =============================================================================
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password-here
SMTP_USE_TLS=true
SMTP_USE_SSL=false
EMAIL_FROM=notifications@yourdomain.com

# =============================================================================
# CORS CONFIGURATION
# =============================================================================
ALLOW_ORIGINS=http://localhost:8080,http://localhost:5173,http://localhost:3000
ALLOW_METHODS=*
ALLOW_HEADERS=*

# =============================================================================
# JWT AUTHENTICATION
# =============================================================================
JWT_SECRET_KEY=your-jwt-secret-key-change-this-to-something-secure
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### **Getting API Keys**

1. **OpenAI API Key**:
   - Visit [OpenAI Platform](https://platform.openai.com/api-keys)
   - Create an account and generate an API key
   - Add billing information (GPT-4o-mini is cost-effective)

2. **ElevenLabs API Key** (for voice features):
   - Visit [ElevenLabs](https://elevenlabs.io/)
   - Sign up and get your API key from the dashboard

3. **Gmail App Password** (for email notifications):
   - Enable 2-factor authentication on your Google account
   - Go to Google Account → Security → App passwords
   - Generate an app password for this application

---

## 📚 API Documentation

### **Base URL**

```
http://localhost:8000
```

### **Interactive API Docs**

FastAPI provides automatic interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### **API Endpoints Overview**

#### **🏠 General**

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API information and welcome message |
| `GET` | `/health` | Health check endpoint |

#### **🔐 Authentication**

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/auth/signup` | Register new user | ❌ No |
| `POST` | `/auth/login` | Login user (returns JWT) | ❌ No |
| `POST` | `/auth/token` | OAuth2 compatible login | ❌ No |
| `GET` | `/auth/me` | Get current user info | ✅ Yes |
| `GET` | `/auth/users` | List all users | ✅ Admin |
| `GET` | `/auth/users/{user_id}` | Get user by ID | ✅ Admin |

#### **👨‍🎓 Students**

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/students/` | Add new student | ✅ Optional |
| `GET` | `/students/` | List all students | ✅ Optional |
| `GET` | `/students/{student_id}` | Get student by ID | ✅ Optional |
| `PUT` | `/students/{student_id}` | Update student | ✅ Optional |
| `DELETE` | `/students/{student_id}` | Delete student | ✅ Optional |
| `GET` | `/students/analytics/overview` | Student analytics | ✅ Optional |

#### **📊 Analytics**

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/analytics/` | Comprehensive analytics summary | ✅ Optional |

#### **💬 Chat**

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/chat/authenticated` | Chat with AI (authenticated) | ✅ Yes |
| `POST` | `/chat` | Chat with AI (public) | ❌ No |
| `GET` | `/stream` | Streaming chat (SSE, authenticated) | ✅ Yes |
| `POST` | `/stream` | Streaming chat (public) | ❌ No |
| `GET` | `/history/me` | Get my chat history | ✅ Yes |
| `DELETE` | `/history/me` | Delete my chat history | ✅ Yes |
| `GET` | `/history/{user_id}` | Get user chat history | ✅ Optional |
| `DELETE` | `/history/{user_id}` | Delete user chat history | ✅ Optional |
| `GET` | `/history/users/recent` | Get recent chat users | ✅ Optional |
| `GET` | `/history/statistics` | Get chat statistics | ✅ Optional |

#### **🎤 Voice**

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/voice-to-text` | Convert voice to text | ❌ No |
| `POST` | `/text-to-speech` | Convert text to speech | ❌ No |
| `GET` | `/voices` | Get available ElevenLabs voices | ❌ No |

---

## 💻 Usage Examples

### **1. Register a New User**

```bash
curl -X POST "http://localhost:8000/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "username": "johndoe",
    "password": "securepassword123",
    "full_name": "John Doe"
  }'
```

**Response:**
```json
{
  "id": "65abc123def456789",
  "email": "john.doe@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "is_active": true,
  "is_admin": false,
  "created_at": "2025-10-12T10:30:00Z",
  "updated_at": "2025-10-12T10:30:00Z"
}
```

### **2. Login and Get JWT Token**

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "securepassword123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### **3. Chat with AI (Authenticated)**

```bash
curl -X POST "http://localhost:8000/chat/authenticated" \
  -