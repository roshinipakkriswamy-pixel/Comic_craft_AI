# ComicCraft – AI Comic Story Creator

ComicCraft is a Generative AI web application that creates personalized five-panel comic stories from a user's idea.

The application uses **FastAPI** for the backend, **Google Gemini** models for story generation, and **Stable Diffusion / placeholder image generation** for comic illustrations.

---

## Features

- Create a personalized 5-panel comic
- Enter a custom story idea
- Choose a character name
- Choose a story setting
- Select the story tone
- Select an art style
- Generate a comic outline using Gemini
- Generate narration and dialogue using Gemini
- Generate comic panel images
- Preview the complete comic in the browser
- Export the comic as a PDF
- Download the generated PDF
- JSON API endpoint for comic generation
- FastAPI Swagger documentation
- Demo mode without an API key
- Automated tests using Pytest

---

## Project Architecture

```text
User
 │
 ▼
Web Interface
 │
 ▼
FastAPI Backend
 │
 ├── Gemini Flash
 │      └── Generates 5-panel comic outline
 │
 ├── Gemini Pro
 │      └── Generates narration and dialogue
 │
 ├── Image Generator
 │      ├── Stable Diffusion
 │      └── Placeholder images
 │
 ├── Comic Layout Builder
 │      └── Combines story + images
 │
 └── PDF Exporter
        └── Creates downloadable PDF