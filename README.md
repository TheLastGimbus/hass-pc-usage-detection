# Home Assistant PC usage detection

## What is this?
This is a super simple script that monitors if you are using your PC (either touching keyboard or mouse), and reports this to Home Assistant

It uses [HTTP binary sensor](https://www.home-assistant.io/integrations/http#binary-sensor)

## How to use it?
1. Download it: `git clone https://github.com/TheLastGimbus/hass-pc-usage-detection/` - or just press "download zip" button above
2. Get your [Home Assistant long-lived access token](https://www.home-assistant.io/docs/authentication/#your-account-profile)
3. (Optional, but **very recomended**) [Set up SSH tunnel to your Home Assistant](#ssh-tunnel)
4. `python3 main.py --url "http://<home_assistant_ip>:<port>/api/states/binary_sensor.<binary_sensor_name>" --token <HASS_LONG_LIVE_TOKEN> --keyboard --mouse`

You need to specify `--keyboard` and `--mouse` flags to detect keeb/mouse activity

Default time of no-activity after PC is unused is 3 minutes. You can specify this with `--time <seconds>`

#### SSH tunnel?
If you are running Home Assistant on your local network, and connecting to your local address (something like `192.168.x.x`) 
with standard HTTP (without `S`) - anyone sniffing your WiFi could get your access token - that gives almost full access to all your home!

To protect against it, you can set up SSH tunnel that encrypts all traffic and ensures that you are connected to your server, and not the potential attacker

1. Set up SSH on your server and SSH keys on your computer (it's easy, Google how to do that if you don't have it already)
2. Type into terminal/cmd: `ssh -L 9876:<home_assistant_ip>:8123 -N -T <user>@<home_assistant_ip>`

`9876` (you can change this) is port that will open on your client (your pc), and `8123` (default HASS port) is port that will be directed to on your server

You can open the browser and type in `localhost:9876` to see for yourself!

