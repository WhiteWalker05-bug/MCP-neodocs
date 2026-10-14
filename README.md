# NeoDocs At-Home Test API & MCP Server

## Overview

NeoDocs provides an automated backend server built on FastMCP to bridge patient health scan logs with LLM-powered interfaces. Designed for seamless querying, this utility streamlines how health parameters, trend histories, and diagnostic knowledge bases are accessed and interpreted by AI agents.

> **Disclaimer:** All test kits, scans, and health knowledge files included in this repository are mock data intended exclusively for project demonstration purposes. They do not constitute professional medical advice, diagnosis, or treatment.

---

## Architecture & Core Modules

The service is organized around modular toolsets that expose discrete endpoints for data retrieval and evaluation:

* **Scan Management (`list_test_results`)**: Retrieves stored at-home test scan history, supporting optional filtering by kit category (wellness vs. uti)[cite: 2].
* **Longitudinal Trend Analysis (`get_result_trend`)**: Isolates a specific biomarker (e.g., pH, glucose, ketones, protein, leukocytes, nitrites) and maps its trajectory chronologically across prior scans[cite: 2].
* **Automated Flagging (`check_out_of_range_results`)**: Evaluates the most current scan entry against defined threshold boundaries, returning flagged out-of-range metrics and safety notices[cite: 2].
* **Knowledge Retrieval (`search_health_guidance`)**: Performs keyword-based matching against markdown-formatted medical knowledge bases to extract concise, relevant definitions[cite: 2].

---

## Tool Reference Matrix

| Identifier | Type | Input Arguments | Functional Behavior |
| :--- | :--- | :--- | :--- |
| `list_test_results` | Tool | `kit_type` (optional string) | Filters and returns user test scans by type or lists all available logs[cite: 2]. |
| `get_result_trend` | Tool | `parameter` (string) | Extracts chronological values for a single requested health marker[cite: 2]. |
| `check_out_of_range_results` | Tool | None | Scans the latest record for parameters breaching standard mock thresholds[cite: 2]. |
| `search_health_guidance` | Tool | `question` (string) | Searches internal markdown files and returns the top two relevant chunks[cite: 2]. |
| `neodocs://kits` | Resource | None | Exposes a JSON schema mapping kit categories to their respective measured metrics[cite: 2]. |
| `explain_my_latest_result` | Prompt | None | Provides a template chaining scan checks and guidance lookups for AI models[cite: 2]. |

---

## Technical Stack & Environment Management

This repository uses **uv** for high-performance Python package management, replacing traditional virtualenv and pip workflows.

* **Setup**: Run `uv sync` to automatically initialize the environment and install exact lockfile dependencies.
* **Execution**: Run `uv python server.py` or use the standard `uv run server.py` protocol to execute the server over standard input/output transport (`stdio`).

---

## Directory Layout

```text
neodocs-mcp/
├── server.py              # Main FastMCP application and tool definitions
├── scans.json             # Mock dataset containing historical test results
├── knowledge_base.md      # Reference documentation for health parameters
├── test_server.py         # Test suite for validating tool responses
├── pyproject.toml         # Project metadata and dependencies configuration
├── uv.lock                # Locked dependency resolution versions
└── README.md              # Project documentation
