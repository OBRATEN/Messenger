# Messenger

It is simple SSH messenger on python.
Works by Linux SSH commands (ssh, ssh-copy-id, ssh-keygen, scp)
Tested on Arch Linux, openssh service.

To install openssh write:
```bash
sudo pacman -S openssh
sudo systemctl enable sshd
sudo systemctl enable sshd.service
reboot
```
To install needed packages:
```bash
sudo pacman -S python-pip
cd Messenger/
```
By pip3:
```bash
pip3 install -r requirements.txt
```
By shell-script:
```bash
./install.sh
```
Here is two types of program:
1. Qt-based
2. CLI-based
To start CLI-based:
```bash
python3 src/cli.py
```
To start Qt-based:
```bash
./start.sh
```
[!Screenshot](/home/arthur/git0.png)
