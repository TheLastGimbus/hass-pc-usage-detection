# Home Assistant PC usage detection

## What is this?
This is a super simple script that monitors if you are using your PC (either touching keyboard or mouse), and reports this to Home Assistant

It uses [HTTP binary sensor](https://www.home-assistant.io/integrations/http#binary-sensor)

## How to use it?
1. Download it: `git clone https://github.com/TheLastGimbus/hass-pc-usage-detection/` - or just press "download zip" button above
2. Get your [Home Assistant long-lived access token](https://www.home-assistant.io/docs/authentication/#your-account-profile)
3. (Optional, but **very recomended**) [Set up SSH tunnel to your Home Assistant](#ssh-tunnel)
4. `pip3 install -r requirements.txt`
5. `python3 main.py --url "http://<home_assistant_ip>:<port>/api/states/binary_sensor.<binary_sensor_name>" --token <HASS_LONG_LIVE_TOKEN> --keyboard --mouse`

You need to specify `--keyboard` and `--mouse` flags to detect keeb/mouse activity

Default time of no-activity after PC is unused is 3 minutes. You can specify this with `--time <seconds>`

## Example setup:
If you are actually going to rely on this, I recommend you few things from my setup:
 - make external [template binary sensor](https://www.home-assistant.io/integrations/binary_sensor.template/) that will also check if your PC is even reachable:
 ```yaml
 binary_sensor:
  - platform: ping
    name: Ping PC
    host: 192.168.1.101  # You need to set yourself static IP address
  - platform: template
    sensors:
      pc_active:
        friendly_name: "PC active"
        value_template: >-
          {{ is_state('binary_sensor.pc_is_touched_script', 'on')
             and is_state('binary_sensor.ping_pc', 'on') }}
```
Now, you can safely use `binary_sensor.pc_active` in your automations!

 - make startup script and add it to your autostart:
This is what I use on Ubuntu - replace `matiii@192.168.1.242` with your server `user@address`:
```bash
#!/bin/bash

# I run SSH tunnel and script separatly in screen, so I can manage and restart them whenever I want

# Set up SSH tunnel
screen -S "hass-ssh-tunnel" -dm ssh -L 9876:192.168.1.242:8123 -N -T matiii@192.168.1.242
screen -S "hass-python-presence-detector" -dm bash -c '\
  MY_SCRIPT_PATH="/PATH/TO/SCRIPT/FOLDER" ; \
  # This is to activate Python virtual enviroment, very recommended, but you can skip it \
  source "$MY_SCRIPT_PATH/venv/bin/activate" ; \
  python3 "$MY_SCRIPT_PATH/main.py" \
      --url "http://localhost:9876/api/states/binary_sensor.pc_is_touched_script" \
      --time 60 \
      --token "HOME_ASSISTANT_LONG_LIVED_TOKEN" \
      --keyboard \
      --mouse \
'
```

If you don't know what `screen` and `venv` is, here is simplified version:
```bash
#!/bin/bash
# Set up SSH tunnel
ssh -L 9876:192.168.1.242:8123 -N -T matiii@192.168.1.242
MY_SCRIPT_PATH="/PATH/TO/SCRIPT/FOLDER"
python3 "$MY_SCRIPT_PATH/main.py" \
    --url "http://localhost:9876/api/states/binary_sensor.pc_is_touched_script" \
    --time 60 \
    --token "HOME_ASSISTANT_LONG_LIVED_TOKEN" \
    --keyboard \
    --mouse
```

Of course, this will look a little different on Windows :no_good:

Now, place this in your autostart and you should be good to go

#### SSH tunnel?
If you are running Home Assistant on your local network, and connecting to your local address (something like `192.168.x.x`) 
with standard HTTP (without `S`) - anyone sniffing your WiFi could get your access token - that gives almost full access to all your home!

To protect against it, you can set up SSH tunnel that encrypts all traffic and ensures that you are connected to your server, and not the potential attacker

1. Set up SSH on your server and SSH keys on your computer (it's easy, Google how to do that if you don't have it already)
2. Type into terminal/cmd: `ssh -L 9876:<home_assistant_ip>:8123 -N -T <user>@<home_assistant_ip>`

`9876` (you can change this) is port that will open on your client (your pc), and `8123` (default HASS port) is port that will be directed to on your server

You can open the browser and type in `localhost:9876` to see for yourself!

