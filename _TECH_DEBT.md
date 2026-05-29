# TECH_DEBT.md

# Technical Debt Register

This document tracks known architectural compromises,
temporary implementations and future refactoring work.

Purpose:

* Prevent forgotten issues
* Document intentional shortcuts
* Track future cleanup work

Only record meaningful technical debt.

Do not record minor bugs.

---

# High Priority

## Runtime Engine Missing

Status:

Not Implemented

Impact:

System components exist but are not yet orchestrated into a continuously running trading engine.

Planned Resolution:

Build runtime/

Target Phase:

Runtime Engine

---

## Database Schema Versioning

Status:

Missing

Impact:

Schema changes currently require manual database deletion.

Planned Resolution:

Migration framework

Examples:

* schema_version table
* migration scripts

Target Phase:

Production Hardening

---

## Repository Layer Missing

Status:

Missing

Impact:

Tradebook interacts directly with DatabaseManager.

Planned Resolution:

Repository abstraction layer.

Example:

database/repositories/

Target Phase:

Production Hardening

---

# Medium Priority

## Folder Structure Drift

Status:

Known

Description:

Current implementation differs from original architecture.

Examples:

core/execution/
core/strategy/
core/indicators/

Original architecture expected:

execution/
strategies/
indicators/

Decision:

No restructuring until major development phases are complete.

Reason:

Avoid unnecessary import churn during active development.

---

## Logging Infrastructure Placement

Status:

Known

Current Location:

core/logging_manager.py

Preferred Future Location:

infrastructure/logging/

Impact:

Low

Priority:

Low

---

## Watchdog Placement

Status:

Known

Current Location:

core/watchdog/

Preferred Future Location:

infrastructure/monitoring/

Impact:

Low

Priority:

Low

---

# Low Priority

## Empty Placeholder Packages

Current Examples:

execution/
strategies/
indicators/

Contain:

**init**.py only

Decision:

Review after architecture stabilization.

Possible Actions:

* Remove
* Re-purpose
* Merge

---

## MASTER_ARCHITECTURE Drift

Status:

Partial

Description:

Actual implementation has evolved beyond the original architecture document.

Action:

Update architecture document periodically.

Priority:

Low

---

# Functional Gaps

## VWAP Signal

Status:

Not Implemented

Impact:

Low

Priority:

Low

Planned Resolution:

Implement after runtime engine completion.

---

# Testing Improvements

## Runtime Stress Testing

Status:

Not Implemented

Description:

Current validation focuses on functionality.

Missing:

* long running tests
* memory leak testing
* queue saturation testing

Priority:

Medium

---

## Recovery Testing

Status:

Not Implemented

Description:

System restart and recovery behavior not yet validated.

Priority:

Medium

---

# Refactoring Rules

Before adding an item:

Ask:

1. Is it working?
2. Is it intentionally imperfect?
3. Will we revisit it later?




One Important Observation

Your config has some duplication:

MAX_TICK_QUEUE_SIZE = 5000

appears twice.

and

WEBSOCKET_PING_INTERVAL
WEBSOCKET_RECONNECT_DELAY
MAX_WEBSOCKET_RETRIES

appear multiple times.

[COMPLETED]
InstrumentUpdater missing

[COMPLETED]
Runtime startup orchestration missing

[COMPLETED]
Watchlist → SymbolRegistry integration missing

[COMPLETED]
Subscription payload generation missing


HIGH PRIORITY

1. TickProcessor not implemented
2. Runtime loop manager not implemented
3. Candle persistence layer missing
4. Tick replay framework missing

MEDIUM PRIORITY

1. Instrument master backup/versioning
2. Subscription batching for large watchlists
3. Automatic instrument refresh scheduling

LOW PRIORITY

1. Runtime metrics dashboard
2. Memory usage monitoring
3. Tick statistics reporting