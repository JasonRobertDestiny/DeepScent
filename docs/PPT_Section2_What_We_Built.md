# SENSORA: What We Built

## L'Oréal Brandstorm 2026 - PPT Section 2

---

## The Problem

Traditional perfumes are designed for the "average" user. But science shows the same fragrance smells completely different on different people due to individual biochemistry:

- **Skin pH** varies from 4.5 to 6.5 - affects molecular stability and scent evolution
- **Skin Type** (dry/normal/oily) - determines how long fragrance lasts
- **Body Temperature** - controls how fast molecules evaporate

**The result?** Consumers spend billions on perfumes that don't perform as expected on their unique skin.

---

## Our Solution: SENSORA

**Sensora** is an AI-powered fragrance personalization platform that creates bespoke perfume formulations by analyzing your unique biology and emotional state.

### Core Innovation: Physio-RAG Technology

**Physio-RAG (Physiological Retrieval-Augmented Generation)** is our proprietary AI engine that:

1. Retrieves scientific rules from a biochemistry knowledge base
2. Automatically adjusts fragrance formulations for each individual
3. Ensures every perfume is optimized for YOUR body chemistry

---

## How It Works: 4-Step User Journey

### Step 1: Bio-Calibration
Users input their physiological profile through an intuitive interface:
- Skin pH level (slider from acidic to alkaline)
- Skin type selection (dry / normal / oily)
- Body temperature

### Step 2: Neuro-Brief
Users describe their desired emotional experience in natural language:

> *"A peaceful morning in a Japanese garden after rain"*
>
> *"Confident and powerful for an important meeting"*
>
> *"Cozy weekend reading by the fireplace"*

Our AI translates these descriptions into **Valence-Arousal coordinates** using the psychological Circumplex Model of Affect.

### Step 3: AI Formulation (The Magic)
The **Sensora Engine** orchestrates multiple AI systems:

1. **Emotion Analysis** - GPT-4o maps feelings to scent families
2. **Physio-RAG Retrieval** - 12 scientific rules correct for body chemistry
3. **Ingredient Selection** - Sustainable database with 100+ materials
4. **Safety Validation** - IFRA 51st Amendment compliance check
5. **Molecular Optimization** - LogP and volatility calculations

**Output:** A complete, personalized perfume formula with:
- Unique name and description
- Full ingredient list with concentrations
- Note pyramid (top/heart/base distribution)
- Performance metrics (longevity, projection, sustainability)
- Physio-corrections applied

### Step 4: Purchase & Delivery
- Export digital formula (JSON format)
- Order custom 30ml Eau de Parfum ($149 USD)
- Secure PayPal checkout
- Ships worldwide in 5-7 business days

---

## The Science Behind Physio-RAG

### Real Examples of Our Correction Rules:

| Your Biology | The Problem | Sensora's Solution |
|--------------|-------------|-------------------|
| **Acidic skin (pH < 4.5)** | Aldehydes become unstable, create off-notes | Reduce aldehydes 15%, substitute with stable acetals |
| **Dry skin** | Fragrance evaporates too fast, poor longevity | Boost high-LogP fixatives by 25% to create artificial lipid matrix |
| **Oily skin** | Top notes get "swallowed", poor projection | Increase volatile top notes 15% for better sillage |
| **Warm body (>37°C)** | Top notes "burn off" instantly | Reduce volatile molecules, use higher molecular weight alternatives |
| **Alkaline skin (pH > 6.0)** | Floral notes become flat | Increase floral concentration 20%, add acidic buffer |

### Scientific Foundation:
- **Raoult's Law** - Predicting fragrance-skin lipid interactions
- **Antoine Equation** - Temperature-dependent evaporation modeling
- **Schiff Base Chemistry** - pH effects on aldehyde stability
- **IFRA Guidelines** - International safety standards compliance

---

## Key Technical Features

