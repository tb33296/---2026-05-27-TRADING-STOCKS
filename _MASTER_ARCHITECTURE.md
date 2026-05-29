Last Updated: 2026-05-29
Architecture Version: 2.0
Runtime Version: 1.1
Current Phase: Market Data Processing Layer

# _MASTER_ARCHITECTURE.md

# Intraday Trading Platform

## Master Architecture Document

### Version 2.0

---

# Project Overview

## Project Name

Intraday Trading Platform

## Objective

Build a production-grade, event-driven intraday paper trading platform for Indian markets using Angel One SmartAPI.

The platform is designed to:

* Run on low-resource hardware
* Operate continuously throughout market hours
* Support future live-trading migration
* Provide modular development and testing
* Maintain high reliability and recoverability

---

# Design Philosophy

The platform follows five primary principles:

## 1. Stability First

System stability is more important than feature count.

## 2. Event Driven Architecture

Market events drive system behavior.

No polling-based trading logic.

## 3. Low Resource Usage

Designed for:

* AWS Free Tier
* Small VPS deployments
* Personal servers

## 4. Modular Design

Every component must be independently testable.

## 5. Broker Independence

Broker-specific code must remain isolated.

Future migration should require minimal changes.

---

# Technology Stack

## Backend

Python 3.10+

## Database

SQLite

## Market Data

Angel One SmartAPI

## Dashboard

Flask

## Frontend

* HTML
* CSS
* JavaScript
* AJAX

## Charting

Chart.js

---

# Architectural Layers

The platform is divided into the following layers.

```text
Infrastructure Layer
        ↓
Market Data Layer
        ↓
Indicator Layer
        ↓
Signal Layer
        ↓
Risk Layer
        ↓
Execution Layer
        ↓
Portfolio Layer
        ↓
Analytics Layer
        ↓
UI Layer
```

---

# Infrastructure Layer

Purpose:

Provide connectivity and runtime services.

## Components

```text
Config
Logging
Database
Authentication
Session Management
WebSocket Management
Reconnect Management
Heartbeat Monitoring
Runtime Engine
```

---

# Current Folder Structure

```text
config/
database/
core/
data/
analytics/
ui/
utils/
tests/
runtime/
```

---

# Core Infrastructure Components

## AuthManager

Responsibilities:

```text
Login
Logout
JWT Management
Feed Token Management
Profile Loading
Session Validation
```

Status:

```text
COMPLETE
```

---

## SessionManager

Responsibilities:

```text
Session Startup
Session Refresh
Session Health Validation
Session Timeout Handling
```

Status:

```text
COMPLETE
```

---

## WebSocketManager

Responsibilities:

```text
WebSocket Connection
Subscription Handling
Tick Reception
Tick Normalization
Tick Queue Delivery
```

Status:

```text
COMPLETE
```

---

## ReconnectManager

Responsibilities:

```text
Connection Recovery
Automatic Reconnect
Recovery Validation
```

Status:

```text
COMPLETE
```

---

## HeartbeatMonitor

Responsibilities:

```text
Connection Health Monitoring
Heartbeat Validation
Recovery Triggering
```

Status:

```text
COMPLETE
```

---

## TickQueue

Responsibilities:

```text
Thread-Safe Tick Buffer
Bounded Queue
Producer / Consumer Decoupling
```

Status:

```text
COMPLETE
```

---

# Instrument Layer

Purpose:

Manage all instrument and token resolution.

---

## InstrumentUpdater

Responsibilities:

```text
Download Instrument Master
Validate Instrument Master
Persist Instrument Master
```

Status:

```text
COMPLETE
```

---

## InstrumentManager

Responsibilities:

```text
Load Instrument Master
Build Indexes
Token Lookup
Symbol Lookup
Name Lookup
Exchange Lookup
```

Status:

```text
COMPLETE
```

---

## TokenResolver

Responsibilities:

```text
Name → Token
Token → Name
Exchange Filtering
Instrument Filtering
```

Status:

```text
COMPLETE
```

---

# Watchlist Layer

Purpose:

Manage active trading universe.

---

## WatchlistLoader

Responsibilities:

```text
Load Watchlist Files
Normalize Symbols
Validation
```

Status:

```text
COMPLETE
```

---

## SymbolRegistry

Responsibilities:

```text
Register Symbols
Manage Active Universe
Generate Subscription Tokens
```

Status:

```text
COMPLETE
```

---

# Subscription Layer

## SubscriptionManager

Responsibilities:

```text
Exchange Mapping
Subscription Payload Generation
SmartAPI Payload Formatting
```

Status:

```text
COMPLETE
```

---

# Runtime Engine

Purpose:

Single orchestration point for runtime startup.

---

## RuntimeEngine Startup Flow

