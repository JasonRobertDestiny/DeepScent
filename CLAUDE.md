# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Aether is a neurophysiology-powered fragrance personalization platform for the L'Oreal Brandstorm 2026 competition. It creates bespoke perfume formulations based on emotional states (via EEG-derived valence-arousal) and individual body chemistry (pH, skin type, temperature).

## Development Commands

### Frontend (Next.js)
```bash
cd frontend
npm install          # Install dependencies
npm run dev          # Start development server (localhost:3000)
npm run build        # Production build
npm run lint         # ESLint check
```

### Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt           # Minimal deps (Vercel-compatible)
pip install -r requirements-full.txt      # Full deps (local development)
uvicorn app.main:app --reload             # Start dev server (localhost:8000)
pytest                                     # Run tests (requires requirements-full.txt)
```

## Architecture

### Data Flow
```
User Input -> Calibration (pH/skin) -> Neuro-Brief (text -> valence-arousal)
           -> AetherAgent -> Physio-RAG Corrections -> IFRA Validation -> Formula
```

### Frontend Structure
- `src/app/` - Next.js App Router pages: Landing(`/`), Calibration, Neuro-Brief, Result
- `src/stores/userProfileStore.ts` - Zustand state with persistence. Holds calibration data, neuro-brief, and formula across page transitions
- `src/lib/api.ts` - Backend API client wrapper

### Backend Structure
- `app/main.py` - FastAPI entry point with CORS and route registration
- `app/core/aether_agent.py` - Core orchestrator: retrieves Physio-RAG rules, generates base formula, applies corrections
- `app/core/ai_service.py` - OpenAI integration for emotion-to-scent analysis (GPT-4o)
- `app/core/physio_rag.py` - Retrieval-augmented generation for physiological corrections. Uses ChromaDB + sentence-transformers when available, falls back to keyword matching
- `app/chemistry/ifra_validator.py` - IFRA 51st Amendment compliance checker
- `app/chemistry/molecular_calc.py` - RDKit-based LogP and molecular weight calculations
- `app/neuro/eeg_simulator.py` - Text-to-valence-arousal conversion for demos (no real EEG hardware needed)
- `app/neuro/ph_analyzer.py` - pH strip image analysis (color matching)
- `app/api/routes/` - REST endpoints: calibration, formulation, payment

### Key Design Decisions
- Heavy dependencies (RDKit, sentence-transformers, ChromaDB) have graceful fallbacks for Vercel serverless deployment
- OpenAI is the primary AI engine; local AetherAgent is the fallback when API key unavailable
- Formula generation always runs IFRA validation before returning to ensure regulatory compliance

## API Endpoints

Base URL: `/api`
- `POST /formulation/generate` - Main formula generation endpoint
- `POST /formulation/validate` - IFRA compliance check
- `POST /formulation/eeg-simulate` - Text-to-valence-arousal simulation
- `GET /formulation/ph-simulate/{skin_type}` - Demo pH values by skin type
- `POST /calibration/profile` - Create user profile

## Environment Variables

### Backend (`backend/.env`)
```
OPENAI_API_KEY=sk-...
OPENAI_BASE_URL=https://api.openai.com/v1  # Or proxy URL
PAYPAL_CLIENT_ID=...
PAYPAL_CLIENT_SECRET=...
```

### Frontend (`frontend/.env.local`)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_PAYPAL_CLIENT_ID=...
```

## Deployment

- Frontend: Vercel (Next.js auto-detection)
- Backend: Vercel serverless via `backend/api/index.py` entry point
- Production URL: deepscent.vercel.app

## Domain Concepts

- **Valence-Arousal (V-A)**: Circumplex model of affect. Valence (-1 to 1) = pleasantness; Arousal (-1 to 1) = energy level
- **Physio-RAG**: Retrieval-augmented generation that queries a rule database to apply physiological corrections (e.g., boost fixatives for dry skin)
- **IFRA Compliance**: International Fragrance Association safety standards. Category 1 = fine fragrance
- **Note Pyramid**: Top (20%), Middle/Heart (35%), Base (45%) concentration ratios
- **LogP**: Octanol-water partition coefficient. Higher LogP = longer lasting on skin
