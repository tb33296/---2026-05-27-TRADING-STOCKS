from pathlib import Path
from datetime import time



BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================
# Market Configuration
# ============================================

TIMEZONE = "Asia/Kolkata"

MARKET_OPEN_TIME = time(9, 15)
MARKET_CLOSE_TIME = time(15,30)

SIGNAL_START_TIME =  time(9,20) #"09:20"
NEW_ENTRY_CUTOFF_TIME = time(14,45) #"14:45"
FORCE_EXIT_TIME = time(15,25) #"15:25"

# ============================================
# Trading Configuration
# ============================================

MAX_ACTIVE_WATCHLIST = 40
MIN_ACTIVE_WATCHLIST = 20

MAX_CONCURRENT_POSITIONS = 5

# ============================================
# Risk Configuration
# ============================================

MAX_DAILY_DRAWDOWN = 3000.0
PER_TRADE_RISK = 500.0

MAX_CONSECUTIVE_LOSSES = 3

# ============================================
# Indicator Configuration
# ============================================

VWAP_WINDOW = 1
ATR_PERIOD = 14
RVOL_PERIOD = 20

# ============================================
# Database Configuration
# ============================================

DATABASE_FOLDER = BASE_DIR / "data"
DATABASE_NAME = "market_data.db"

SQLITE_DB_PATH = DATABASE_FOLDER / DATABASE_NAME

SQLITE_TIMEOUT = 30

# ============================================
# Logging Configuration
# ============================================

LOG_FOLDER = BASE_DIR / "logs"

SYSTEM_LOG_FILE = LOG_FOLDER / "system.log"
ERROR_LOG_FILE = LOG_FOLDER / "error.log"

LOG_LEVEL = "INFO"

LOG_ROTATION_SIZE = "10 MB"

# ============================================
# WebSocket Configuration
# ============================================

WEBSOCKET_RETRY_LIMIT = 20
WEBSOCKET_RETRY_DELAY = 5

HEARTBEAT_INTERVAL = 15
HEARTBEAT_TIMEOUT = 30

# ============================================
# Dashboard Configuration
# ============================================

DASHBOARD_HOST = "0.0.0.0"
DASHBOARD_PORT = 5000

DASHBOARD_REFRESH_INTERVAL = 2000

# ============================================
# System Health Configuration
# ============================================

MEMORY_WARNING_THRESHOLD = 75
CPU_WARNING_THRESHOLD = 80

SYSTEM_MONITOR_INTERVAL = 10

# ============================================
# Queue Configuration
# ============================================

MAX_TICK_QUEUE_SIZE = 5000
MAX_CANDLE_QUEUE_SIZE = 1000

# ============================================
# File Paths
# ============================================

REPORT_FOLDER = BASE_DIR / "reports"
SCREENSHOT_FOLDER = BASE_DIR / "screenshots"

# ============================================
# Authentication Configuration
# ============================================

LOGIN_RETRY_LIMIT = 5
LOGIN_RETRY_DELAY = 5

SESSION_REFRESH_INTERVAL = 1800

# ============================================
# WebSocket Configuration
# ============================================

WEBSOCKET_RECONNECT_INTERVAL = 5
WEBSOCKET_MAX_RECONNECTS = 20

TICK_QUEUE_MAX_SIZE = 5000


# Session Configuration

SESSION_TIMEOUT_MINUTES = 55

SESSION_REFRESH_BUFFER_MINUTES = 5

MAX_SESSION_REFRESH_FAILURES = 3

SESSION_HEALTH_CHECK_INTERVAL = 60

# ============================================
# Tick Queue Configuration
# ============================================

MAX_TICK_QUEUE_SIZE = 5000

TICK_PROCESSING_TIMEOUT = 1

WEBSOCKET_PING_INTERVAL = 15

WEBSOCKET_RECONNECT_DELAY = 5

MAX_WEBSOCKET_RETRIES = 20