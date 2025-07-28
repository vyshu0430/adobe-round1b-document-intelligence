import os
import fitz  # PyMuPDF
import json
from datetime import datetime
from sentence_transformers import SentenceTransformer, util

# --- Define persona and job ---


# --- Load embedding model ---
model = SentenceTransformer('./all-MiniLM-L6-v2')

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)
    persona = config["persona"]
    job_to_be_done = config["job_to_be_done"]


# --- Paths ---
INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"
RESULT_JSON = os.path.join(OUTPUT_DIR, "result.json")

# --- Helper: Extract headings & text ---
def extract_sections(pdf_path):
    doc = fitz.open(pdf_path)
    sections = []
    full_text_blocks = []

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        page_text = ""

        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    line_text = " ".join([span["text"] for span in line["spans"]])
                    font_size = max([span["size"] for span in line["spans"]])

                    # Determine heading level
                    if font_size > 20:
                        level = "H1"
                    elif 16 < font_size <= 20:
                        level = "H2"
                    elif 13 < font_size <= 16:
                        level = "H3"
                    else:
                        level = None  # Not a heading

                    if level:
                        sections.append({
                            "document": os.path.basename(pdf_path),
                            "page": page_num,
                            "section_title": line_text.strip(),
                            "text": line_text.strip()  # used for scoring
                        })

                    page_text += line_text + " "

        full_text_blocks.append({
            "document": os.path.basename(pdf_path),
            "page": page_num,
            "text": page_text.strip()
        })

    return sections, full_text_blocks

# --- Main process ---
def main():
    all_sections = []
    all_subsections = []
    input_docs = []

    # Step 1: Process all PDFs
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".pdf"):
            input_docs.append(filename)
            filepath = os.path.join(INPUT_DIR, filename)
            sections, subs = extract_sections(filepath)
            all_sections.extend(sections)
            all_subsections.extend(subs)

    # Step 2: Rank sections by relevance
    for section in all_sections:
        score = util.cos_sim(
            model.encode(job_to_be_done),
            model.encode(section["text"])
        ).item()
        section["score"] = score

    # Top N (e.g., 5) sections sorted by score
    top_sections = sorted(all_sections, key=lambda x: x["score"], reverse=True)[:5]

    # Step 3: Rank full paragraphs (sub-sections)
    for sub in all_subsections:
        score = util.cos_sim(
            model.encode(job_to_be_done),
            model.encode(sub["text"])
        ).item()
        sub["score"] = score

    top_subs = sorted(all_subsections, key=lambda x: x["score"], reverse=True)[:5]

    # Step 4: Format final output
    result = {
        "metadata": {
            "input_documents": input_docs,
            "persona": persona,
            "job_to_be_done": job_to_be_done,
            "processing_timestamp": datetime.utcnow().isoformat() + "Z"
        },
        "extracted_sections": [
            {
                "document": sec["document"],
                "page": sec["page"],
                "section_title": sec["section_title"],
                "importance_rank": rank + 1
            } for rank, sec in enumerate(top_sections)
        ],
        "sub_section_analysis": [
            {
                "document": sub["document"],
                "refined_text": sub["text"][:500],  # trim long content
                "page": sub["page"]
            } for sub in top_subs
        ]
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(RESULT_JSON, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print("✅ Output saved to result.json")

if __name__ == "__main__":
    main()
