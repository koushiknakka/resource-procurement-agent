# 🛒 Resource Procurement Agent

Welcome to the **Resource Procurement Agent**! This is a smart, AI-driven application designed to streamline the process of procuring resources (like lab equipment, materials, etc.). Instead of manually searching and comparing vendors, you simply tell the agent what you need in natural language, and it handles the rest—extracting your requirements, analyzing options, and generating a detailed, ranked report of the best choices.

---

## 🌟 What is it?

The Resource Procurement Agent is a full-stack application built with modern technologies. It consists of two main parts:

1. **The Brain (Backend):** A Python-based AI agent built using **LangGraph** and **LangChain** (powered by Google GenAI). It processes your request through a step-by-step pipeline:
   - **Extractor:** Figures out exactly *what* you want and *how many*.
   - **Analyzer:** Searches through datasets to find the best vendors and ranks them.
   - **Formatter:** Packages all this data into a beautiful, easy-to-read markdown report.
   This brain is exposed to the web via a lightning-fast **FastAPI** server.

2. **The Face (Frontend):** A sleek, modern web interface built with **React**, **TypeScript**, and **Vite**. It gives you a clean chat-like interface to talk to the agent and displays the generated reports with proper formatting (thanks to `react-markdown`).

---

## 🛠️ Tech Stack

- **Backend:** Python (>=3.13), FastAPI, LangGraph, LangChain, Google GenAI
- **Frontend:** React (v18), TypeScript, Vite, TailwindCSS (assumed), Lucide React
- **Package Management:** `uv` (for blazing fast Python dependency management) and `npm`

---

## 📁 Project Structure

Here is a quick map of the repository so you know where everything lives:

```text
resource-procurement-agent/
├── .env                 # Environment variables (API keys go here)
├── datasets/            # Folder containing vendor/product data for the agent to analyze
├── frontend/            # The React web application
│   ├── src/             # Frontend source code (components, styles)
│   ├── package.json     # Node.js dependencies
│   └── vite.config.ts   # Vite bundler configuration
├── src/                 # The core Python AI Agent code
│   ├── nodes/           # The individual steps of the LangGraph (extractor, analyzer, formatter)
│   └── state.py         # Defines the data that flows between nodes
├── main.py              # A command-line script to test the agent without running the web server
├── server.py            # The FastAPI web server that connects the agent to the frontend
├── pyproject.toml       # Python project metadata and dependencies
└── uv.lock              # Lockfile for reproducible Python environments
```

---

## 🚀 How to Get It Running

Follow these step-by-step instructions to get the Resource Procurement Agent running on your local machine.

### Step 1: Prerequisites
Before you start, make sure you have the following installed on your computer:
- **Python 3.13** or higher.
- **Node.js** (v18 or higher recommended).
- **uv** (Optional but highly recommended for managing Python packages. Install it from [Astral's website](https://docs.astral.sh/uv/)).
- A **Google Gemini API Key** (You can get one from Google AI Studio).

### Step 2: Clone & Set Up the Backend
1. Open your terminal and navigate to the root folder of this project (`resource-procurement-agent`).
2. Create your environment variables file. Create a file named `.env` in the root folder and add your Google API key:
   ```env
   GOOGLE_API_KEY="your_google_gemini_api_key_here"
   ```
3. Install the Python dependencies. If you are using `uv`:
   ```bash
   uv venv
   # Activate the virtual environment
   # On Windows: .venv\Scripts\activate
   # On Mac/Linux: source .venv/bin/activate
   
   # Install dependencies
   uv pip install -e .
   ```
   *(If you prefer standard pip, you can run `pip install -r requirements.txt`)*

### Step 3: Set Up the Frontend
1. Keep your backend terminal open, but open a *new* terminal window.
2. Navigate into the frontend folder:
   ```bash
   cd frontend
   ```
3. Install the Node.js dependencies:
   ```bash
   npm install
   ```

### Step 4: Launch the Application!
To use the app, you need to run both the backend server and the frontend server at the same time.

**Terminal 1 (Backend):**
Make sure you are in the root `resource-procurement-agent` folder and your virtual environment is active.
```bash
uvicorn server:api_server --reload --port 8000
```
*Your API is now running at `http://localhost:8000`.*

**Terminal 2 (Frontend):**
Make sure you are inside the `frontend` folder.
```bash
npm run dev
```
*Your React app will start. The terminal will give you a local URL (usually `http://localhost:5173`).*

**Click that URL, open it in your browser, and start asking the agent for procurement help!**

---

## 🧪 Testing the Agent in the Terminal
If you just want to test the LangGraph pipeline without booting up the web interface, you can run the `main.py` script directly:

```bash
python main.py
```
This will run a pre-programmed test query ("The EEE power systems lab needs to replace some old burned out light blocks...") and print the step-by-step reasoning and final report directly in your console.
