echo make sure you have run the "install_venv.cmd"... 

REM activate spiderEnv 
call activate spiderEnv 

REM send out spiders 
python main.py flight

call deactivate 

pause