# Debian Package Template for Custom Applications

This template helps you create a `.deb` package for your application with a structured directory layout, systemd service integration, configuration files, and post-installation setup. Once you set up the template, you can easily add your application files, configure the package, and build it into a `.deb` package for installation on Debian-based systems.

## Prerequisites

- **Debian-based system** (e.g., Ubuntu, Debian) to create and test the `.deb` package.
- **dpkg-deb**: The Debian packaging tool (`dpkg-deb`) should be installed by default. If not, install it with:
  ```bash
  sudo apt update
  sudo apt install dpkg
  ```

## How to Use This Template

### Step 1: Run the Template Generator Script

1. Clone or download this repository.
2. Run the `prep.sh` script with your application name as an argument:
   ```bash
   chmod +x create_deb_template.sh
   ./create_deb_template.sh myapp
   ```

This will generate a directory structure for your `.deb` package in a folder named `<app_name>_deb_package` (e.g., `myapp_deb_package`).

### Step 2: Customize the Package Template

1. **Place Your Application Files**:
   - Add your application’s executables, scripts, or other files into the appropriate directories:
     - **Executables**: Place them in `usr/local/bin/`.
     - **Configuration Files**: Place them in `etc/<app_name>/` (e.g., `etc/myapp/`).

2. **Edit the Control File**:
   - The control file (`DEBIAN/control`) defines essential metadata for the package:
     ```plaintext
     Package: myapp                 # Replace 'myapp' with your app name
     Version: 1.0                   # Update the version as needed
     Section: base
     Priority: optional
     Architecture: amd64            # Change architecture if necessary
     Depends: systemd               # Add dependencies as needed
     Maintainer: Your Name <email@example.com>
     Description: MyApp - A custom Debian package template.
     ```

3. **Customize the Systemd Service**:
   - Open the systemd service file in `lib/systemd/system/<app_name>.service`:
     ```plaintext
     [Unit]
     Description=MyApp Service
     After=network.target

     [Service]
     ExecStart=/usr/local/bin/<app_name>_start.sh  # Point to your application’s main executable
     ExecStop=/bin/kill $MAINPID
     Restart=on-failure
     Type=simple
     User=root
     StandardOutput=journal
     StandardError=journal

     [Install]
     WantedBy=multi-user.target
     ```

4. **Modify Post-Install and Pre-Removal Scripts**:
   - **Post-Install Script** (`DEBIAN/postinst`): This script runs after package installation. It can set up directories, open ports, enable the systemd service, and more.
   - **Pre-Removal Script** (`DEBIAN/prerm`): This script stops and disables the systemd service before package removal.

   Update these scripts as needed for your application.

### Step 3: Build the `.deb` Package

Once everything is in place, build the `.deb` package with the following command:

```bash
dpkg-deb --build <app_name>_deb_package
```

For example:
```bash
dpkg-deb --build myapp_deb_package
```

This will create a file named `myapp_deb_package.deb` in the current directory.

### Step 4: Install and Test the Package

To install the `.deb` package:

```bash
sudo dpkg -i myapp_deb_package.deb
```

To verify the service is running:
```bash
sudo systemctl status myapp.service
```

#### Common `systemctl` Commands for Managing the Service
- **Start the Service**: `sudo systemctl start myapp.service`
- **Stop the Service**: `sudo systemctl stop myapp.service`
- **Restart the Service**: `sudo systemctl restart myapp.service`
- **Check Status**: `sudo systemctl status myapp.service`

To remove the package, which will also stop and disable the service:
```bash
sudo dpkg -r myapp
```

### Directory Structure Overview

After running the script, your package structure should look like this:

```plaintext
myapp_deb_package/
├── DEBIAN
│   ├── control            # Package metadata
│   ├── postinst           # Post-installation script
│   └── prerm              # Pre-removal script
├── etc
│   └── myapp
│       └── config.yaml    # Placeholder for configuration file
├── lib
│   └── systemd
│       └── system
│           └── myapp.service # Systemd service file template
├── usr
│   └── local
│       └── bin
│           └── myapp_start.sh # Placeholder for main executable script
└── var
    └── log
        └── myapp             # Directory for log files
```

### Customization Tips

- **Opening Ports**: The `postinst` script includes commented-out commands for opening a port using `iptables` or `ufw`. Uncomment and modify these commands as needed.
- **Logging**: Direct log output to the designated `var/log/<app_name>/` directory.
- **Dependencies**: List any dependencies required by your application in the `control` file under the `Depends` field.

### Notes

- This template is a starting point. You may need to modify it further to meet the specific requirements of your application.
- Remember to thoroughly test the `.deb` package before distributing it.

### License

GNU GENERAL PUBLIC LICENSE
