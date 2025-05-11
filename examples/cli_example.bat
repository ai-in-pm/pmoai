@echo off
REM Example script demonstrating PMOAI CLI usage in Windows

REM List available agents
echo Listing available agents...
pmoai list agents

REM List available tasks
echo.
echo Listing available tasks...
pmoai list tasks

REM List available crews
echo.
echo Listing available crews...
pmoai list crews

REM Initialize configuration files in a custom directory
echo.
echo Initializing configuration files in 'custom_config' directory...
mkdir custom_config 2>nul
pmoai init --output-dir custom_config

REM Modify the configuration files (example)
echo.
echo Modifying configuration files...
echo # Custom project name added >> custom_config\crews.yaml

REM Run a crew using the custom configuration
echo.
echo Running a crew using custom configuration...
echo This would execute the crew if you uncomment the following line:
REM pmoai run project_initiation_crew --config-dir custom_config --project-name "Custom Project" --output-dir output

pause
