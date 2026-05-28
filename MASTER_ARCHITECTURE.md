# MASTER_ARCHITECTURE.md

## Project Name

Intraday Paper Trading Platform

## Primary Goal

A low-resource, production-grade intraday paper trading platform for Indian markets using Angel One SmartAPI.

The system is designed for:

* AWS Free Tier deployment
* Long-running stability
* Modular architecture
* Future migration to live trading

---

# Core Architectural Principles

1. Stability first
2. Risk-first engineering
3. Low RAM usage
4. Modular development
5. Centralized configuration
6. SQLite-only persistence
7. No heavy frameworks
8. Async market data ingestion
9. Candle-based persistence only
10. Plug-and-play deployment

---

# Technology Stack

## Backend

* Python 3.12+

## Web Framework

* Flask

## Database

* SQLite

## Frontend

* HTML
* CSS
* Vanilla JavaScript
* AJAX polling

## Charts

* Chart.js

## Scheduling

* APScheduler

## Networking

* asyncio
* websockets

---

# Folder Structure

project_root/
│
├── analytics/
├── config/
├── core/
├── data/
├── database/
├── execution/
├── indicators/
├── logs/
├── reports/
├── replay/
├── screenshots/
├── strategies/
├── tests/
├── ui/
├── utils/
│
├── loginInfo.py
├── main.py
├── requirements.txt
├── README.md
├── MASTER_ARCHITECTURE.md
├── TECH_DEBT.md
└── generate_project_structure.bat

---

# Module Responsibilities

## config/

Centralized configuration system.

No constants allowed elsewhere.

---

## core/

Core infrastructure:

* authentication
* websocket manager
* scheduler
* session manager
* watchdogs

---

## indicators/

All indicator calculations:

* VWAP
* AWVAP
* CVD
* ATR
* RVOL

---

## strategies/

Signal generation layer.

---

## execution/

Paper execution simulation.

---

## analytics/

Performance calculations and reports.

---

## database/

SQLite management and schema handling.

---

## ui/

Flask dashboard.

---

## utils/

Shared reusable helpers.

---

# Database Philosophy

SQLite only.

Persistence targets:

* candles
* trades
* summaries
* logs
* system health

No raw tick persistence.

---

# Event Flow

WebSocket
→ Tick Normalizer
→ Tick Queue
→ Candle Builder
→ Indicator Engine
→ Signal Engine
→ Risk Engine
→ Execution Engine
→ Position Manager
→ Database
→ Dashboard

---

# Configuration Rules

ALL configurable values MUST exist ONLY in:

config/config.py

or

.env

NO hidden constants allowed anywhere else.

---

# Memory Optimization Rules

1. No full tick storage
2. Fixed-size deque usage
3. Avoid large DataFrames
4. Use lightweight structures
5. SQLite WAL mode
6. Bounded queues only
7. Lightweight logging
8. Lazy loading where possible

---

# Logging Standards

Rotating logs:

* system.log
* error.log
* websocket.log
* trades.log

---

# Naming Conventions

## Files

snake_case.py

## Classes

PascalCase

## Functions

snake_case

## Constants

UPPER_CASE

---

# Development Methodology

Strict iterative development.

One phase at a time.

Every phase must:

* compile
* integrate
* pass tests
* remain backward compatible

---

# Checkpoint System

## Checkpoint 1

Infrastructure operational:

* config
* logging
* SQLite
* utilities

## Checkpoint 2

Connectivity operational:

* authentication
* websocket
* reconnects

## Checkpoint 3

Market data operational:

* candles
* aggregation
* session management

---

# Git Workflow

Recommended:

git init

Feature branch workflow mandatory.

Never develop directly on main.

---

# Deployment Philosophy

Target:

* Ubuntu AWS Free Tier
* 1 GB RAM
* 20 GB storage

Optimized for:

* long uptime
* low CPU
* low RAM

---

# Future Expansion

Future live trading migration:

* execution adapter abstraction
* broker abstraction layer
* risk policy layer
* multi-strategy framework

Architecture must remain stable during migration.
