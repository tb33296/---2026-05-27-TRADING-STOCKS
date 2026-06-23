# ROADMAP.md

# Intraday Trading Platform Roadmap

## Project Status

Current Phase:

Execution Engine Validated

Current Milestone Achieved:

End-to-End Runtime Validation

Validated Flow:

Ticks
→ Candles
→ Indicators
→ Signals
→ Strategies
→ Orders
→ PaperBroker
→ Tradebook
→ SQLite

Status:

COMPLETE

---

# Development Philosophy

The platform will be built incrementally.

Rules:

1. Every phase must compile.
2. Every phase must integrate.
3. Every phase must pass tests.
4. No phase may break completed functionality.
5. Stability takes precedence over features.

---

# Phase 1 — Foundation

Status:

COMPLETE

Completed:

* Configuration system
* Logging system
* SQLite database layer
* Utility functions
* Authentication
* Session management
* Websocket infrastructure
* Tick queue
* Reconnection logic
* Heartbeat monitoring

Checkpoint:

Infrastructure Operational

---

# Phase 2 — Market Data Layer

Status:

COMPLETE

Completed:

* Instrument management
* Token resolution
* Symbol registry
* Market clock
* Candle model
* Candle builder
* Timeframe manager

Checkpoint:

Market Data Operational

---

# Phase 3 — Analytics Layer

Status:

COMPLETE

Completed:

* Indicator framework
* Moving averages
* VWAP
* VWMA

Checkpoint:

Indicator Engine Operational

---

# Phase 4 — Signal Layer

Status:

COMPLETE

Completed:

* Signal framework
* Signal manager
* Crossover signal

Pending:

* VWAP signal

Checkpoint:

Signal Engine Operational

---

# Phase 5 — Strategy Layer

Status:

COMPLETE

Completed:

* Strategy framework
* Strategy manager
* Crossover strategy

Checkpoint:

Strategy Engine Operational

---

# Phase 6 — Execution Layer

Status:

COMPLETE

Completed:

* Order model
* Position model
* Tradebook
* Paper broker

Features:

* Position lifecycle
* Simulated fills
* Slippage simulation
* Trade persistence

Checkpoint:

Execution Engine Operational

---

# Phase 7 — Runtime Engine
STATUS: COMPLETE

Completed:
✓ RuntimeEngine v1.1
✓ Automatic Startup
✓ Watchlist Registration
✓ Instrument Resolution
✓ Subscription Payload Generation
✓ Live Subscription
✓ Tick Queue Ingestion


Phase 7.1 – Market Data Processing
STATUS: NEXT

Objectives:

1. TickProcessor
2. Tick Routing
3. 1 Minute Candle Generation
4. Multi-Timeframe Aggregation
5. Candle Storage
6. Runtime Candle Validation

# Phase 8 — Risk Management

Status:

PLANNED

Goal:

Prevent catastrophic trading behavior.

Modules:

core/risk/
├── risk_manager.py
├── stop_loss_manager.py
├── position_sizer.py
└── exposure_limits.py

Features:

* Max daily loss
* Max open positions
* Position sizing
* Exposure limits
* Circuit breakers

Checkpoint:

Risk Engine Operational

---

# Phase 9 — Portfolio Management

Status:

PLANNED

Goal:

Manage account state.

Modules:

core/portfolio/
├── portfolio_manager.py
├── account.py
└── performance_tracker.py

Features:

* Capital tracking
* Equity tracking
* Drawdown tracking
* Exposure tracking

Checkpoint:

Portfolio Engine Operational

---

# Phase 10 — Analytics Engine

Status:

PLANNED

Goal:

Understand strategy performance.

Modules:

analytics/

Features:

* Win rate
* Profit factor
* Expectancy
* Drawdown
* Sharpe ratio
* Trade distribution
* Daily summaries

Checkpoint:

Analytics Operational

---

# Phase 11 — Replay Engine

Status:

PLANNED

Goal:

Replay historical sessions.

Modules:

replay/

Features:

* Historical playback
* Strategy validation
* Trade reconstruction

Checkpoint:

Replay Operational

---

# Phase 12 — Dashboard

Status:

PLANNED

Goal:

Real-time monitoring.

Modules:

ui/

Features:

* Open positions
* Live trades
* PnL
* Signals
* System health
* Charts

Checkpoint:

Dashboard Operational

---

# Phase 13 — Live Broker Abstraction

Status:

FUTURE

Goal:

Prepare migration from paper trading to live trading.

Modules:

broker/

Features:

* Broker abstraction layer
* Angel One adapter
* Future broker adapters

Checkpoint:

Broker Independent Architecture

---

# Phase 14 — Production Hardening

Status:

FUTURE

Features:

* Database migrations
* Log rotation improvements
* Recovery procedures
* Health monitoring
* Deployment automation

Checkpoint:

Production Ready Platform

---

# Deferred Until Later

The following are intentionally postponed:

* Multi-strategy framework
* Machine learning
* Multi-account support
* Distributed architecture
* Cloud clustering
* Microservices

Reason:

Premature complexity.

Current priority is a stable single-node trading platform.

---

# Current Focus

Immediate Next Task:

Build Runtime Engine

Target Outcome:

A continuously running event-driven paper trading system operating without manual intervention.



# Future Enhancement: Dynamic Depth Subscription Manager

## Problem

Angel One WebSocket V2 Depth Mode (Mode 4) is limited to approximately 50 symbols per connection.

Current implementation subscribes all active watchlist symbols to:

* Quote Mode (Mode 2)
* Depth Mode (Mode 4)

This architecture will not scale beyond the current watchlist size.

---

## Proposed Solution

Create:

runtime/depth_subscription_manager.py

Responsibilities:

* Maintain Quote subscriptions for the full watchlist.
* Dynamically allocate Depth subscriptions to the highest-priority symbols.
* Continuously rebalance Depth subscriptions during market hours.

---

## Target Architecture

NIFTY 100 Universe
↓
QUOTE Mode (2)
↓
100 Symbols

Indicator Processing
↓

Rank By:

* Strategy Score
* RVOL
* Momentum
* Volatility

  ```
    ↓
  ```

Top 20–40 Symbols
↓

DEPTH Mode (4)
↓

Liquidity Ratio
Liquidity Delta
Order Flow Analysis

---

## Benefits

* Scale to 100+ symbols without violating Angel One Depth limits.
* Reduce unnecessary market depth traffic.
* Focus Liquidity and Order Flow analysis on the most relevant candidates.
* Lower CPU and memory consumption.

---

## Alternative Approaches

### Option A — Multiple WebSocket Connections

Angel One currently allows multiple concurrent WebSocket connections.

Example:

Connection 1 → 50 Depth Symbols
Connection 2 → 50 Depth Symbols
Connection 3 → 50 Depth Symbols

Pros:

* Supports larger Depth universes.

Cons:

* Increased complexity.
* Increased network traffic.
* Increased processing load.

Status:
Not recommended at current project maturity.

---

### Option B — Dynamic Subscription Rotation

Periodically:

* Unsubscribe low-priority symbols.
* Subscribe high-priority symbols.

Pros:

* Efficient use of Depth quota.
* Better scalability.

Cons:

* Additional subscription management logic required.

Status:
Preferred long-term solution.

---

## Prerequisites

Must be completed before implementation:

* RVOL validation
* VWMA validation
* Liquidity Ratio validation
* Liquidity Delta validation
* Slippage workflow validation
* Trade quality analysis

---

## Priority

Low

Target Phase:
Post-validation optimization phase.
