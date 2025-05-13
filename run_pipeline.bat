@echo off
setlocal

echo ====================================
echo Running query_description_generator.py...
echo Input: %1
python "scripts\query_description_generator.py" "%1"
IF %ERRORLEVEL% NEQ 0 EXIT /B %ERRORLEVEL%

echo ====================================
echo Running promela_queries.py...
python "scripts\promela_queries.py"
IF %ERRORLEVEL% NEQ 0 EXIT /B %ERRORLEVEL%

echo ====================================
echo Running generate_promela.py...
echo Input: %1
python "scripts\generate_promela.py" "%1"
IF %ERRORLEVEL% NEQ 0 EXIT /B %ERRORLEVEL%

echo ====================================
echo All scripts executed successfully.
pause
endlocal
