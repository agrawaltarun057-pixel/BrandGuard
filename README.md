# 🛡️ BrandGuard
### Brand Compliance and Content Review System

BrandGuard is a web-based prototype designed to help teams manage
product information, marketing claims, and brand rules in one place.

The project aims to make brand-content review more structured by
bringing relevant product data, claims, and brand guidelines together.
Its longer-term goal is to help teams identify content inconsistencies
before publishing.

> **Project status:** Working web prototype. Advanced automated
> compliance analysis and a complete review workflow remain planned
> improvements.

---

## 🌐 Live Demo

- **Frontend:** https://agrawaltarun057-pixel.github.io/BrandGuard/
- **Backend:** https://brandguard-xcmp.onrender.com
- **Backend Health Check:** https://brandguard-xcmp.onrender.com/
- **Source Code:** https://github.com/agrawaltarun057-pixel/BrandGuard

The frontend is hosted on GitHub Pages, while the Python FastAPI
backend is deployed on Render.

---

## 🎯 Problem Statement

Product information and marketing content need to remain consistent
with approved product facts and brand guidelines.

Incorrect product details, mismatched prices, prohibited wording,
or unsupported claims can confuse customers and affect brand trust.

BrandGuard is being developed to support a more organized approach
to managing product information, claims, and brand-content reviews.

## 💡 Proposed Solution

BrandGuard provides a web dashboard connected to a Python backend.

The current prototype exposes application data related to:

- Products
- Marketing claims
- Brand rules
- Application state

The project is designed to evolve into a more complete brand-compliance
and content-review platform.

---

## ✨ Current Implementation

The following components have been implemented:

- Public-facing web dashboard
- HTML, CSS, and JavaScript frontend
- Python backend built with FastAPI
- Frontend connected to a deployed backend
- REST API endpoints that exchange JSON data
- Product, claims, and brand-rules data accessible through the API
- Backend health-check endpoint
- Public deployment of the frontend and backend

The availability of data through the API does not mean that every
dashboard action or every proposed workflow has been fully verified.

## 🧭 Planned Improvements

The following features are part of the development roadmap and
should not be considered fully implemented:

### 1. Automated Brand Compliance Checker
Identify potential product-detail errors, price mismatches, prohibited
words, and unsupported claims in submitted content.

### 2. Evidence-Linked Findings and Fix Suggestions
Connect potential issues to approved product facts or brand rules,
explain the reason for each finding, and suggest possible corrections.

### 3. Complete Review and Approval Workflow
Support submission statuses, reviewer decisions, feedback, and
audit history throughout the review process.

---

## 🏗️ Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| API Communication | REST APIs, JSON |
| Frontend Hosting | GitHub Pages |
| Backend Hosting | Render |
| Version Control | Git, GitHub |

## 🔌 Architecture

```text
                 User
                   |
                   v
       BrandGuard Web Dashboard
       HTML / CSS / JavaScript
          Hosted on GitHub Pages
                   |
                   | REST API / JSON
                   v
          Python FastAPI Backend
             Hosted on Render
                   |
                   v
             Application Data
       Products / Claims / Brand Rules
             / Application State
```

This diagram describes the current high-level architecture.
It does not imply that an unimplemented database or AI service exists.

---

## ⚙️ Run the Backend Locally

### Prerequisites

- Python installed
- Git installed
- A terminal or command prompt

### 1. Clone the repository

```bash
git clone https://github.com/agrawaltarun057-pixel/BrandGuard.git
cd BrandGuard
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the FastAPI server

```bash
uvicorn main:app --reload
```

The local backend should be available at:

http://127.0.0.1:8000

FastAPI's interactive API documentation is normally available at:

http://127.0.0.1:8000/docs

These local instructions assume the dependencies install successfully
and the application starts with the current project configuration.

### Run the Frontend

Open the deployed frontend:

https://agrawaltarun057-pixel.github.io/BrandGuard/

If running the frontend locally, make sure its API configuration points
to the backend you intend to use. The public frontend may be configured
to communicate with the deployed backend rather than localhost.

---

## 🧪 Testing and Verification

The project has been opened on multiple systems, and the deployed
backend health endpoint has been checked.

For a quick backend check, open:

https://brandguard-xcmp.onrender.com/

For application data, the current backend also exposes:

https://brandguard-xcmp.onrender.com/api/state

The API response can be inspected in a browser.

This section documents the checks performed so far; it is not a claim
of comprehensive automated testing or production readiness.

---

## 🚧 Current Limitations

BrandGuard is an evolving prototype.

- Advanced AI-based compliance analysis is not fully implemented.
- Evidence-linked findings and automatic fix suggestions are planned.
- A complete review and approval workflow remains future work.
- The current project should not be treated as a production-grade
  compliance or legal verification system.

---

## 🗺️ Development Roadmap

- [x] Build the web dashboard
- [x] Develop the Python FastAPI backend
- [x] Deploy the frontend
- [x] Deploy the backend
- [x] Connect the frontend to the backend
- [x] Expose application data through API endpoints
- [ ] Implement automated brand-compliance checks
- [ ] Add evidence-linked findings and fix suggestions
- [ ] Complete the review and approval workflow

---

## 🤝 Contributions and Feedback

BrandGuard is a developing project. Feedback, ideas, and suggestions
for improving the prototype are welcome.

When reporting an issue, include a clear description of the problem
and the steps needed to reproduce it.

---

## 📄 Project Information

**Project:** BrandGuard  
**Category:** Web Development / Brand Compliance  
**Frontend:** HTML, CSS, JavaScript  
**Backend:** Python, FastAPI  
**Deployment:** GitHub Pages and Render

Built as a hackathon project, with a focus on turning a proposed
solution into a publicly accessible working prototype.
