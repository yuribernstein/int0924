#!/bin/bash

echo "Cloning repository..."

sudo git clone https://github.com/yuribernstein/int0924.git

echo "Setting up Python virtual environment..."
sudo apt -y update &>/dev/null && sudo apt install python3.12-venv -y &>/dev/null

python3 -m venv int0924/coding/flask_systeminfo/_venv_
source int0924/coding/flask_systeminfo/_venv_/bin/activate
pip install -r int0924/coding/flask_systeminfo/requirements.txt &>/dev/null
sudo cp -a int0924/coding/flask_systeminfo /opt

echo "Creating run.sh and systemd service..."
cat<<EOF>> /opt/flask_systeminfo/run.sh
#!/bin/bash
#
source /opt/flask_systeminfo/_venv_/bin/activate
python3 app.py
EOF

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

chmod 755 /opt/flask_systeminfo/run.sh
sudo systemctl daemon-reload
sudo systemctl enable systeminfo.service
sudo systemctl start systeminfo.service

echo "Deployment complete. The Flask application is running as a service."