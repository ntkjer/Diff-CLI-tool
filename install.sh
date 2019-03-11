#/bin/bash/

python -m virtualenv venv 
echo "created a Python 2.7 virtual environment called venv in $PWD"
source $PWD/venv/bin/activate
echo "activated virtualenv"
cd $PWD/src/
pip install --editable .
deactivate
echo "successfully installed replay"

echo "downloading data from s3 to /tmp/ehub_data/"
mkdir /tmp/ehub_data
cd /tmp/ehub_data
aws s3 cp s3://net.energyhub.assets/public/dev-exercises/audit-data.tar.gz .
tar xvzf audit-data.tar.gz
echo "done!"

