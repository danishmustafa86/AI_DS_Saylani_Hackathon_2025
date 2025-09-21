# 🎓 AI Campus Admin Agent

> **An intelligent campus administration system powered by AI, built for the Saylani Hackathon 2025**

![AI Campus Admin](https://img.shields.io/badge/AI-Powered-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green) ![React](https://img.shields.io/badge/React-18-blue) ![TypeScript](https://img.shields.io/badge/TypeScript-5-blue) ![MongoDB](https://img.shields.io/badge/MongoDB-7-green)

## 🌟 Overview

AI Campus Admin Agent is a comprehensive web application designed to revolutionize campus administration through artificial intelligence. It combines modern web technologies with AI capabilities to provide an intuitive, efficient, and powerful platform for managing student data, analytics, and administrative tasks.

## ✨ Key Features

### 🤖 **AI-Powered Assistant**
- **Real-time Chat Interface** with streaming responses
- **Intelligent Query Processing** using OpenAI GPT models
- **Context-Aware Responses** for administrative queries
- **Voice Integration** with ElevenLabs text-to-speech
- **Persistent Chat History** with full conversation tracking

### 👥 **Student Management System**
- **Complete CRUD Operations** for student records
- **Advanced Search & Filtering** by name, department, email
- **Department-wise Organization** with visual breakdowns
- **Bulk Import/Export** capabilities
- **Real-time Data Validation** and error handling

### 📊 **Analytics Dashboard**
- **Interactive Charts** with Recharts library
- **Department Distribution** with pie charts and bar graphs
- **Student Growth Trends** over time
- **Activity Tracking** and engagement metrics
- **Exportable Reports** for administrative use

### 🔐 **Authentication & Security**
- **JWT-based Authentication** with secure token management
- **Role-based Access Control** (Admin/User roles)
- **Password Encryption** using bcrypt
- **Session Management** with automatic token refresh
- **Protected Routes** and API endpoints

### 🎨 **Modern UI/UX**
- **Responsive Design** for all device sizes
- **Dark/Light Theme** support
- **Beautiful Animations** and transitions
- **Accessible Components** following WCAG guidelines
- **Professional Design System** with consistent styling

## 🛠️ Technology Stack

### **Backend**
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern, fast web framework for building APIs
- **[Python 3.11+](https://python.org/)** - Core programming language
- **[MongoDB](https://mongodb.com/)** - NoSQL database for flexible data storage
- **[Motor](https://motor.readthedocs.io/)** - Async MongoDB driver
- **[Pydantic](https://pydantic.dev/)** - Data validation and settings management
- **[OpenAI API](https://openai.com/api/)** - GPT models for AI responses
- **[ElevenLabs API](https://elevenlabs.io/)** - Text-to-speech conversion
- **[Python-JOSE](https://python-jose.readthedocs.io/)** - JWT token handling
- **[Passlib](https://passlib.readthedocs.io/)** - Password hashing
- **[Uvicorn](https://uvicorn.org/)** - ASGI server

### **Frontend**
- **[React 18](https://reactjs.org/)** - Modern UI library
- **[TypeScript](https://typescriptlang.org/)** - Type-safe JavaScript
- **[Vite](https://vitejs.dev/)** - Fast build tool and dev server
- **[React Router](https://reactrouter.com/)** - Client-side routing
- **[TanStack Query](https://tanstack.com/query)** - Server state management
- **[Zustand](https://zustand-demo.pmnd.rs/)** - Lightweight state management
- **[Tailwind CSS](https://tailwindcss.com/)** - Utility-first CSS framework
- **[Shadcn/ui](https://ui.shadcn.com/)** - Beautiful UI components
- **[Recharts](https://recharts.org/)** - Composable charting library
- **[Axios](https://axios-http.com/)** - HTTP client for API calls
- **[React Hook Form](https://react-hook-form.com/)** - Performant forms

### **Development & Deployment**
- **[Poetry](https://python-poetry.org/)** - Python dependency management
- **[ESLint](https://eslint.org/)** - JavaScript/TypeScript linting
- **[Prettier](https://prettier.io/)** - Code formatting
- **[Git](https://git-scm.com/)** - Version control

## 🚀 Quick Start

### Prerequisites
- **Python 3.11+**
- **Node.js 18+**
- **MongoDB** (local or Atlas)
- **OpenAI API Key**

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ai-campus-admin.git
cd ai-campus-admin
```

### 2. Backend Setup
```bash
# Navigate to backend
cd backend

# Install Poetry (if not installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Setup environment
cp env.example .env
# Edit .env and add your API keys

# Start the backend
poetry run python main.py
```

### 3. Frontend Setup
```bash
# Navigate to frontend (in new terminal)
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 4. Access the Application
- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend` directory:

```env
# AI Services
OPENAI_API_KEY=sk-your-openai-api-key
ELEVENLABS_API_KEY=your-elevenlabs-key

# Database
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=ai_campus

# Security
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret

# Email (Optional)
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### MongoDB Setup

**Option 1: Local MongoDB**
```bash
# Install MongoDB locally
# Start MongoDB service
mongod --dbpath /path/to/data
```

**Option 2: MongoDB Atlas**
```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
```

## 📁 Project Structure

```
ai-campus-admin/
├── backend/                 # FastAPI backend
│   ├── routers/            # API route handlers
│   ├── services/           # Business logic
│   ├── models/             # Data models
│   ├── schemas/            # Pydantic schemas
│   ├── agent/              # AI agent logic
│   ├── db.py               # Database configuration
│   ├── settings.py         # Application settings
│   └── main.py             # Application entry point
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── lib/            # Utilities and API
│   │   ├── stores/         # State management
│   │   ├── types/          # TypeScript types
│   │   └── styles/         # CSS styles
│   ├── public/             # Static assets
│   └── package.json        # Dependencies
├── docs/                   # Documentation
└── README.md               # This file
```

## 🎯 Core Functionalities

### 🤖 AI Chat System
- **Streaming Responses**: Real-time AI responses with Server-Sent Events
- **Context Awareness**: Maintains conversation context across sessions
- **Voice Integration**: Text-to-speech for AI responses
- **History Management**: Persistent chat history with search capabilities

### 👨‍🎓 Student Management
- **CRUD Operations**: Create, read, update, delete student records
- **Search & Filter**: Advanced filtering by multiple criteria
- **Data Validation**: Comprehensive input validation and error handling
- **Export/Import**: CSV and JSON data exchange capabilities

### 📈 Analytics & Reporting
- **Visual Dashboards**: Interactive charts and graphs
- **Department Analytics**: Student distribution and trends
- **Activity Tracking**: User engagement and system usage
- **Custom Reports**: Exportable analytics reports

### 🔒 Security Features
- **Authentication**: Secure login/signup with JWT tokens
- **Authorization**: Role-based access control
- **Data Protection**: Encrypted passwords and secure API endpoints
- **Session Management**: Automatic token refresh and logout

## 🔌 API Endpoints

### Authentication
- `POST /auth/signup` - User registration
- `POST /auth/login` - User authentication
- `GET /auth/me` - Get current user info

### Students
- `GET /students/` - List all students
- `POST /students/` - Create new student
- `GET /students/{id}` - Get student by ID
- `PUT /students/{id}` - Update student
- `DELETE /students/{id}` - Delete student

### Analytics
- `GET /analytics/` - Get analytics summary
- `GET /students/analytics/overview` - Student analytics

### Chat
- `POST /chat/authenticated` - Send chat message
- `GET /stream` - Real-time streaming chat
- `GET /history/me` - Get chat history

## 🧪 Testing

### Backend Tests
```bash
cd backend
poetry run pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## 📦 Deployment

### Backend Deployment
```bash
# Production build
poetry build

# Run with Gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

### Frontend Deployment
```bash
# Build for production
npm run build

# Serve static files
npm run preview
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

## 📋 Development Guidelines

- **Code Style**: Follow PEP 8 for Python, ESLint/Prettier for TypeScript
- **Commits**: Use conventional commits format
- **Testing**: Write tests for new features
- **Documentation**: Update README and inline docs

## 🐛 Troubleshooting

### Common Issues

**Backend won't start**
- Check Python version (3.11+)
- Verify MongoDB connection
- Ensure all environment variables are set

**Frontend build errors**
- Clear node_modules: `rm -rf node_modules && npm install`
- Check Node.js version (18+)
- Verify all dependencies are installed

**API connection issues**
- Check CORS configuration
- Verify backend is running on port 8000
- Check network firewall settings

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏆 Hackathon Information

**Event**: Saylani Hackathon 2025 - AI & Data Science Track
**Team**: [Your Team Name]
**Category**: Campus Administration & AI Integration

## 🙏 Acknowledgments

- **Saylani Mass IT Training** for organizing the hackathon
- **OpenAI** for providing powerful AI models
- **FastAPI** and **React** communities for excellent frameworks
- **MongoDB** for flexible data storage solutions

## 📞 Support

For support, email [your-email@example.com] or join our [Discord server](https://discord.gg/your-server).

---

<div align="center">
  <strong>Built with ❤️ for Saylani Hackathon 2025</strong>
  <br>
  <sub>Empowering campus administration through AI</sub>
</div>
