# Architecture Report

## PROJECT_DEPENDENCY_ANALYZER

- PROJECT_DEPENDENCY_ANALYZER

## analytics

- analytics.__init__

## config

- config.__init__
- config.config
- config.risk_config_loader
- config.scoring_config_loader

## core

- core.__init__
- core.auth.__init__
- core.auth.auth_manager
- core.execution.charges_engine
- core.execution.execution_result
- core.execution.order
- core.execution.paper_broker
- core.execution.paper_execution_engine
- core.execution.position
- core.execution.tradebook
- core.indicators.atr
- core.indicators.awvap
- core.indicators.cvd
- core.indicators.indicator_base
- core.indicators.indicator_manager
- core.indicators.liquidity_delta
- core.indicators.moving_average
- core.indicators.rvol
- core.indicators.vwap
- core.indicators.vwma
- core.instruments.instrument_manager
- core.instruments.instrument_updater
- core.instruments.symbol_registry
- core.instruments.token_resolver
- core.journal.trade_feature_snapshot
- core.journal.trade_journal_manager
- core.journal.trade_metrics_snapshot
- core.journal.trade_snapshot
- core.logging_manager
- core.market_data.candle
- core.market_data.candle_builder
- core.market_data.market_clock
- core.market_data.timeframe_manager
- core.positions.position
- core.positions.position_manager
- core.risk.position_size_decision
- core.risk.position_sizing_engine
- core.risk.risk_decision
- core.risk.risk_engine
- core.session.__init__
- core.session.session_manager
- core.signals.crossover_signal
- core.signals.orderflow_signal
- core.signals.signal
- core.signals.signal_manager
- core.signals.vwap_signal
- core.strategy.crossover_strategy
- core.strategy.multifactor_decision
- core.strategy.multifactor_strategy
- core.strategy.orderflow_strategy
- core.strategy.strategy_base
- core.strategy.strategy_manager
- core.strategy.trade_context
- core.strategy.trade_decision
- core.strategy.trade_decision_engine
- core.trade_management.exit_decision
- core.trade_management.trade_manager
- core.watchdog.__init__
- core.watchdog.heartbeat_monitor
- core.websocket.__init__
- core.websocket.reconnect_manager
- core.websocket.subscription_manager
- core.websocket.tick_queue
- core.websocket.websocket_manager

## database

- database.__init__
- database.db_manager

## execution

- execution.__init__

## indicators

- indicators.__init__

## loginInfo

- loginInfo

## main

- main

## replay

- replay.__init__

## runtime

- runtime.__init__
- runtime.candle_runtime
- runtime.indicator_runtime
- runtime.runtime_engine
- runtime.signal_runtime
- runtime.tick_processor
- runtime.trade_pipeline
- runtime.trading_engine

## tests

- tests.TEMP_GETNAMEs
- tests.TEMP_test_auth
- tests.__init__
- tests.test_atr
- tests.test_atr_runtime
- tests.test_auth_runtime
- tests.test_awvap
- tests.test_awvap_runtime
- tests.test_candle_rollover
- tests.test_config
- tests.test_crossover_signal
- tests.test_cvd
- tests.test_cvd_runtime
- tests.test_database
- tests.test_end_to_end_runtime
- tests.test_end_to_end_v2
- tests.test_heartbeat_monitor
- tests.test_indicator_runtime
- tests.test_instrument_lookup
- tests.test_instrument_updater
- tests.test_liquidity_delta
- tests.test_liquidity_delta_runtime
- tests.test_live_candle_builder
- tests.test_live_market_feed
- tests.test_live_subscription_runtime
- tests.test_logger
- tests.test_moving_average
- tests.test_multifactor_strategy
- tests.test_orderflow_signal
- tests.test_orderflow_strategy
- tests.test_paper_execution
- tests.test_position_exit
- tests.test_position_manager
- tests.test_position_sizing_engine
- tests.test_position_sizing_engine_v2
- tests.test_risk_config_loader
- tests.test_risk_engine
- tests.test_risk_lockout
- tests.test_runtime_engine
- tests.test_runtime_engine_v11
- tests.test_rvol
- tests.test_rvol_runtime
- tests.test_scoring_config_loader
- tests.test_stop_loss_exit
- tests.test_subscription_manager_runtime
- tests.test_symbol_registry_runtime
- tests.test_tick_processor_runtime
- tests.test_tick_queue
- tests.test_timeframe_manager
- tests.test_trade_context
- tests.test_trade_database_schema
- tests.test_trade_decision_engine
- tests.test_trade_decision_engine_v2
- tests.test_trade_journal_data
- tests.test_trade_journal_lifecycle
- tests.test_trade_journal_manager
- tests.test_trade_lifecycle
- tests.test_trade_manager
- tests.test_trade_pipeline
- tests.test_trade_pipeline_journal
- tests.test_trading_engine
- tests.test_vwap_signal
- tests.test_watchlist_loader
- tests.test_websocket_runtime

## tree

- tree

## ui

- ui.__init__

## utils

- utils.__init__
- utils.helpers
- utils.market_time
- utils.system_monitor
- utils.watchlist_loader

