
## Approach Explanation – Adobe "Connecting the Dots" Challenge – Round 1B

This solution is designed to intelligently analyze a collection of PDFs and extract the most relevant sections and sub-sections based on a specific user's persona and their job-to-be-done. The goal is to build a lightweight, offline, CPU-compatible system that ranks document segments semantically according to the user’s informational needs.

---

### 1. Document Parsing and Preprocessing

All input PDF documents are read from the `/app/input` directory. Using the `PyMuPDF` library (`fitz`), the program extracts:
- Structured section-level headings (using font-size heuristics to detect H1, H2, H3)
- Full text content from each page

Additionally, the first few pages (up to 3) of every PDF are scanned to gather introductory content which is later used to infer the persona and task.

---

### 2. Automatic Persona and Job Detection

Unlike hardcoded configurations, our system dynamically determines:
- **Persona** (e.g., PhD researcher, student, analyst) using keyword-based matching (e.g., "research", "student", "financial", "review")
- **Job-to-be-done** by detecting common task phrases like "benchmark", "prepare a review", "summarize", or "conduct a survey"

This makes the system generalizable and adaptive to different use cases without requiring external input files.

---

### 3. Semantic Ranking using Sentence Transformers

To determine relevance:
- The model `all-MiniLM-L6-v2` from Sentence Transformers is used to convert section headings and page text into vector embeddings
- The inferred job-to-be-done is also embedded
- **Cosine similarity** is computed between job embeddings and section embeddings

The top 5 most relevant sections (based on headings) and top 5 sub-sections (based on page-level content) are selected.

---

### 4. Output Format

The final JSON output (`result.json`) contains:
- Metadata including: input file names, inferred persona, job-to-be-done, and processing timestamp
- A list of top 5 relevant sections with document name, section title, page number, and importance rank
- A list of top 5 relevant sub-sections (text blocks) with page number and content snippet

---

### 5. Performance and Constraints Compliance

This solution meets all performance and deployment constraints:
- Runs entirely on CPU
- Requires no internet connection
- Processes 3–5 documents in under 60 seconds
- Uses a model under 100MB
- Fully Dockerized with support for AMD64 architecture

---

This modular and intelligent document processor is designed to scale to new personas and job contexts and provides a foundation for a more interactive PDF experience in future phases of the challenge.
