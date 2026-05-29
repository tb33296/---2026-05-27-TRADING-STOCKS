# PROJECT_STATE.md

## Project Overview

Project Name:
Intraday Trading Platform

Language:
Python 3.10+

Broker:
Angel One SmartAPI

Architecture:
Event-Driven Modular Trading Platform

Status:
Active Development

Current Phase:
Execution Engine Validation Completed

Last Updated:
2026-05-29

---

# Core Design Principles

## 1. Event Driven Architecture

Data flow:

Ticks
→ Candles
→ Indicators
→ Signals
→ Strategies
→ Orders
→ Execution
→ Persistence

Every layer has a single responsibility.

---

## 2. No Runtime Constants In Modules

All runtime constants must be defined in:

config/config.py

Examples:

* market timings
* slippage
* database paths
* holiday files
* timeframes
* risk limits

Hardcoded runtime values inside implementation files are prohibited.

---

## 3. Separation Of Concerns

Indicators:
Analytics only.

Signals:
Event detection only.

Strategies:
Trading decisions only.

Execution:
Order handling only.

Persistence:
Database only.

No layer may perform responsibilities belonging to another layer.

---

# Current Architecture

## Completed Infrastructure

### Authentication

Location:

core/auth/

Completed:

* AuthManager

Status:
Working

---

### Session Management

Location:

core/session/

Completed:

* SessionManager

Status:
Working

---

### Websocket Infrastructure

Location:

core/websocket/

Completed:

* WebSocketManager
* ReconnectManager
* SubscriptionManager
* TickQueue

Status:
Working

Validated with live Angel One feed.

---

### Watchdog

Location:

core/watchdog/

Completed:

* HeartbeatMonitor

Status:
Working

---

# Instrument Layer

Location:

core/instruments/

Completed:

* InstrumentManager
* TokenResolver
* SymbolRegistry

Status:
Working

---

# Market Data Layer

Location:

core/market_data/

Completed:

* Candle
* CandleBuilder
* MarketClock
* TimeframeManager

Status:
Working

Capabilities:

* OHLC generation
* candle rollover
* timeframe management
* market session awareness
* holiday awareness

---

# Indicator Layer

Location:

core/indicators/

Completed:

* IndicatorBase
* IndicatorManager
* MovingAverage
* VWMA
* VWAP

Status:
Working

Indicators process only CLOSED candles.

---

# Signal Layer

Location:

core/signals/

Completed:

* Signal
* SignalManager
* CrossoverSignal

Pending:

* VWAPSignal

Status:
Working

---

# Strategy Layer

Location:

core/strategy/

Completed:

* StrategyBase
* StrategyManager
* CrossoverStrategy

Current Strategy:

LONG-only crossover strategy.

Behavior:

BUY
→ Enter Long

SELL
→ Exit Long

Status:
Working

---

# Execution Layer

Location:

core/execution/

Completed:

* Order
* Position
* Tradebook
* PaperBroker

Features:

* simulated fills
* slippage
* position lifecycle
* trade persistence

Status:
Working

---

# Database Layer

Location:

database/

Completed:

* DatabaseManager

Database:

SQLite

File:

data/market_data.db

Status:
Working

---

# Validation Status

## Runtime Tests

Completed:

* Authentication Runtime Test
* Websocket Runtime Test
* Heartbeat Runtime Test
* Live Feed Test

Status:
Passing

---

## End To End Validation

Completed

Validated Flow:

Ticks
→ Indicators
→ Signals
→ Strategy
→ Orders
→ PaperBroker
→ Tradebook
→ SQLite

Status:
Passing

This is the most important milestone achieved so far.

---

# Current Technical Debt

High Priority:

* Project documentation
* Runtime engine
* Database schema versioning
* Database migration system

Medium Priority:

* Folder cleanup
* Package consolidation
* Repository layer

Low Priority:

* Logging relocation
* Infrastructure package separation

---

# Known Architectural Observations

Current structure is functional but not final.

Several infrastructure components currently reside inside core.

No refactoring should be performed until architecture documentation is finalized.

---

# Immediate Next Objectives

1. Create ARCHITECTURE.md
2. Create ROADMAP.md
3. Create CHANGELOG.md
4. Define final folder structure
5. Build Runtime Engine
6. Build Risk Layer
7. Build Portfolio Layer

---

# Important Decisions Already Made

* Event driven architecture
* Config driven runtime
* SQLite persistence from early stages
* Closed candle indicator calculations
* Strategy/Signal separation
* Simulated slippage in paper broker
* Thread-safe components where applicable

---

# Recovery Instructions For New Chat

Upload:

* PROJECT_STATE.md
* ARCHITECTURE.md
* ROADMAP.md

Then start with:

"Continue development from current project state."

These documents are the source of truth for the project.
