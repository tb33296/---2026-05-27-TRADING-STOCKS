# Folder Tree

```text
!! 2026-05-27 TRADING STOCKS (38 folders, 144 files)/
├── analytics (0 folders, 1 files)/
│   └── __init__.py (0 lines)
├── broker (1 folders, 0 files)/
│   └── websocket (0 folders, 0 files)/
├── config (0 folders, 2 files)/
│   ├── __init__.py (0 lines)
│   └── config.py (205 lines)
├── core (14 folders, 51 files)/
│   ├── auth (0 folders, 2 files)/
│   │   ├── __init__.py (0 lines)
│   │   └── auth_manager.py (290 lines)
│   ├── execution (0 folders, 7 files)/
│   │   ├── charges_engine.py (107 lines)
│   │   ├── execution_result.py (29 lines)
│   │   ├── order.py (89 lines)
│   │   ├── paper_broker.py (366 lines)
│   │   ├── paper_execution_engine.py (150 lines)
│   │   ├── position.py (203 lines)
│   │   └── tradebook.py (355 lines)
│   ├── indicators (0 folders, 10 files)/
│   │   ├── atr.py (160 lines)
│   │   ├── awvap.py (148 lines)
│   │   ├── cvd.py (188 lines)
│   │   ├── indicator_base.py (112 lines)
│   │   ├── indicator_manager.py (242 lines)
│   │   ├── liquidity_delta.py (198 lines)
│   │   ├── moving_average.py (237 lines)
│   │   ├── rvol.py (120 lines)
│   │   ├── vwap.py (203 lines)
│   │   └── vwma.py (172 lines)
│   ├── instruments (0 folders, 4 files)/
│   │   ├── instrument_manager.py (378 lines)
│   │   ├── instrument_updater.py (181 lines)
│   │   ├── symbol_registry.py (440 lines)
│   │   └── token_resolver.py (242 lines)
│   ├── market_data (0 folders, 4 files)/
│   │   ├── candle.py (123 lines)
│   │   ├── candle_builder.py (341 lines)
│   │   ├── market_clock.py (256 lines)
│   │   └── timeframe_manager.py (290 lines)
│   ├── positions (0 folders, 2 files)/
│   │   ├── position.py (40 lines)
│   │   └── position_manager.py (132 lines)
│   ├── risk (0 folders, 2 files)/
│   │   ├── risk_decision.py (14 lines)
│   │   └── risk_engine.py (109 lines)
│   ├── session (0 folders, 2 files)/
│   │   ├── __init__.py (0 lines)
│   │   └── session_manager.py (269 lines)
│   ├── signals (0 folders, 5 files)/
│   │   ├── crossover_signal.py (321 lines)
│   │   ├── orderflow_signal.py (211 lines)
│   │   ├── signal.py (87 lines)
│   │   ├── signal_manager.py (216 lines)
│   │   └── vwap_signal.py (233 lines)
│   ├── strategies (0 folders, 0 files)/
│   ├── strategy (0 folders, 3 files)/
│   │   ├── crossover_strategy.py (219 lines)
│   │   ├── strategy_base.py (219 lines)
│   │   └── strategy_manager.py (263 lines)
│   ├── trade_management (0 folders, 1 files)/
│   │   └── trade_manager.py (179 lines)
│   ├── watchdog (0 folders, 2 files)/
│   │   ├── __init__.py (0 lines)
│   │   └── heartbeat_monitor.py (171 lines)
│   ├── websocket (0 folders, 5 files)/
│   │   ├── __init__.py (0 lines)
│   │   ├── reconnect_manager.py (194 lines)
│   │   ├── subscription_manager.py (247 lines)
│   │   ├── tick_queue.py (134 lines)
│   │   └── websocket_manager.py (433 lines)
│   ├── __init__.py (0 lines)
│   └── logging_manager.py (64 lines)
├── data (3 folders, 4 files)/
│   ├── calendar (0 folders, 1 files)/
│   │   └── holiday.txt (16 lines)
│   ├── instruments (0 folders, 1 files)/
│   │   └── OpenAPIScripMaster.json (1736077 lines)
│   ├── watchlists (0 folders, 1 files)/
│   │   └── nifty100.txt (4 lines)
│   └── market_data.db (28 lines)
├── database (0 folders, 3 files)/
│   ├── __init__.py (0 lines)
│   ├── db_manager.py (122 lines)
│   └── schema.sql (0 lines)
├── execution (0 folders, 1 files)/
│   └── __init__.py (0 lines)
├── indicators (0 folders, 1 files)/
│   └── __init__.py (0 lines)
├── instruments (0 folders, 0 files)/
├── logs (2 folders, 4 files)/
│   ├── 2026-05-28 (0 folders, 1 files)/
│   │   └── app.log (0 lines)
│   ├── 2026-05-29 (0 folders, 1 files)/
│   │   └── app.log (8 lines)
│   ├── error.log (0 lines)
│   └── system.log (3 lines)
├── replay (0 folders, 1 files)/
│   └── __init__.py (0 lines)
├── reports (0 folders, 0 files)/
├── runtime (0 folders, 6 files)/
│   ├── __init__.py (0 lines)
│   ├── candle_runtime.py (71 lines)
│   ├── indicator_runtime.py (57 lines)
│   ├── runtime_engine.py (318 lines)
│   ├── signal_runtime.py (202 lines)
│   └── tick_processor.py (192 lines)
├── screenshots (0 folders, 0 files)/
├── strategies (0 folders, 1 files)/
│   └── __init__.py (0 lines)
├── tests (0 folders, 46 files)/
│   ├── __init__.py (0 lines)
│   ├── TEMP_GETNAMEs.py (34 lines)
│   ├── TEMP_test_auth.py (24 lines)
│   ├── test_atr.py (77 lines)
│   ├── test_atr_runtime.py (68 lines)
│   ├── test_auth_runtime.py (27 lines)
│   ├── test_awvap.py (100 lines)
│   ├── test_awvap_runtime.py (89 lines)
│   ├── test_candle_rollover.py (168 lines)
│   ├── test_config.py (9 lines)
│   ├── test_crossover_signal.py (102 lines)
│   ├── test_cvd.py (49 lines)
│   ├── test_cvd_runtime.py (67 lines)
│   ├── test_database.py (13 lines)
│   ├── test_end_to_end_runtime.py (371 lines)
│   ├── test_heartbeat_monitor.py (72 lines)
│   ├── test_indicator_runtime.py (121 lines)
│   ├── test_instrument_lookup.py (47 lines)
│   ├── test_instrument_updater.py (29 lines)
│   ├── test_liquidity_delta.py (52 lines)
│   ├── test_liquidity_delta_runtime.py (73 lines)
│   ├── test_live_candle_builder.py (66 lines)
│   ├── test_live_market_feed.py (203 lines)
│   ├── test_live_subscription_runtime.py (219 lines)
│   ├── test_logger.py (11 lines)
│   ├── test_moving_average.py (58 lines)
│   ├── test_orderflow_signal.py (134 lines)
│   ├── test_paper_execution.py (90 lines)
│   ├── test_position_exit.py (158 lines)
│   ├── test_position_manager.py (104 lines)
│   ├── test_risk_engine.py (164 lines)
│   ├── test_risk_lockout.py (117 lines)
│   ├── test_runtime_engine.py (61 lines)
│   ├── test_runtime_engine_v11.py (42 lines)
│   ├── test_rvol.py (57 lines)
│   ├── test_rvol_runtime.py (67 lines)
│   ├── test_stop_loss_exit.py (175 lines)
│   ├── test_subscription_manager_runtime.py (132 lines)
│   ├── test_symbol_registry_runtime.py (124 lines)
│   ├── test_tick_processor_runtime.py (133 lines)
│   ├── test_tick_queue.py (104 lines)
│   ├── test_timeframe_manager.py (237 lines)
│   ├── test_trade_lifecycle.py (209 lines)
│   ├── test_vwap_signal.py (103 lines)
│   ├── test_watchlist_loader.py (25 lines)
│   └── test_websocket_runtime.py (41 lines)
├── ui (0 folders, 1 files)/
│   └── __init__.py (0 lines)
├── utils (0 folders, 5 files)/
│   ├── __init__.py (0 lines)
│   ├── helpers.py (11 lines)
│   ├── market_time.py (26 lines)
│   ├── system_monitor.py (15 lines)
│   └── watchlist_loader.py (76 lines)
├── .env (11 lines)
├── .gitignore (9 lines)
├── _CHANGELOG.md (287 lines)
├── _folderTree.md (114 lines)
├── _MASTER_ARCHITECTURE.md (879 lines)
├── _PROJECT_STATE.md (495 lines)
├── _ROADMAP.md (424 lines)
├── _TECH_DEBT.md (340 lines)
├── folderTree.md (122 lines)
├── generate_project_structure.bat (88 lines)
├── loginInfo.py (13 lines)
├── main.py (12 lines)
├── PROMPT_Text.txt (1262 lines)
├── pytest.ini (5 lines)
├── README.md (0 lines)
├── requirements.txt (15 lines)
└── tree.py (82 lines)
```
