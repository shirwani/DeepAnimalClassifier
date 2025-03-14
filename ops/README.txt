###################################################################
# PREREQ ON ALL SYSTEMS
#   Install python 3.12 if it's not already installed on the server
#   Make sure python3 is aliased to python 3.12
###################################################################

#####################################################
# SETTING UP THE LOCAL DEV MACHINE TO RUN THE SCRIPTS
#####################################################
    cd DeepAnimalClassifier
    mkdir -p ./models
    which python3 # -> shoud point to python 3.12 on the system
    python3 -m venv venv
    alias python="venv/bin/python3.12"
    alias pip="venv/bin/pip3.12"
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt

######################################################
# COPYING TRAINING FILES FROM LOCAL -> TRAINING SERVER
######################################################
    ssh root@97-107-130-190.ip.linodeusercontent.com 'mkdir -p /root/DeepAnimalClassifier/datasets'
    ssh root@97-107-130-190.ip.linodeusercontent.com 'mkdir -p /root/DeepAnimalClassifier/models'
    scp ./train.py           root@97-107-130-190.ip.linodeusercontent.com:/root/DeepAnimalClassifier/.
    scp ./cv.py              root@97-107-130-190.ip.linodeusercontent.com:/root/DeepAnimalClassifier/.
    scp ./utils.py           root@97-107-130-190.ip.linodeusercontent.com:/root/DeepAnimalClassifier/.
    scp ./requirements.txt   root@97-107-130-190.ip.linodeusercontent.com:/root/DeepAnimalClassifier/.
    scp ./datasets/train.h5  root@97-107-130-190.ip.linodeusercontent.com:/root/DeepAnimalClassifier/datasets/.
    scp ./datasets/cv.h5     root@97-107-130-190.ip.linodeusercontent.com:/root/DeepAnimalClassifier/datasets/.
    scp ./datasets/test.h5   root@97-107-130-190.ip.linodeusercontent.com:/root/DeepAnimalClassifier/datasets/.
    scp ./ops/start_training root@97-107-130-190.ip.linodeusercontent.com:/root/DeepAnimalClassifier/.
    scp ./config.json        root@97-107-130-190.ip.linodeusercontent.com:/root/DeepAnimalClassifier/.

    ###############################
    # APPLICATION ENVIRONMENT SETUP
    ###############################
    cd ~/DeepAnimalClassifier
    apt update
    apt install python3.12-venv
    which python3 # -> shoud point to python 3.12 on the system
    python3 -m venv venv
    alias python="venv/bin/python3.12"
    alias pip="venv/bin/pip3.12"
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt

################################################
# COPYING FILES FROM LOCAL -> APPLICATION SERVER
################################################
    ssh root@66-228-35-9.ip.linodeusercontent.com 'mkdir -p /var/www/flask-apps/DeepAnimalClassifier/models'
    ssh root@66-228-35-9.ip.linodeusercontent.com 'mkdir -p /var/www/flask-apps/DeepAnimalClassifier/templates'
    ssh root@66-228-35-9.ip.linodeusercontent.com 'mkdir -p /var/www/flask-apps/DeepAnimalClassifier/ops'
    ssh root@66-228-35-9.ip.linodeusercontent.com 'mkdir -p /var/www/flask-apps/DeepAnimalClassifier/static/js'
    ssh root@66-228-35-9.ip.linodeusercontent.com 'mkdir -p /var/www/flask-apps/DeepAnimalClassifier/static/images/examples'
    scp ./application.py                root@66-228-35-9.ip.linodeusercontent.com:/var/www/flask-apps/DeepAnimalClassifier/.
    scp ./utils.py                      root@66-228-35-9.ip.linodeusercontent.com:/var/www/flask-apps/DeepAnimalClassifier/.
    scp ./static/js/script.js           root@66-228-35-9.ip.linodeusercontent.com:/var/www/flask-apps/DeepAnimalClassifier/static/js/.
    scp ./templates/getUserInput.html   root@66-228-35-9.ip.linodeusercontent.com:/var/www/flask-apps/DeepAnimalClassifier/templates/.
    scp ./templates/showResult.html     root@66-228-35-9.ip.linodeusercontent.com:/var/www/flask-apps/DeepAnimalClassifier/templates/.
    scp ./templates/imageError.html     root@66-228-35-9.ip.linodeusercontent.com:/var/www/flask-apps/DeepAnimalClassifier/templates/.
    scp ./static/images/*.jp*g          root@66-228-35-9.ip.linodeusercontent.com:/var/www/flask-apps/DeepAnimalClassifier/static/images/.
    scp ./static/images/examples/*.jp*g root@66-228-35-9.ip.linodeusercontent.com:/var/www/flask-apps/DeepAnimalClassifier/static/images/examples/.
    scp ./requirements.txt              root@66-228-35-9.ip.linodeusercontent.com:/var/www/flask-apps/DeepAnimalClassifier/.
    scp ./config.json                   root@66-228-35-9.ip.linodeusercontent.com:/var/www/flask-apps/DeepAnimalClassifier/.
    scp ./ops/start_app                 root@66-228-35-9.ip.linodeusercontent.com:/var/www/flask-apps/DeepAnimalClassifier/.

    ###############################
    # APPLICATION ENVIRONMENT SETUP
    ###############################
    cd /var/www/flask-apps/DeepAnimalClassifier
    apt update
    apt install python3.12-venv
    which python3 # -> shoud point to python 3.12 on the system
    python3 -m venv venv
    alias python="venv/bin/python3.12"
    alias pip="venv/bin/pip3.12"
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    pip install gunicorn

    ##########################
    # APPLICATION SERVER SETUP
    ##########################
    # Update /etc/nginx/sites-available/sites on the application server
    sudo ln -s /etc/nginx/sites-available/sites /etc/nginx/sites-enabled
    sudo service nginx restart

#######################################################
# RUNNING TRAINING & APPLICATION LOCALLY ON DEV MACHINE
#######################################################
    python train.py --dev
    python application.py --dev

    ########################################
    # TO COPY MODEL FROM THE TRAINING SERVER
    ########################################
    scp "root@172-104-24-151.ip.linodeusercontent.com:/root/DeepAnimalClassifier/models/*.pkl" ./models/.

#########################################
# RUNNING TRAINING ON THE TRAINING SERVER
#########################################
    pkill -f DeepAnimalClassifier
    nohup python train.py > /dev/null 2>&1 &

    ############################################################################
    # DEPLOYING THE TRAINED MODEL FROM THE TRAINING SERVER -> APPLICATION SERVER
    ############################################################################
    cd ~/DeepAnimalClassifier
    scp ./models/* root@66-228-35-9.ip.linodeusercontent.com:/var/www/flask-apps/DeepAnimalClassifier/models/.

###################################################
# RUNNING THE APPLICATION ON THE APPLICATION SERVER
###################################################
    cd /var/www/flask-apps/DeepAnimalClassifier
    pkill -f DeepAnimalClassifier

    #################################
    # To use model from ./config.json
    #################################
    nohup gunicorn -b 127.0.0.1:5003 application:app > /dev/null 2>&1 &

    ##########################################
    # To use model specified from command line
    ##########################################
    # MODEL="m_20250306125531.h5" nohup gunicorn -b 127.0.0.1:5003 application:app > /dev/null 2>&1 &

