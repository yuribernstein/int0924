#!/bin/bash


function check_result() {
    if [ $? -ne 0 ]; then
        echo "[ERROR] $1 failed. Exiting."
        exit 1
    fi
    echo "[SUCCESS] $1 succeeded."
}



sudo git clone https://github.com/yuribernstein/int0924.git &>/dev/null
check_result "cloning repository"

sudo apt -y update &>/dev/null && sudo apt install python3.12-venv -y &>/dev/null
check_result "installing venv"

python3 -m venv int0924/coding/flask_systeminfo/_venv_
check_result "creating virtual environment"

source int0924/coding/flask_systeminfo/_venv_/bin/activate
check_result "activating virtual environment"

pip install -r int0924/coding/flask_systeminfo/requirements.txt &>/dev/null
check_result "installing dependencies"

sudo cp -a int0924/coding/flask_systeminfo /opt
check_result "copying application to /opt/flask_systeminfo"


cat<<EOF>> /opt/flask_systeminfo/run.sh
#!/bin/bash
#
source /opt/flask_systeminfo/_venv_/bin/activate
python3 app.py
EOF

sudo chmod 755 /opt/flask_systeminfo/run.sh
check_result "creating run.sh script"   



cat<<EOF>> /etc/systemd/system/systeminfo.service
[Unit]
Description=My Custom Service
After=network.target

[Service]
WorkingDirectory=/opt/flask_systeminfo
ExecStart=/opt/flask_systeminfo/run.sh
Type=simple
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF

check_result "setting up systemd service"


sudo systemctl daemon-reload
sudo systemctl enable systeminfo.service
sudo systemctl start systeminfo.service

check_result "starting systeminfo service"

