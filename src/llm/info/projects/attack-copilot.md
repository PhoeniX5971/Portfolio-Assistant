# Attack Copilot

Cybersecurity meets Generative AI: a multi-agent system specializing in Microsoft Active Directory.

## Overview

Attack Copilot is an intelligent LLM-driven tool designed for **purple team workflows**, combining offensive and defensive insights. It analyzes AD objects, privileges, ACLs, trusts, SPNs, and relationships to uncover viable attack paths, then provides actionable recommendations for both red and blue teams.

## Core Capabilities

### Red Team — Attack Path Generation

- Enumerates users, groups, machines, GPOs, ACLs, trusts, and delegation paths
- Identifies privilege escalation and lateral movement opportunities
- Generates step-by-step attack chains with recommended tools and commands
- Suggests lab-friendly execution order

### Blue Team — Defense & Mitigation

- Explains root causes behind potential attacks
- Provides hardening guidance for AD objects, ACLs, and configurations
- Recommends detection strategies and SOC-ready monitoring rules
- Validation procedures for ensuring mitigations worked

### Multi-Agent Architecture

- Modular agentic model with shared context and structured messaging
- Built on the **Synaptic framework** for orchestration
- Enables coordinated reasoning and tool-assisted operations

## Features

- **Discovery & Enumeration**: Users, groups, machines, GPOs, SPNs, ACLs
- **Attack Path Construction**: Graph-based pathfinding, privilege escalation chains, multi-step attack narratives
- **Mitigation & Defense**: Immediate fixes, long-term hardening strategies, validation checks
- **Reporting**: Combined Red/Blue output, per-path breakdown, Markdown-friendly export, tool recommendations

## Technical Details

- **Languages & Tools**: Python, Synaptic framework, Discord.py, PowerShell modules
- **AI & Memory**: LLM orchestration, RAG-based memory, multi-agent reasoning
- **Deployment**: Docker containers for modular, portable agents

## Roadmap

- Future lightweight C2 layer for end-to-end simulation
- Interactive execution in lab environments
- Automated collection, analysis, and validation of attack simulations

**Note:** Not open-sourced yet. Contains proprietary components under evaluation for potential commercial release. Proof-of-concept video demonstration will be available soon.

Deliverable Skills: Cybersecurity, Generative AI, Active Directory, Purple Teaming, Multi-Agent AI, Multi-Step Reasoning

runnable: false
