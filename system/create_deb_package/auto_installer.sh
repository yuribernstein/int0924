#!/bin/bash
git clone https://github.com/yuribernstein/int0924.git
cd int0924/system/create_deb_package
dpkg-deb --build systeminfo_deb_package
mv systeminfo_deb_package.deb systeminfo.deb
echo "systeminfo.deb package is ready."
sudo apt -y install ./systeminfo.deb