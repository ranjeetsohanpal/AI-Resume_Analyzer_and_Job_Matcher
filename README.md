# 🧠 AI Resume Analyzer & Job Matcher

An intelligent web application that analyzes uploaded resumes, extracts skills and summaries, and recommends the top matching jobs using NLP and semantic similarity models.

## 🔍 Overview

This project uses Natural Language Processing (NLP) techniques and a sentence transformer model (`all-MiniLM-L6-v2`) to:
- Extract structured data (name, skills, summary) from PDF resumes
- Find and rank the top 3 job descriptions that best match the resume
- Highlight missing skills for each job match

The frontend is built with **React** and the backend is powered by **Flask** and **Python**.

---

## 🚀 Features

- 📄 Upload and parse resumes (PDF format)
- 🤖 AI-powered semantic matching using Sentence Transformers
- ✅ Display top job matches with score and missing skills
- 💡 Clean UI with detailed skill/job breakdown

---

## 📦 Tech Stack

### 🔧 Backend
- Python
- Flask
- SentenceTransformers (`all-MiniLM-L6-v2`)
- Custom Resume Parser

### 🎨 Frontend
- React
- Tailwind CSS (for styling)

---

## 🧪 How It Works

1. **User uploads a PDF resume**
2. **Flask backend parses**:
   - Name
   - Summary
   - Skills
3. **Job Matcher** uses sentence transformer to compare resume summary with job descriptions
4. **Top matches are returned** along with:
   - Similarity score
   - Missing required skills
5. **React frontend displays** all this in a clean, readable format

---
