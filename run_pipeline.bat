@echo off
setlocal

REM Get the input C file path from the first argument
set INPUT_FILE=%1

REM Set the output directory and file path
set OUTPUT_DIR=promela_code
set OUTPUT_FILE=%OUTPUT_DIR%\promela.pml

REM Ensure output directory exists
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

echo ====================================
echo Running query_description_generator.py...
echo Input: %INPUT_FILE%
python "scripts\query_description_generator.py" --input "%INPUT_FILE%"
IF %ERRORLEVEL% NEQ 0 EXIT /B %ERRORLEVEL%

echo ====================================
echo Running promela_queries.py...
python "scripts\promela_queries.py"
IF %ERRORLEVEL% NEQ 0 EXIT /B %ERRORLEVEL%

echo ====================================
echo Running generate_promela.py...
echo Input: %INPUT_FILE%
echo Output will be saved to: %OUTPUT_FILE%
python "scripts\generate_promela.py" --input "%INPUT_FILE%"
IF %ERRORLEVEL% NEQ 0 EXIT /B %ERRORLEVEL%

echo ====================================
echo All scripts executed successfully.
endlocal