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

If all answers are yes:

Record it here.

Otherwise:

It is either a bug or a roadmap item.
