# SSH Honeypot
I coded a SSH Honeypot using python from scratch. This code will simulate a SSH Server for attackers to connect and they're gonna spend their time to attach the server (bruteforce attack, etc)
## Features
- Log the connection and geolocation of the attacker
- Bruteforce attack detector
- Simulate the Ubuntu SSH shell
## Requirement
- Python 3.9+
- Paramiko installed
  ```python
  pip install paramiko
  ```
- GeoIP2 installed
  ```python
  pip install geoip2
  ```
- GeoLite / GeoIP database
  You can download the free GeoLite database from maxmind, but you need your free license key. Make sure that you have an maxmind account and download the database into the directory
  ```
  curl "https://download.maxmind.com/app/geoip_download_by_token?edition_id=GeoLite2-City&license_key={LICENSE KEY HERE}&suffix=mmdb.gz" -o GeoLite2-City-database.tar.gz \
    && tar -xzvf GeoLite2-Country.tar.gz
  ```
## How to run?
- Clone this repository into your local directory
  ```
  git clone https://github.com/alfredoknnth/ssh-honeypot
  ```
- Install the requirement packages using
  ```python
  pip install -r requirement.txt
  ```
- Change the `SSH_HOST`, `SSH_PORT`, and other configuration in `config.py`
- Run the dummy server using
  ```python
  python server.py
  ```
