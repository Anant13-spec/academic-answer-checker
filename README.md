# Academic Answer Quality Checker

An NLP-powered web application that evaluates a student's written answer against a model answer and provides a detailed quality assessment.

The system analyzes the answer using **semantic similarity, key-point coverage, grammar, and clarity**, then combines these metrics into an overall score and generates feedback.

---

## 🚀 Features

### Current Features

* 📝 Question, model answer, and student answer input
* 🧠 Semantic similarity using Sentence Transformers
* 📌 Key-point coverage detection
* ✍️ Grammar evaluation using LanguageTool
* 📖 Basic clarity evaluation
* 📊 Weighted overall score
* 💡 Automated feedback
* ✅ Covered concept detection
* ❌ Missing concept detection
* 📱 Responsive web interface

---

## 🧠 How It Works

The application evaluates a student's answer through multiple stages:

```text
                    Student Answer
                          │
                          ↓
                 ┌─────────────────┐
                 │  NLP Evaluation  │
                 └────────┬────────┘
                          │
          ┌───────────────┼───────────────┐
          ↓               ↓               ↓
    Semantic          Key Point        Grammar
    Similarity        Coverage         Analysis
          │               │               │
          └───────────────┼───────────────┘
                          ↓
                       Clarity
                          │
                          ↓
                   Weighted Scoring
                          │
                          ↓
                    Final Score
                          │
                          ↓
                       Feedback
```

---

## 📊 Evaluation Metrics

### 1. Semantic Similarity

The system uses:

```text
all-MiniLM-L6-v2
```

from Sentence Transformers to convert the model answer and student answer into semantic embeddings.

Cosine similarity is then used to estimate how closely their meanings match.

This allows the system to recognize semantically similar answers even when different words are used.

---

### 2. Key-Point Coverage

The model answer is divided into individual points/sentences.

Each point is compared semantically with the student's answer.

The system identifies:

```text
✓ Covered Points
✗ Missing Points
```

The coverage percentage is calculated from the proportion of detected model-answer points covered by the student.

---

### 3. Grammar Score

Grammar is evaluated using:

```text
LanguageTool
```

The system detects grammatical errors and converts the detected error rate into a grammar score.

---

### 4. Clarity Score

The current clarity metric considers factors such as:

* Average sentence length
* Extremely long sentences
* Very short answers

This component is intentionally simple in the current version and will be improved in future iterations.

---

### 5. Final Score

The current weighted score is:

```text
Final Score =
    Semantic Similarity × 40%
  + Key Point Coverage × 30%
  + Grammar × 15%
  + Clarity × 15%
```

The result is displayed as the student's overall answer quality score.

---

## 🛠️ Tech Stack

### Backend

* Python
* Flask

### NLP / AI

* Sentence Transformers
* `all-MiniLM-L6-v2`
* scikit-learn
* LanguageTool
* NLTK

### Frontend

* HTML
* CSS
* Jinja2 Templates

### Development

* Git
* GitHub
* Python Virtual Environment

---

## 📁 Project Structure

```text
academic-answer-checker/
│
├── app.py
│
├── evaluator/
│   ├── __init__.py
│   ├── similarity.py
│   ├── coverage.py
│   ├── grammar.py
│   ├── clarity.py
│   ├── scoring.py
│   └── feedback.py
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Anant13-spec/academic-answer-checker.git
cd academic-answer-checker
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

#### Linux / macOS

```bash
source venv/bin/activate
```

#### Windows

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## 🤖 First Run

The application uses the:

```text
all-MiniLM-L6-v2
```

Sentence Transformer model.

On the first run, the model may need to be downloaded and cached locally. Subsequent runs should load it from the local cache.

---

## 🧪 Example

### Question

```text
Explain TCP.
```

### Model Answer

```text
TCP is a connection-oriented transport layer protocol.
It provides reliable data delivery, flow control, and
congestion control. TCP establishes a connection between
the sender and receiver before transmitting data.
```

### Student Answer

```text
TCP creates a connection between two devices before
communication. It ensures reliable delivery of data and
controls the rate of transmission to prevent network
congestion.
```

### Example Evaluation

```text
Semantic Similarity     82.27%
Key Point Coverage     100.00%
Grammar Score          100.00%
Clarity Score          100.00%

Final Score             92.91%
```

The exact score may vary depending on the input and model version.

---

## 🏗️ Architecture

The application follows a modular architecture.

```text
                     Flask Application
                            │
                            ↓
                         app.py
                            │
            ┌───────────────┼───────────────┐
            ↓               ↓               ↓
       similarity       coverage        grammar
            │               │               │
            └───────────────┼───────────────┘
                            ↓
                         clarity
                            │
                            ↓
                         scoring
                            │
                            ↓
                        feedback
                            │
                            ↓
                      Flask Template
                            │
                            ↓
                         Browser
```

Each evaluation component is separated into its own Python module, making the system easier to maintain and extend.

---

## 🔮 Future Improvements

The project is currently an evolving prototype. Planned improvements include:

### NLP Improvements

* [ ] Improve semantic similarity calibration
* [ ] Improve key-point extraction
* [ ] Improve missing-concept detection
* [ ] Improve clarity/readability analysis
* [ ] Add contradiction detection
* [ ] Add keyword and concept analysis
* [ ] Evaluate the system against a labeled dataset

### AI Features

* [ ] AI-generated detailed feedback
* [ ] AI-generated model answers
* [ ] Question difficulty analysis
* [ ] Answer improvement suggestions
* [ ] Personalized learning recommendations

### Application Features

* [ ] Student accounts
* [ ] Teacher accounts
* [ ] Authentication and authorization
* [ ] Evaluation history
* [ ] Database integration
* [ ] Dashboard and analytics
* [ ] Export evaluation reports
* [ ] Multiple question types

### Engineering

* [ ] Unit testing
* [ ] API layer
* [ ] Error handling improvements
* [ ] Logging
* [ ] Docker support
* [ ] Cloud deployment
* [ ] CI/CD pipeline

---

## 🎯 Project Goal

The long-term goal is to build an intelligent academic evaluation system that goes beyond simple keyword matching and evaluates answers based on **meaning, concept coverage, language quality, and clarity**.

---

## 👨‍💻 Author

**Anant Jain**

Computer Science & Engineering Student

GitHub:
https://github.com/Anant13-spec
