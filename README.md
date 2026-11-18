# Medical Symptom Summarizer

An AI-powered medical symptom summarization application built using **Python, OpenAI GPT-4o, Streamlit, and Pydantic**.

## Overview

Healthcare professionals often receive patient symptom descriptions in unstructured formats. Manually reviewing these descriptions can take time and make important information harder to identify.

The Medical Symptom Summarizer converts a patient's written symptom description into a structured summary using GPT-4o.

The application extracts:

- **Chief Complaint** – Main reason for seeking medical attention
- **Onset** – When the symptoms started
- **Duration** – How long the symptoms have been present
- **Severity** – Pain or symptom severity on a scale of 1–10, when provided
- **Red Flags** – Potentially concerning symptoms
- **Triage Level** – Low, moderate, or high urgency

> **Disclaimer:** This application is a summarization tool, not a diagnostic system. It does not replace professional medical judgment. All outputs must be reviewed by a qualified healthcare professional.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| OpenAI GPT-4o | Symptom summarization |
| Streamlit | Web application interface |
| Pydantic | Output validation |
| Pytest | Automated testing |
| python-dotenv | Environment variable management |

## System Architecture

1. Patient enters a symptom description.
2. Streamlit receives the input.
3. The prompt builder prepares the instructions and patient message.
4. GPT-4o processes the description and returns JSON.
5. Pydantic validates the generated response.
6. Streamlit displays the structured summary.
7. The user can export the result as JSON.

## Project Structure

```text
project-01-medical-symptom-summarizer/
│
├── app/
│   ├── streamlit_app.py
│   ├── prompt_builder.py
│   └── validator.py
│
├── tests/
│   └── test_prompts.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/umajety/medical-symptom-summarizer.git
cd medical-symptom-summarizer
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the OpenAI API key

Create a `.env` file in the project root and add:

```text
OPENAI_API_KEY=your_openai_api_key
```

Replace the placeholder with your own API key.

**Never upload your `.env` file or API key to GitHub.**

### 5. Run the application

```bash
streamlit run app/streamlit_app.py
```

Streamlit will open the application in your browser.

## Running Tests

Run the automated tests from the project root:

```bash
python -m pytest tests/test_prompts.py -v
```

The test suite contains 10 test cases covering:

- User message formatting
- System prompt instructions
- Valid response validation
- Invalid severity values
- Invalid triage levels
- Missing required fields
- Optional fields
- Default red flags
- Minimum and maximum severity values

## Key Features

- AI-powered symptom summarization
- Structured JSON responses
- Pydantic validation
- Triage categorization
- Automatic API retry handling
- Session-based summary history
- JSON export
- Automated unit tests

## Future Improvements

- SOAP note generation
- Batch processing of patient records using CSV
- Secure database integration
- User authentication
- Usage monitoring and logging
- Deployment as a password-protected web application

## Author

**Upamanyu Majety**

GitHub: [@umajety](https://github.com/umajety)