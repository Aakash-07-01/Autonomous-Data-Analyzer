# Autonomous Data Analyzer

An automated, AI-powered CSV analytics dashboard built to streamline data profiling and exploratory data analysis (EDA). The application allows users to upload any CSV file, and an autonomous AI agent automatically processes the data, identifies trends, generates interactive charts, and produces a comprehensive HTML report. 

## Features

- **Automated Data Profiling:** Upload any CSV file to instantly get descriptive statistics, correlation heatmaps, and missing value analysis without writing any code.
- **Interactive Dashboards:** Auto-generates fully interactive Plotly charts and compiles them into a downloadable HTML report.
- **AI Agent Streaming:** Built with LangGraph and Server-Sent Events (SSE) to stream the AI agent's "thoughts" and progress in real-time on the frontend.
- **Reduced Analysis Time:** Cuts down manual EDA time from hours to minutes.
- **Modern UI:** A clean, responsive frontend built with React, TailwindCSS, and Framer Motion.

## Tech Stack

### Backend
- **Python 3**
- **FastAPI** - High-performance web framework for the API endpoints and SSE streaming.
- **LangGraph & LangChain** - Powers the autonomous agent workflow and reasoning capabilities.
- **Pandas** - Core data manipulation and statistical profiling.
- **Plotly** - Generation of interactive data visualizations.
- **Jinja2** - Templating for the final HTML report generation.

### Frontend
- **React 19**
- **Vite** - Lightning-fast build tool and dev server.
- **TailwindCSS** - Utility-first CSS framework for styling.
- **Framer Motion** - Smooth UI animations and transitions.
- **Axios & Server-Sent Events** - API communication and real-time streaming.

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the `backend` directory and add any required API keys (e.g., your LLM provider key):
   ```bash
   # Example .env
   GROQ_API_KEY=your_api_key_here
   ```
4. Start the FastAPI server:
   ```bash
   python main.py
   ```
   The backend will run on `http://localhost:8080`.

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install the Node.js dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`.

## How to Use

1. Open the frontend in your browser.
2. Drag and drop (or browse to select) a CSV file containing your dataset.
3. Watch the agent's real-time thought process as it analyzes the data, checks for missing values, computes correlations, and determines the best visualizations.
4. Once the analysis is complete, view the summary statistics and download the generated interactive HTML report!

## License
MIT License
