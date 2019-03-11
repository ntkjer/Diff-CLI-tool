#/bin/bash/

source $PWD/venv/bin/activate
echo "Activated virtualenv"
echo "Testing replay"
python src/test_replay/test.py
echo "Testing helper_lib"
python src/test_helper_lib/test.py
deactivate
echo "Done"
