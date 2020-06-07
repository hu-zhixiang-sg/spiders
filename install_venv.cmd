echo you have to first set anaconda path to the system environment variable list... 

REM remove existing venv named spiderEnv 
call conda env remove --name newEnv -y 

REM create venv spiderEnv 
call conda create -y --name newEnv python=3.6 

REM enter venv 
call activate newEnv 

REM install requirements 
python -m pip install -r requirements.txt 

echo "Spider virtual environment is ready." 

deactivate 

pause 