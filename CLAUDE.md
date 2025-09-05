# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Creative Future Portrait is an AI-powered application that generates creative future portraits of children based on their current photos and dream descriptions. This is **not a prediction tool** but a creative, AI-generated visualization for entertainment and family engagement.

## Development Commands

### Package Management
- Install dependencies: `uv sync`
- Add new dependency: `uv add <package>`
- Remove dependency: `uv remove <package>`

### Running the Application
- Run main script: `uv run python main.py`
- Start development server (when Streamlit is implemented): `uv run streamlit run app.py`

## Architecture

### Current State
- **Language**: Python 3.12+
- **Package Manager**: uv (modern Python package manager)
- **Current Implementation**: Basic placeholder in `main.py`

### Planned Architecture (from requirements.md)
- **Frontend**: Streamlit web application
- **Backend Options**: 
  - OpenAI Images API (for ease of use)
  - Local Diffusers with Stable Diffusion (for flexibility)
- **Image Processing**: PIL for EXIF removal, resizing, watermarking
- **No Persistent Storage**: Images processed in-memory only, no server-side storage

### Key Features to Implement
1. Image upload with EXIF removal and orientation correction
2. Dream text input processing (converted to AI prompts)
3. Age progression (5-40 years, default +20)
4. Style selection (soft realistic, realistic, illustration)
5. Watermarking with "creative/not prediction" messaging
6. PNG metadata embedding for provenance
7. Content safety controls (negative prompts, NSFW filtering)

## Configuration
- Environment variables stored in `.env` file:
  - `OPENAI_API_KEY`: Required for OpenAI backend
  - `BACKEND`: Choose "openai" or "diffusers"
  - `DIFFUSERS_MODEL`: Specify local model (e.g., "stabilityai/sdxl-turbo")

## Privacy & Safety Design Principles
- **Data Minimization**: No server-side image storage by default
- **EXIF Removal**: Automatic removal of metadata from uploaded images
- **Creative Labeling**: Clear messaging that output is creative, not predictive
- **Content Safety**: Built-in filtering for inappropriate content
- **Age Appropriateness**: Designed specifically for children's portraits

## File Structure
- `main.py`: Current entry point (placeholder)
- `pyproject.toml`: Project configuration with uv
- `requirements.md`: Detailed Japanese specification document
- `uv.lock`: Dependency lock file

## Important Notes
- This project is intended for **creative/entertainment purposes only**
- All generated images should include watermarks indicating they are "creative, not predictions"
- Compliance with privacy laws (APPI/GDPR/COPPA) is required for commercial use
- Content safety is a core requirement - no NSFW, violence, or inappropriate content