| Feature | What It Does |
|---------|--------------|
| **Physio-RAG Engine** | 12 peer-reviewed scientific rules for personalization |
| **GPT-4o Integration** | Natural language to fragrance translation |
| **IFRA Compliance** | Real-time safety validation, allergen detection |
| **Sustainability Filter** | Prioritizes upcycled & bio-based ingredients |
| **Note Pyramid AI** | Optimizes top/heart/base ratio for balanced longevity |
| **Molecular Calculator** | LogP and molecular weight analysis using chemistry models |

---

## Example Output

**User Input:**
- pH: 5.5 (slightly acidic)
- Skin Type: Normal
- Temperature: 36.5°C
- Prompt: *"Fresh morning breeze, optimistic and calm"*

**Sensora Output:**

> ### Morning Zephyr
> *Experience the serene embrace of a fresh morning breeze, infused with the invigorating zest of citrus and the calming whispers of nature.*
>
> **Top Notes:** Bergamot, Lemon, Green Tea
> **Heart Notes:** Jasmine, Lily of the Valley, Cucumber
> **Base Notes:** White Musk, Cedarwood
>
> **Performance:** Longevity 72% | Projection 64% | Sustainability 75%
>
> **Physio-Corrections Applied:**
> - Balanced citrus notes for skin pH 5.5
> - Optimized volatility for 36.5°C body temperature
> - Standard longevity profile for normal skin type

---

## Alignment with L'Oréal Strategy

| L'Oréal Brandstorm Criteria | How Sensora Delivers |
|-----------------------------|---------------------||
| **Innovation** | World's first Physio-RAG fragrance personalization platform |
| **Tech & Science** | AI + biochemistry + molecular chemistry integration |
| **Sustainability** | Bio-based ingredients priority, upcycling database, carbon-conscious formulation |
| **Inclusivity** | Personalized for EVERY body chemistry - no more "one size fits all" |

### Supporting L'Oréal for the Future 2030:
- 95% bio-based ingredients in our database
- Upcycled materials flagged and prioritized
- Digital-first reduces physical sampling waste
- On-demand production minimizes overstock

---

## Live Product Demo

**Production URL:** https://deepscent.vercel.app

**Backend API:** https://deep-scent.vercel.app

Fully functional end-to-end experience:
1. Visit the website
2. Complete Bio-Calibration
3. Write your Neuro-Brief
4. Receive personalized AI-generated formula
5. Purchase via PayPal

---

## Key Messages for Slides

### Headline:
> **"Sensora: Fragrance That Feels You"**

### Tagline:
> **"Your Skin. Your Scent. Your Science."**

### The Hook:
> **"Why does the same perfume smell amazing on your friend but wrong on you? The answer is biochemistry. Sensora is the solution."**

### The Differentiator:
> **"Traditional perfumes are designed for average skin. Sensora designs for YOUR skin."**

---

## Suggested Slide Structure

**Slide 2A: The Problem**

- Same perfume, different results (visual: two people, same bottle, different reactions)
- Science explanation: pH, skin type, temperature

**Slide 2B: Our Solution**
- Sensora logo and tagline
- Physio-RAG technology explanation
- 4-step user journey icons

**Slide 2C: The Technology**
- How Physio-RAG works (diagram)
- Example correction rules
- AI integration stack

**Slide 2D: Live Demo / Screenshots**
- Website screenshots
- Example formula output
- User testimonial or demo video QR code

---

## Technical Specifications (If Needed)

- **Frontend:** Next.js 14, React, Tailwind CSS, Framer Motion
- **Backend:** FastAPI (Python), deployed on Vercel Serverless
- **AI Engine:** OpenAI GPT-4o for emotion analysis
- **Database:** ChromaDB for vector similarity search
- **Payment:** PayPal SDK integration
- **Compliance:** IFRA 51st Amendment rule engine

---

*Document prepared for L'Oréal Brandstorm 2026 Competition*
*Project: Sensora - AI-Driven Adaptive Perfume Formulation Platform*
