@echo off
setlocal

echo ============================================
echo Creating Intraday Trading Platform Structure
echo ============================================

@REM set ROOT=project_root

@REM if not exist "%ROOT%" (
@REM mkdir "%ROOT%"
@REM )

@REM cd /d "%ROOT%"

echo Creating folders...

mkdir analytics
mkdir config
mkdir core
mkdir data
mkdir database
mkdir execution
mkdir indicators
mkdir logs
mkdir reports
mkdir replay
mkdir screenshots
mkdir strategies
mkdir tests
mkdir ui
mkdir utils

echo Creating **init**.py files...

type nul > analytics\__init__.py
type nul > config\__init__.py
type nul > core\__init__.py
type nul > database\__init__.py
type nul > execution\__init__.py
type nul > indicators\__init__.py
type nul > replay\__init__.py
type nul > strategies\__init__.py
type nul > tests\__init__.py
type nul > ui\__init__.py
type nul > utils\__init__.py

echo Creating starter files...

type nul > config\config.py
type nul > core\logging_manager.py
type nul > database\db_manager.py
type nul > database\schema.sql

type nul > utils\helpers.py
type nul > utils\market_time.py
type nul > utils\system_monitor.py

type nul > tests\test_config.py
type nul > tests\test_logger.py
type nul > tests\test_database.py

type nul > requirements.txt
type nul > README.md
type nul > MASTER_ARCHITECTURE.md
type nul > TECH_DEBT.md
type nul > main.py

echo Creating database placeholder...

type nul > data\market_data.db

echo Creating .env.example...

(
echo API_KEY=
echo SECRET_KEY=
echo CLIENT_ID=
echo PIN=
echo TOTP_SECRET=
echo APP_PASS=
) > .env.example

echo ============================================
echo Project structure created successfully.
echo ============================================

pause
