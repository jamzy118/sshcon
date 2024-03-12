# sshconn

Simple SSH connections helper in lazy python.

# install

Example, do it your way, it's just python script with few deps.

```
cd ~/.local/
git clone https://github.com/jamzy118/sshcon.git
cd sshcon
python -m venv ./venv
venv/bin/pip install -r requirements.txt
```

then customize sshcon.sh script when copying it over to your $PATH

# Configuration

Nothing to configure really, but if you want connections JSON it's in ~/.config/sshcon.json

# usage

```
sshcon add "LABEL" "USER@HOST" PORT
```

Adds new connection to the list.

```
sshcon 
```

Opens searchable ([tab]) prompt with all connections.

```
sshcon delete
```

Enable "delete" mode, where you can delete connections.

```
ssh con "LABEL"
```

Connect with host without prompt

# example

```
sshcon add "VPN server" "root@10.8.1.1" 2020
sshcon con "VPN server" # or without label to enable search
```
