#!/bin/bash

# Check if an application name is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <app_name>"
  exit 1
fi

APP_NAME=$1
VERSION="1.0" # Default version, adjust as needed
PACKAGE_DIR="${APP_NAME}_deb_package" # Root directory for the package

# Create the directory structure
echo "Creating directory structure for $APP_NAME package..."
mkdir -p "${PACKAGE_DIR}/DEBIAN"
mkdir -p "${PACKAGE_DIR}/usr/local/bin"     # Place for executables or scripts
mkdir -p "${PACKAGE_DIR}/etc/${APP_NAME}"   # Place for configuration files
mkdir -p "${PACKAGE_DIR}/lib/systemd/system" # Place for the systemd service file
mkdir -p "${PACKAGE_DIR}/var/log/${APP_NAME}" # Log directory

# Create a sample control file
echo "Creating control file..."
cat << EOF > "${PACKAGE_DIR}/DEBIAN/control"
Package: ${APP_NAME}
Version: ${VERSION}
Section: base
Priority: optional
Architecture: amd64
Depends: systemd
Maintainer: Your Name <your.email@example.com>
Description: ${APP_NAME} - A custom Debian package template
EOF

# Create a sample post-installation script
echo "Creating post-installation script..."
cat << EOF > "${PACKAGE_DIR}/DEBIAN/postinst"
#!/bin/bash
set -e

# Create necessary directories and set permissions
mkdir -p /var/log/${APP_NAME}
chmod 755 /var/log/${APP_NAME}

# Uncomment the line below to open a specific port if needed
# iptables -A INPUT -p tcp --dport 8080 -j ACCEPT

# Enable and start the service
systemctl enable ${APP_NAME}.service
systemctl start ${APP_NAME}.service
EOF
chmod +x "${PACKAGE_DIR}/DEBIAN/postinst"

# Create a sample pre-removal script
echo "Creating pre-removal script..."
cat << EOF > "${PACKAGE_DIR}/DEBIAN/prerm"
#!/bin/bash
set -e

# Stop and disable the service before removing the package
systemctl stop ${APP_NAME}.service
systemctl disable ${APP_NAME}.service
EOF
chmod +x "${PACKAGE_DIR}/DEBIAN/prerm"

# Create a sample systemd service file
echo "Creating systemd service file..."
cat << EOF > "${PACKAGE_DIR}/lib/systemd/system/${APP_NAME}.service"
[Unit]
Description=${APP_NAME} Service
After=network.target

[Service]
ExecStart=/usr/local/bin/${APP_NAME}_start.sh
ExecStop=/bin/kill \$MAINPID
Restart=on-failure
Type=simple
User=root
StandardOutput=journal
StandardError=journal

# Uncomment the lines below to redirect output to log files
# StandardOutput=file:/var/log/myapp/myapp.log
# StandardError=file:/var/log/myapp/myapp_error.log

[Install]
WantedBy=multi-user.target
EOF

# Create placeholder executable and configuration files
echo "Creating placeholder executable and configuration files..."
cat << EOF > "${PACKAGE_DIR}/usr/local/bin/${APP_NAME}_start.sh"
#!/bin/bash
echo "${APP_NAME} is running"
EOF
chmod +x "${PACKAGE_DIR}/usr/local/bin/${APP_NAME}_start.sh"

# Create a sample configuration file
cat << EOF > "${PACKAGE_DIR}/etc/${APP_NAME}/config.yaml"
# Configuration file for ${APP_NAME}
# Add your configurations here
EOF

# Completion message
echo "Template structure for ${APP_NAME} package is ready."
echo "To finish packaging:"
echo "1. Place your application files in the appropriate directories."
echo "2. Modify the control file, service file, and scripts as needed."
echo "3. Run 'dpkg-deb --build ${PACKAGE_DIR}' to build the .deb package."
