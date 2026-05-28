# AI-Powered E-Commerce Business Analyzer

A full AI system that takes your e-commerce business data, identifies problems,
recommends strategies, generates a human-like explanation, and produces a
downloadable PDF report — all in one Streamlit web app.

---

## Project Structure

```
ecommerce_analyzer/
├── app.py                  ← Main app (run this)
├── requirements.txt        ← All Python packages
├── .env.example            ← Template for API key
├── models/
│   ├── problem_detector.py ← Detects business problems with confidence scores
│   └── strategy_engine.py  ← Maps problems → actionable strategies
├── utils/
│   └── explainer.py        ← HuggingFace LLM explanation generator
└── report/
    └── pdf_generator.py    ← Creates the downloadable PDF report
```

---

## HOW TO SET UP (complete beginner guide)

### STEP 1 — Install Python

1. Go to https://www.python.org/downloads/
2. Download **Python 3.11** (click the big yellow button)
3. Run the installer
4. IMPORTANT: On the first screen, tick **"Add Python to PATH"**
5. Click "Install Now"
6. Verify: open **Command Prompt** (Windows) or **Terminal** (Mac/Linux)
   and type: `python --version`
   You should see: `Python 3.11.x`

---

### STEP 2 — Install VS Code (code editor)

1. Go to https://code.visualstudio.com/
2. Download and install it (it's free)
3. Open VS Code

---

### STEP 3 — Open the project folder in VS Code

1. Open VS Code
2. Click **File → Open Folder**
3. Navigate to and select the `ecommerce_analyzer` folder
4. Click **"Open"**

---

### STEP 4 — Open Terminal inside VS Code

1. In VS Code, click **Terminal → New Terminal** (from the top menu)
2. A terminal panel opens at the bottom of VS Code

---

### STEP 5 — Install all required packages

In the VS Code terminal, type this command and press Enter:

```bash
pip install -r requirements.txt
```

Wait for it to finish (may take 1–3 minutes). You'll see lots of text — that's normal.

---

### STEP 6 — Set up your FREE HuggingFace API key (for AI explanations)

This gives you better AI-powered explanations. Without it the app still works
using smart built-in templates.

1. Go to https://huggingface.co and click **Sign Up** (free)
2. After logging in, click your profile picture → **Settings**
3. Click **Access Tokens** in the left menu
4. Click **"New token"**
5. Give it any name (e.g. "business-analyzer")
6. Role: select **"Read"**
7. Click **"Generate a token"**
8. Copy the token (it starts with `hf_...`)

Now:
1. In your project folder, find the file called `.env.example`
2. Make a copy of it and rename the copy to `.env`
3. Open `.env` and replace `your_huggingface_token_here` with your token:
   ```
   HF_API_TOKEN=hf_your_actual_token_here
   ```
4. Save the file

---

### STEP 7 — Run the app!

In the VS Code terminal, type:

```bash
streamlit run app.py
```

Your browser will automatically open to:
```
http://localhost:8501
```

The app is now running!

---

## HOW TO USE THE APP

1. **Step 1**: Enter your business name, type, and revenue target
2. **Step 2**: Enter your monthly sales, traffic, and conversion rate
3. **Step 3**: Enter marketing spend, retention rate, and inventory
4. **Step 4**: Review your data and click **"Analyze My Business"**
5. **Results**: See your health score, problems, strategies, and AI explanation
6. **Download**: Click "Generate PDF Report" to get a full 4–5 page report

---

## TROUBLESHOOTING

**"pip is not recognized"**
→ Python was not added to PATH. Re-install Python and tick "Add Python to PATH"

**"ModuleNotFoundError"**
→ Run `pip install -r requirements.txt` again in the terminal

**"streamlit is not recognized"**
→ Try `python -m streamlit run app.py` instead

**App opens but shows an error**
→ Check the terminal for the red error message and share it for help

**AI explanation is generic / template-based**
→ You haven't added your HuggingFace token to the `.env` file (see Step 6)

---

## WHAT THE APP DOES

| Component | What it does |
|---|---|
| Multi-step Wizard | Collects your business data across 4 beautiful screens |
| Problem Detector | Identifies issues like low conversion, poor ROI, overstock |
| Confidence Score | Shows how certain the system is about each problem (60–95%) |
| Strategy Engine | Maps each problem to proven short-term and long-term actions |
| AI Explainer | Generates a human-like paragraph using Mistral 7B (HuggingFace) |
| Radar Chart | Visual comparison of your metrics vs industry benchmarks |
| PDF Generator | Creates a professional 4–5 page downloadable report |

---

## Technologies Used

- **Python 3.11** — Programming language
- **Streamlit** — Web UI framework
- **Plotly** — Interactive charts
- **Scikit-learn** — ML foundations
- **HuggingFace API** — Free LLM (Mistral 7B)
- **ReportLab** — PDF generation
- **python-dotenv** — Environment variable management


