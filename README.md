# MMA Fighting Updater

Simple application used to notify updates to the Mixed Martial Arts website: mmafighting.com. The script polls the website and uses NMA to push any new updates to an Android device. 

## Prerequisites
* `pip install -r requirement.txt`
* NMA client installed on client device and key saved in `~/.notify/api-key.txt` on the host

## Example Usage (Bash)
Poll every 30 seconds: `while True; do python mma-fighting-updater.py; sleep 30; done;`


rhc ssh pytho
