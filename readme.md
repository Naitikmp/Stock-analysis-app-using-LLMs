# Stock Analysis Application 📈

A Demo simple web application that provides intelligent stock analysis and recommendations using LangChain and OpenAI's GPT models. The application features a Flask backend for data processing and analysis, coupled with a sleek and simple Next.js frontend for an optimal user experience.


## ✨ Features

- Real-time stock analysis using LangChain and OpenAI's GPT models
- Historical stock data analysis using yfinance
- Web scraping for recent stock news
- Financial statement analysis
- Buy/Sell/Hold recommendations with detailed justification
- Clean and responsive user interface
- Secure API key handling

## 🔧 Technologies Used

### Backend
- Python 3.8+
- Flask
- LangChain
- OpenAI GPT models
- yfinance
- BeautifulSoup4
- DuckDuckGo Search(Not implemented and rather used google search)

### Frontend
- Next.js 13+
- TypeScript
- Tailwind CSS
- React Hooks

## 📋 Prerequisites

Before running the application, make sure you have:

- Python 3.8 or higher installed
- Node.js 14.0 or higher installed
- An OpenAI API key
- Git (for cloning the repository)

## 🚀 Installation

### Clone the Repository

```bash
git clone https://github.com/Naitikmp/Stock-analysis-app-using-LLMs
cd stock-analyzer
```

### Backend Setup

1. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Create a `.env` file in the backend directory (optional):
```env
FLASK_ENV=development
FLASK_APP=app.py
OPENAI_API_KEY="your key here"
```

### Frontend Setup

1. Install frontend dependencies:
```bash
cd ../frontend
npm install
```

2. Create a `.env.local` file (optional):
```env
NEXT_PUBLIC_API_URL=http://localhost:5000
```

## 🎯 Usage

### Starting the Backend

1. Navigate to the backend directory:
```bash
cd backend
python app.py
```
The Flask server will start on `http://localhost:5000`

### Starting the Frontend

1. In a new terminal, navigate to the frontend directory:
```bash
cd frontend
npm run dev
```
The Next.js application will start on `http://localhost:3000`

### Using the Application

1. Open your browser and go to `http://localhost:3000`
2. Enter your OpenAI API key in the secure input field
3. Enter the stock name you want to analyze
4. Click "Analyze Stock" and wait for the results
5. Review the comprehensive analysis including:
   - Historical price trends
   - Recent news analysis
   - Financial statement insights
   - Clear Buy/Sell/Hold recommendation
   - Detailed justification for the recommendation

## 📦 Project Structure

```
stock-analyzer/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── app/
│   │   └── page.tsx
│   ├── public/
│   ├── tailwind.config.ts
│   └── package.json
└── README.md
```

## 🔒 Security Considerations

- The application never stores OpenAI API keys
- API keys are transmitted securely and only used for the current session
- All API requests are made server-side to protect sensitive information
- CORS policies are implemented to prevent unauthorized access

## 🛠️ Development

### Backend Dependencies

```txt
flask==2.3.3
flask-cors==4.0.0
yfinance==0.2.28
beautifulsoup4==4.12.2
langchain==0.0.350
openai==1.3.5
requests==2.31.0
```

### Frontend Dependencies

```json
{
  "dependencies": {
    "next": "14.0.0",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "typescript": "5.2.2",
    "tailwindcss": "3.3.0"
  }
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License



## 🙏 Acknowledgments

- [OpenAI](https://openai.com/) for providing the GPT models
- [LangChain](https://langchain.com/) for the amazing framework
- [yfinance](https://pypi.org/project/yfinance/) for stock data
- [Pranav kushare](https://github.com/Pranav082001/stock-analyzer-bot)for reference
- All other open-source libraries used in this project
