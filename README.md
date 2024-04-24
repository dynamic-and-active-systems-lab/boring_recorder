# boring_recorder
An RPI audio recorder

### Hardware
This system expects the [RPI Relay Board](https://www.waveshare.com/wiki/RPi_Relay_Board) and the [CodecZero](https://www.raspberrypi.com/documentation/accessories/audio.html) to be installed on the RPI. The relay board should be wired to provide 27 V to the PCB signal conditioner as shown in the image. 

### Pre-reqs
1. Create a repos directory on your RPI in your home folder:
   ```
   user@raspberrypi:~ $ mkdir repos
   user@raspberrypi:~ $ cd repos
   ```
2. Clone this repo into that directory:
   ```
   git clone https://github.com/dynamic-and-active-systems-lab/boring_recorder
   ```
3. Pi-Codec is a submodule that can be initialized after the cloning of this repo with 
	`git submodule update --init --recursive`

4. When using this for the first time, you need to generate the virtual environment and install the necessary packages:
  ```
	python3 -m venv .venv
	source ./venv/bin/activate
	pip install -r requirements.txt
  ```
### Running on boot
To get the audio recording to run on boot, you need to edit the crontab file on the RPI:
```
sudo crontab -e
```
Once in the file add the following:
```
@reboot /bin/sleep 10; /home/dasl/repos/boring_recorder/recorderLaunch.sh  >> /home/dasl/repos/boring_recorder/mycrontablog.txt 2>&1
```

### Notes on modifications of python packages or submodules
1. If you add new package requirements, add them to the requirements.txt file using
	`pip3 freeze > requirement.txt`
2. Note on initial setup: to add other submodules, use
`git submodule add <webaddress_of_git_repo>`



