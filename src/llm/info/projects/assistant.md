# Assistant – Phoenix Portfolio AI Agent

**Description:**  
The Assistant is an interactive AI agent integrated into PhoeniX5971's portfolio. It runs in a terminal-like environment, demonstrating both technical skill and user engagement. Visitors can query it for information about projects, skills, and contact details, while it guides them through the portfolio using terminal commands and GUI cues. It is the only project in the portfolio that is fully **runnable**, allowing for live interaction.

**Key Features:**

- **Interactive Terminal Experience:** Navigate the portfolio with commands like `ls`, `cd`, `cat`, `tree`, `pwd`, `help`, and `clear`.
- **Runnable Project:** Launch the Assistant directly with `run assistant` and interact with the AI in real-time.
- **File System Awareness:** Operates within a safe, simulated Linux-like environment, with access limited to allowed files:
  - `cv/about.md`, `cv/contact.md`, `cv/resume.md`
  - `projects/attack-copilot.md`, `projects/synaptic.md`, `projects/assistant.md`
  - `skills.md`, `technologies.md`
- **Contextual Responses:** Provides concise answers, then suggests terminal commands to view source files.
- **Guided Exploration:** Offers hybrid support—users can type commands or click files in the sidebar file browser.
- **Structured Logging:** Tracks internal AI reasoning via logs categorized as `info`, `success`, `warning`, and `error`.
- **Rerun Handling:** Supports multi-step reasoning and reruns when additional context or file access is needed.

**Behavioral Highlights:**

- Keeps responses concise, suitable for a terminal interface.
- Suggests navigation commands to explore content (`cat cv/about.md`).
- Refuses any hostile, illegal, or configuration-exposing requests.
- Ensures safe access by only reading from allowed files in the knowledge base.

**Technology Stack:**

- **Backend:** Python, FastAPI
- **Frontend Integration:** Next.js (Portfolio Terminal)
- **AI Logic:** Custom agent orchestrated via `Session` modules
- **Security:** Environment-based secrets, file access guardrails, and rerun prompt controls

**Notes:**

- Designed as the runnable AI assistant in the portfolio.
- Demonstrates a real-time, secure, and guided AI interface.
- Serves as both a portfolio showcase and an example of LLM-based agent orchestration.
