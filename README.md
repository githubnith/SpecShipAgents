# SpecShip Agents

A collection of specialized AI agents built with Pydantic AI for gathering and processing requirements. The agents use a conversational interface to collect information systematically and ensure all necessary details are captured.

## Overview

This project implements two main agents:

1. **Information Gathering Agent**: A general-purpose agent that helps gather travel-related information from users, including:
   - Destination and origin
   - Travel dates
   - Hotel budget preferences

2. **Elicitor Agent**: A specialized agent for gathering business requirements, including:
   - Specific requirements and implementation details
   - Development details (new build vs enhancement)
   - Business value and success metrics
   - Test cases and impacted applications
   - Approvals and target dates

## Features

- **Conversational Interface**: Interactive CLI for natural dialogue with agents
- **Systematic Information Collection**: Step-by-step gathering of all required details
- **Validation Rules**: Ensures all necessary information is collected before proceeding
- **No Assumptions**: Agents explicitly ask for clarification rather than making assumptions
- **Structured Output**: Information is captured in well-defined Pydantic models

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/githubnith/SpecShipAgents.git
   cd SpecShip
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your API keys and configuration

## Usage

### Information Gathering Agent
```bash
python extras/info_gathering_cli.py
```

### Elicitor Agent
```bash
python extras/elicitor_cli.py
```

## Project Structure

```
SpecShip/
├── agents/
│   ├── info_gathering_agent.py   # Travel information gathering agent
│   └── elicitor_agent.py         # Business requirements elicitor agent
├── extras/
│   ├── info_gathering_cli.py     # CLI for info gathering agent
│   └── elicitor_cli.py           # CLI for elicitor agent
├── utils.py                      # Shared utilities
├── requirements.txt              # Project dependencies
└── .env                          # Environment configuration
```

## License

This project is licensed under the MIT License.