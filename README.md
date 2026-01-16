# Aether - AI-Driven Adaptive Perfume Platform

> L'Oréal Brandstorm 2026 Competition Project

Aether is a neurophysiology-powered fragrance personalization platform that creates bespoke perfume formulations based on real-time emotional states and individual body chemistry.

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Bio-Sensors   │────▶│   Physio-RAG    │────▶│   AI Formula    │
│  (EEG/HRV/GSR)  │     │    Correction   │     │    Generator    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                      │                       │
         ▼                      ▼                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Valence-Arousal │     │   Skin pH/Temp  │     │  IFRA Compliant │
│    Mapping      │     │   Adjustments   │     │   Formulation   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## Tech Stack

**Frontend**
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Zustand (State Management)

**Backend**
- FastAPI (Python 3.11+)
- RDKit (Molecular Calculations)
- ChromaDB (Vector Store for RAG)

## Quick Start

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Project Structure

```
DeepScent/
├── frontend/           # Next.js application
│   ├── src/
│   │   ├── app/       # App router pages
│   │   ├── components/# React components
│   │   ├── stores/    # Zustand stores
│   │   └── lib/       # Utilities
│   └── public/        # Static assets
│
├── backend/           # FastAPI application
│   ├── app/
│   │   ├── core/      # Core engine
│   │   ├── chemistry/ # Molecular calculations
│   │   ├── neuro/     # Valence-arousal mapping
│   │   └── main.py    # Entry point
│   └── data/          # Ingredient database
│
└── docs/              # Documentation
```

## Key Features

- **Neuro-Brief**: Natural language emotional input mapped to scent families
- **Bio-Calibration**: Skin pH, temperature, and type adjustments
- **Physio-RAG**: Retrieval-augmented generation for personalized corrections
- **IFRA Compliance**: Automated safety validation for all formulations
- **Sustainability Scoring**: Green chemistry metrics

## Team

DeepScent Team - L'Oréal Brandstorm 2026

## License

MIT
