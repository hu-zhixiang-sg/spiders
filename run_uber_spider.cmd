echo make sure you have run the "install_venv.cmd"... 

REM cd path/to/this/folder

REM activate spiderEnv 
call activate spiderEnv 

REM send out spiders 
python main.py uber

call deactivate 

pause