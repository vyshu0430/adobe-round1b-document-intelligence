
# Round 1B – Persona-Driven Document Intelligence

This project is part of Adobe's "Connecting the Dots" Challenge – Round 1B. It processes a collection of PDF documents and extracts the most relevant sections and sub-sections based on an inferred user persona and job-to-be-done.

## 🧠 Key Features

- Automatically infers persona and task from PDFs
- Extracts and ranks headings (H1, H2, H3)
- Ranks sub-sections by semantic relevance using transformer embeddings
- Outputs results in structured JSON format
- Fully Dockerized, offline, and CPU-compliant

## 📁 Folder Structure

```
.
├── input/                 # Folder containing input PDFs
├── output/                # Output result.json
├── all-MiniLM-L6-v2/      # Pre-downloaded model
├── main_b.py              # Main script
├── Dockerfile             # Docker setup
├── requirements.txt       # Dependencies
├── approach_explanation.md
├── README.md
```

## ⚙️ Build & Run Instructions

### 🔧 Build Docker Image
```
docker build --platform linux/amd64 -t round1b_solution:v1 .
```

### 🚀 Run the Container
```
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none round1b_solution:v1
```

## 🛠 Requirements

- Python 3.10
- PyMuPDF
- sentence-transformers
- torch

## 📦 Model Info

- Model: `all-MiniLM-L6-v2` (from sentence-transformers)
- Size: ~90MB
- Stored locally in: `all-MiniLM-L6-v2/` folder for offline usage

---

This solution is fully self-contained, platform-independent, and complies with all performance, offline, and CPU-only constraints defined in the challenge.
