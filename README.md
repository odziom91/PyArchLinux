# PyArchLinux
## version 0.5.3
Arch Linux Installer Script in Python 3!<br/>
### DISCLAIMER
This script is provided "as is" - without any WARRANTY!<br/>
Please use it as your own risk!<br/>
Official way to install Arch Linux is Installation Guide which is available here:<br/>
https://wiki.archlinux.org/index.php/installation_guide<br/>
<br/>
### NOTE
From <b>2020.09</b> ISO image <b>"wget"</b> command is not available after booting CD/DVD.<br/>
Please use <b>"curl"</b> command instead. More info in "How to" section.<br/>
### I. How to
1. Download Arch Linux iso from official webpage:<br/>
https://www.archlinux.org/download/<br/>
2. Burn iso into CD/DVD or create USB via software like Balena Etcher:<br/>
https://www.balena.io/etcher/<br/>
3. Boot CD/DVD or prepared USB image.<br/>
4. Check Internet connection via command:<br/>
ping -c 5 archlinux.org<br/>
5. Download PyArchLinux script by one of commands below:<br/>
curl -o PyArchLinux.py https://github.com/odziom91/PyArchLinux/raw/master/PyArchLinux.py<br/>
or:<br/>
curl -o PyArchLinux.py https://odziomek.pl/PyArchLinux.py<br/>
6. Run downloaded script via Python! Use command:<br/>
python PyArchLinux.py<br/>
7. Follow menus, commands and actions on the screen.<br/>
