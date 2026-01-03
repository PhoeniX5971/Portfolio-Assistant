# Synaptic

A modular framework for building, managing, and running AI models and tools with provider abstraction and autonomous orchestration systems.

## Overview

Synaptic is a lightweight and extensible AI framework designed to simplify model orchestration, tool integration, and memory management.

It abstracts away the differences between AI providers and enables dynamic automation for agent systems and intelligent pipelines. Built for developers who need architectural flexibility, Synaptic allows you to register tools, integrate models, manage context, and enable autonomous execution across multiple providers.

## Core Capabilities

### Provider Abstraction Layer

- **Unified Interface**: Write logic once and switch between providers with minimal modification.
- **Interchangeable Backends**: Supports OpenAI, Gemini, and DeepSeek via a shared abstraction layer.
- **Lifecycle Handling**: Standardized logic for model initialization, execution, and cleanup.

### Autonomous Systems

- **Auto Tool Runner**: Automatically triggers tool execution based on model intent and real-time context.
- **Auto Memory Manager**: Handles dynamic session-based and persistent memory for ongoing interactions.
- **Safety Controls**: Includes a **Blacklist Manager** to restrict specific tools from auto-execution based on security policy.

### Global Tool Registry

- **Centralized Metadata**: A single registry storing metadata and references for all loaded tools.
- **Seamless Interoperability**: Enables controlled global access and communication across different models and runtime contexts.

## Features

- **Standardized Tooling**: Uses an **Auto Tool Wrapper** to ensure external tools follow consistent runtime behavior.
- **Extensible Memory**: Core utilities designed for easy state management and persistence.
- **Clean Architecture**: Modular directory structure separating core logic, providers, and local tools.

## Technical Details

- **Languages & Tools**: Python, Modular Architecture, Provider Adapters.
- **Providers**: OpenAI (\`synaptic.providers.openai\_\`), Gemini (\`synaptic.providers.gemini\`), DeepSeek (\`synaptic.providers.deepseek_adapter\`).
- **Project Structure**:
  - \`core/\`: Base classes for models, providers, and tools.
  - \`providers/\`: Implementation-specific logic for different LLM vendors.
  - \`memory/\`: Persistence and session management utilities.

## Installation

\`\`\`bash

# Clone the repository

git clone https://github.com/PhoeniX5971/synaptic.git
cd synaptic

# Install dependencies

pip install -e .
\`\`\`

**Documentation:** Full technical details are available in the [Project Wiki](https://synaptic-wiki.vercel.app/docs/intro).

Deliverable Skills: AI Framework, Orchestration, LLM Ops, Automation, Multi-Provider, Agentic AI, Python

runnable: false
