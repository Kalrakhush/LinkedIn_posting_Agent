# LinkedIn Posting Agent

This project uses CrewAI to generate and post LinkedIn content based on user inputs. A web UI built with Flask provides a beautiful, animated interface where you can enter:
- Topic
- Tone
- Audience
- Details
- Hashtags

One agent processes these inputs into a polished post, and a second agent logs into LinkedIn (using your personal credentials) and submits the post via the unofficial linkedin‑api.

## Setup

1. Install dependencies:
   ```bash
   pip install poetry
   poetry install
