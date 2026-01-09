# Google Calendar REST API for AI Receptionist

A Flask-based REST API that integrates with Google Calendar to enable AI receptionists to book appointments automatically.

## 🚀 Features

- **Google Calendar Integration** - OAuth2 authentication with Google Calendar API
- **REST API** - Simple endpoints for booking appointments
- **AI-Ready** - Designed to work with voice assistants and chatbots
- **Cloud Deployment** - Ready for Railway deployment
- **Testing Interface** - Built-in web form for testing bookings

## 📋 Prerequisites

- Python 3.9+
- Google Cloud Console project with Calendar API enabled
- Google OAuth2 credentials

## 🛠️ Setup

### 1. Clone the repository
```bash
git clone https://github.com/Gulenoor-Khalid/Google-calendar-RestApi-for-Ai-receptionist.git
cd Google-calendar-RestApi-for-Ai-receptionist
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Google OAuth2
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Calendar API
4. Create OAuth2 credentials (Web application)
5. Copy `credentials.example.json` to `credentials.json`
6. Fill in your actual Google OAuth2 credentials

### 4. Set environment variables
```bash
cp .env.example .env
# Edit .env with your actual values
```

### 5. Run the application
```bash
python app.py
```

## 🔧 API Usage

### Authorization
Visit `http://localhost:5000/authorize` to complete Google OAuth flow.

### Book Appointment
```bash
POST /add_event
Content-Type: application/json

{
  "summary": "Dental Appointment",
  "start_time": "2024-12-15T14:00:00Z",
  "end_time": "2024-12-15T15:00:00Z"
}
```

### Test Interface
Visit `http://localhost:5000/test` for a web-based booking form.

## 🧪 Testing

Run the automated test:
```bash
python test_booking.py
```

## 🚀 Deployment

This app is configured for Railway deployment:
- `Procfile` - Gunicorn configuration
- `runtime.txt` - Python version
- Environment-based settings

## 🔒 Security

- Sensitive files (`credentials.json`, `token.json`, `.env`) are gitignored
- OAuth2 flow with proper scopes
- Token refresh handling

## 📁 Project Structure

```
├── app.py              # Main Flask application
├── test_booking.py     # Automated testing script
├── requirements.txt    # Python dependencies
├── Procfile           # Railway deployment config
├── runtime.txt        # Python version
├── .gitignore         # Git ignore rules
├── credentials.example.json  # OAuth2 credentials template
└── .env.example       # Environment variables template
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.
---

## 👤Developer/Author

**Gul e Noor**  
AI Automations expert | AI Product Developer | AI Agents & Automation  
Smart Infrastructure & AI Applications  

- GitHub:https://github.com/Gulenoor-Khalid
- LinkedIn: www.linkedin.com/in/gul-e-noor-khalid  
- Email:gulenoor.ai.automation@gmail.com  
<!--
Author: Gule Noor
Role: AI Engineer, Generative AI Developer
Keywords: AI agents, generative AI, automation, smart infrastructure
-->