```text
RuntimeEngine
        ↓
SessionManager
        ↓
AuthManager
        ↓
InstrumentManager
        ↓
WatchlistLoader
        ↓
SymbolRegistry
        ↓
SubscriptionManager
        ↓
WebSocketManager
        ↓
TickQueue
```

Status:

```text
COMPLETE
```

---

# Current Runtime Flow

Validated runtime flow:

```text
RuntimeEngine
        ↓
SessionManager.start_session()
        ↓
AuthManager.login()
        ↓
InstrumentManager.load_instruments()
        ↓
WatchlistLoader.load()
        ↓
SymbolRegistry.register()
        ↓
SubscriptionManager.build_payload()
        ↓
WebSocketManager.connect()
        ↓
WebSocketManager.subscribe()
        ↓
TickQueue.enqueue()
```

Status:

```text
VALIDATED
```

---

# Market Data Layer

Purpose:

Convert raw ticks into candles.

Current status:

```text
IN DEVELOPMENT
```

---

## TickProcessor

Responsibilities:

```text
Consume TickQueue
Route Market Data
Validate Tick Streams
Forward To Candle Builder
```

Status:

```text
NOT STARTED
```

---

## CandleBuilder

Responsibilities:

```text
Build 1 Minute Candles
Update Active Candles
Emit Completed Candles
```

Status:

```text
PARTIALLY COMPLETE
```

---

## TimeframeManager

Responsibilities:

```text
1m → 5m Aggregation
1m → 15m Aggregation
Future Timeframes
```

Status:

```text
PARTIALLY COMPLETE
```

---

## CandleStore

Responsibilities:

```text
Store Active Candles
Store Historical Candles
Provide Candle Access
```

Status:

```text
NOT STARTED
```

---

# Indicator Layer

Purpose:

Generate market indicators.

Planned indicators:

```text
VWAP
VWMA
Moving Average
ATR
RVOL
AWVAP
CVD
```

Status:

```text
FRAMEWORK COMPLETE
RUNTIME INTEGRATION PENDING
```

---

# Signal Layer

Purpose:

Convert indicators into trading signals.

Components:

```text
Signal
SignalManager
CrossoverSignal
VWAPSignal
```

Status:

```text
PARTIALLY COMPLETE
```

---

# Risk Layer

Purpose:

Protect trading capital.

Planned components:

```text
RiskManager
PositionSizer
DailyLossGuard
ExposureManager
```

Status:

```text
NOT STARTED
```

---

# Execution Layer

Purpose:

Execute paper trades.

Components:

```text
PaperBroker
Order
Position
TradeBook
```

Status:

```text
PARTIALLY COMPLETE
```

---

# Portfolio Layer

Purpose:

Track portfolio state.

Planned:

```text
PortfolioManager
Equity Tracking
Drawdown Tracking
PnL Tracking
```

Status:

```text
NOT STARTED
```

---

# Analytics Layer

Purpose:

Performance measurement.

Planned:

```text
Performance Analyzer
Trade Statistics
Equity Curve
Reports
```

Status:

```text
NOT STARTED
```

---

# Database Philosophy

SQLite only.

Persist:

```text
Candles
Trades
Positions
Signals
Performance
System Events
```

Do NOT persist:

```text
Raw Ticks
```

---

# Configuration Rules

All configurable values must exist in:

```text
config/config.py
```

or

```text
.env
```

No hidden constants are allowed elsewhere.

---

# Memory Management Rules

```text
No Tick Persistence
Bounded Queues
Fixed Size Buffers
Minimal DataFrames
SQLite WAL Mode
Lazy Loading
```

---

# Logging Standards

Required logs:

```text
system.log
error.log
```

Optional future logs:

```text
trades.log
risk.log
performance.log
```

---

# Git Workflow

Rules:

```text
Never develop directly on main
Feature branches mandatory
Commit after every validated milestone
```

---

# Current Project Status

## Runtime Engine v1.1

Completed and Validated:

```text
AuthManager
SessionManager
WebSocketManager
ReconnectManager
HeartbeatMonitor
TickQueue

InstrumentUpdater
InstrumentManager
TokenResolver

WatchlistLoader
SymbolRegistry

SubscriptionManager

RuntimeEngine
```

---

# Next Development Phase

## Phase 5

Market Data Processing Layer

```text
TickQueue
        ↓
TickProcessor
        ↓
CandleBuilder
        ↓
TimeframeManager
        ↓
CandleStore
```

Primary Objective:

Convert live market ticks into validated multi-timeframe candle streams.

---

# Long-Term Architecture

Final trading pipeline:

```text
WebSocket
        ↓
TickQueue
        ↓
TickProcessor
        ↓
CandleBuilder
        ↓
TimeframeManager
        ↓
Indicator Engine
        ↓
Signal Engine
        ↓
Risk Engine
        ↓
Execution Engine
        ↓
Portfolio Engine
        ↓
Analytics Engine
        ↓
Dashboard
```

This architecture shall remain the governing design document for future development.
