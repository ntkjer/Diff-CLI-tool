#/bin/bash/

python -m virtualenv venv 
echo "created a Python 2.7 virtual environment called venv in $PWD"
source $PWD/venv/bin/activate
echo "activated virtualenv"
cd $PWD/src/
pip install --editable .
deactivate
echo "successfully installed replay"
