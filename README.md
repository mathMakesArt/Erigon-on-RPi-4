# **Erigon-on-RPi-4**
### My personal guide to running an Erigon archive node (Ethereum) on an 8GB Raspberry Pi 4

<br />
<br />

## **Why?**
* Blockchain node software is something that I want to learn more about
* An Ethereum archive node contains immense volumes of data to explore and analyze
* I'm impressed that such a system can sync and run indefinitely on less than 20 watts of electricity
* It seems like a cool idea

<br />
<br />

## **WARNINGS**
**Erigon is still in beta, and may experience database corruption if the `erigon` process is stopped during initial sync (e.g. to reboot).**
* Prior to completion of the initial sync, users should plan to run their computer 24/7 in order to avoid this issue.
* Once the first sync has completed, the `erigon` process can be safely stopped and restarted without loss of data.

<br />
<br />

## **NOTES:**

### **Raspberry Pi Selection**
* I highly recommend using the 8GB version of the RPi Model 4.
* The EthereumOnARM team have built and tested their custom Ubuntu Server image specifically for the version with 8 GB RAM.
* Erigon already recommends a minimum of 16 GB RAM, more than that of the highest-tier RPi. So restricting RAM any further below 8 GB is not advised.
### **Network Setup**
* You must have an internet connection with the ability to port-forward
    * **Port 30303** (on the IP address assigned to the Raspberry Pi) must be open to external traffic, **both TCP and UDP**, before the `erigon` process launches (on reboot)
    * If your router supports it, I find it helpful to assign a static IP address to the RPi
* The EthereumOnARM installer image is designed for wired networking.
* You may be able to complete the steps below using the Raspberry Pi's onboard WiFi, but this will require additional configuration to ensure internet connectivity upon boot.
### **Drive Selection:** Type
* An SSD (Solid State Drive) is an absolute necessity, as HDDs (Hard Disk Drives) do not support the read/write speeds necessary for archive node sync.
* a SATA III SSD is more than fast enough to sync. More modern interfaces such as NVMe are unlikely to offer much of a performance improvement relative to their additional cost. 
### **Drive Selection:** Size
* As of writing, an Erigon archive node (without pruning) can still just barely be run on a 2TB drive.
* 4 TB is a more realistic minimum, as a 2 TB drive will soon be too small to store an entire Erigon archive node data.
* 8 TB is likely overkill, but could be useful in applications where additional storage space is desired.
### **Drive Selection:** Other
* When comparing SSD options, pay attention to the **"TBW"** (Total Bytes Written) value associated with the warranty of each SSD.
* Solid State Drives are typically sold under a warranty for a given amount of time, but this warranty coverage will end early if the TBW value is exceeded.
* The SSD of an archive node will endure a significantly higher TBW per year of runtime, relative to other common SSD applications.
* Similarly-priced drives can have widely varying TBW limits!
### **SSD Integration**
* I used the [**NASPi**](https://wiki.geekworm.com/NASPi), a NUC-style NAS server solution for SATA III drives.
* It is perfectly acceptable to use other alternative products.
* The goal is to facilitate safe integration of a SSD into the Raspberry Pi 4 system.
* The NASPi is sold by Geekworm at [**this URL**](https://geekworm.com/products/geekworm-naspi-2-5-sata-hdd-ssd-kit-for-raspberry-pi-4-model-b), and is also available through other vendors.
* My specific model uses the **X823 V1.5** and **X-C1 V1.3** boards.
### **Other Upgrades for Longevity**
* **Power Surge and Outage Protection**
    * At the very least, I recommend using a surge protector.
    * A UPS (uninterruptable power supply) can protect from power surges and also maintain liveness during a power outage, preventing problems like data corruption and hardware failure.
    * $50 can purchase a UPS with maximum output of 200W or more (far above the power needed for this project).
    * $10 can purchase an Arduino Nano clone board to facilitate sending simple signals to the RPi GPIO, in this case a signal which turns off during a power outage.
    * The Raspberry Pi can then detect this (lack of a) signal within Ubuntu Server, sending whatever commands are necessary to gracefully stop Erigon-related services and shut down the computer.
    * Though it's not necessary for the underlying archive node functionality, I think that blackout protection and automatic shutdown (to conserve backup battery power) are worth the investment in this case.
* **Heatsinks and Temperature Management**
    * I highly recommend some form of active cooling. Without a fan, the system can quickly reach internal temperatures of 90 degrees Celsius or above. Sustained periods of high temperature will reduce hardware lifetimes.
    * If using the NASPi device, a fan is included but heatsinks are not.
        * Any heatsink with thickness of **5 mm or below** will fit under the NASPi fan bracket.
    * I personally used the 4-pack of copper heatsinks (designed specifically for the Raspberry Pi 4) from this larger [**heatsink kit**](https://www.amazon.com/gp/product/B0963BMGFY/).
        * With a 40mm fan but no heatsinks, my node ran at temperatures between 55 and 70 degrees Celsius during sync.
        * After adding the heatsinks, I have seen a temperature reduction of approximately 7 degrees Celsius on average.
    
<br />
<br />

## **FILES INCLUDED:**
Unless otherwise noted, files will be located on the Raspberry Pi.<br />
Intended local paths (within Ubuntu Server) are given in parenthesis after each filename.

* Related to Erigon
    * **erigon.conf** (`/etc/supervisor/conf.d/erigon.conf`)
    * **rpcdaemon.conf** (`/etc/supervisor/conf.d/rpcdaemon.conf`)

  These two files are based on the work of Chase Wright (see Acknowledgements section).

<br />

* Related to power monitoring with Arduino Nano
    * **nano_power_monitor.ino** (N/A)
        * Arduino script for upload to Nano device
    * **safe_shutdown.py** (`/home/arduino/safe_shutdown.py`)
        * Python script which monitors GPIO for (lack of) signal from Arduino Nano
        * Run manually with the following command (NOTE: normally not needed, as this is managed by `rc.local`)
            * `sudo python /home/arduino/safe_shutdown.py`
    * **rc.local** (`/etc/rc.local`)
        * Modified for automatic launch of `safe_shutdown.py` upon startup

<br />
<br />

## **STEPS TO INSTALL AND SYNC ERIGON:**

1. **Download and extract the EthereumOnARM custom Ubuntu Server image for Raspberry Pi**
    * Option 1: [**Direct Link to v21.03.00**](https://www.ethereumonarm.com/downloads/ethonarm_21.03.00.img.zip)
    * Option 2: Find the link in the "Downloads" section of the [**EthereumOnARM Quick Guide**](https://ethereum-on-arm-documentation.readthedocs.io/en/latest/quick-guide/download-and-install.html)
2. **Use a program like [**Balena Etcher**](https://www.balena.io/etcher/) to write this image onto a MicroSD card with at least 16GB capacity**
3. **Connect the SSD to the Raspberry Pi (via the USB3.0 interface, if using NASPi)**
    1. **NOTE:** *The SSD can be in any state, whether empty or formatted or full. The EthereumOnARM image will automatically reformat the disk as needed.*
4. **Connect the Arduino Nano, if applicable, by the following steps**
    1. Connect two wires (e.g. Dupont jumper wires) to the Arduino Nano (if applicable)
        1. By default, my provided software uses the Arduino's **Digital 2** pin and any **Ground**
        2. Jumper wires can be M-F or F-F
            1. The Raspberry Pi GPIO must connect to a Female terminal
            2. The Arduino Nano GPIO can likely accept both Male and Female jumpers, but this may vary depending on the exact model and manufacturer
    2. Connect the Arduino Nano device to a computer and upload the `nano_power_monitor.ino` script
        1. A copy of `nano_power_monitor.ino` can be found this repository
    3. Disconnect the Arduino from the computer and reconnect it to a micro-USB power source
        1. This power source should NOT be connected to the UPS battery backup (if applicable) because the Arduino is supposed to lose all signal during a power outage.
    4. Connect each wire from the Arduino to its appropriate GPIO terminal on the RPi
        1. Digital 2 should connect to RPI GPIO 24 (unless you modify the code)
        2. Ground should connect an RPI GPIO Ground
5. **Before connecting power to the device, connect the RPi to a router (or other appropriate device, such as a network switch) via the Ethernet port**
    1. Also attach a keyboard, mouse, and/or monitor if applicable
    
       (Alternatively, you can interact through an SSH client from another computer)

6. **Connect the device to power (and press the power button, if using a NASPi product)**
7. **Wait for the device to proceed through an automated setup process, including formatting the SSD, until it restarts and eventually prompts you with a login screen**
    1. When prompted to log in, wait 3 additional minutes for multiple lines of other text to complete
8. **Enter the username and password when prompted**
    1. USERNAME: ethereum
       
       PASSWORD: ethereum
9. **Change the password when prompted**
10. **Run the following commands for initial updates**
    1. `sudo apt-get update`
    2. `sudo apt-get upgrade`
11. **Run the following commands if using the "NASPi" product and/or Arduino-based automated shutdown (if applicable)**
    1. `sudo apt-get install -y unzip make gcc python git wiringpi python3-pigpio python-setuptools`
    2. `sudo apt-get install -y python3-distutils`
    3. `wget https://github.com/joan2937/pigpio/archive/master.zip`
    4. `unzip master.zip`
    5. `cd pigpio-master`
    6. `sudo make`
    7. `sudo make install`
    8. `cd ~`
    9. `git clone https://github.com/geekworm-com/x-c1`
    10. `cd x-c1`
    11. `sudo chmod +x *.sh`
    12. `sudo bash install-ubuntu.sh`
    13. `echo "alias xoff='sudo /usr/local/bin/x-c1-softsd.sh'" >> ~/.bashrc`
12. **Edit `~/x-c1/fan.py` to change the temperature thresholds and/or fan speeds, if desired**
    1. `sudo nano fan.py`
13. **Add the `safe_shutdown.py` file (if applicable)**
    1. `cd ..` until root directory is reached
    2. `cd home`
    3. `sudo mkdir arduino`
    4. `cd arduino`
    5. Copy `safe_shutdown.py` to this folder
14. **Install `supervisor` and configure services for Erigon**
    1. `cd ..` to root directory
    2. `cd home`
    3. `sudo apt-get install supervisor`
    4. `cd ..` to root directory
    5. `cd etc`
    6. `sudo nano rc.local` to edit the `rc.local` file for autorun on startup
        1. Replace the existing file contents with that of this repository
    7. `cd supervisor/conf.d`
    8. Create `/etc/supervisor/erigon.conf` and `/etc/supervisor/rpcdaemon.conf`, pasting in the contents from this repository
        1. `sudo nano erigon.conf`
        2. `sudo nano rpcdaemon.conf`

        <br />

    **NOTE:** If you are using the default `erigon` service instead of `supervisor`, the relevant configuration filepaths are `/etc/ethereum/erigon.conf` and `/etc/ethereum/erigon-rpc.conf`.
15. **Install Erigon**
    1. `sudo apt-get install erigon`
16. **Stop and disable the `geth` service, which is enabled by default**
    1. `sudo systemctl stop geth`
    2. `sudo systemctl disable geth`
17. **Ensure that the `erigon` process is disabled (to launch through `supervisor` instead)**
    1. `sudo systemctl disable erigon`
    
    <br />

    **NOTE:** If you are using the default `erigon` process instead of `supervisor`, you should SKIP this step!
18. **Edit the file `/etc/ethereum/erigon.conf` to ensure Erigon is properly configured as an archive node without pruning**
    1. `cd ..` to root directory
    2. `cd etc/ethereum`
    3. `sudo nano erigon.conf`
        1. Delete the `--blockDownloaderWindow 32768 --prune=hrtc` content
        2. Full file should be a single line containing the following content only:

           `ARGS="--datadir /home/ethereum/.erigon --private.api.addr 127.0.0.1:8090"`
19. **If the system time is incorrect, set your timezone and enable network-based clock synchronization**
    1. `sudo apt install systemd-timesyncd`
    2. `sudo timedatectl set-timezone America/New_York` (or whatever timezone applies)
        1. If the above command fails, use

           `sudo dpkg-reconfigure tzdata`

           and select your timezone through the GUI
    3. `sudo timedatectl set-ntp true`
    4. Check the results of the clock sync with
       
       `timedatectl`
20. **Reboot one more time to begin the Erigon sync process (automatically upon startup)**
    1. `sudo reboot`

<br />
<br />

## **STEPS TO MONITOR THE SYNC:**

There are a variety of ways to monitor the Erigon sync process. I personally tend to keep multiple simultaneous SSH connections open, with different commands running in each terminal. The commands are explained below.
1. `sudo tail -f /home/erigon.err.log`
    * Displays the most recent contents (and live updates) to the Erigon error logfile
    * This will include warnings and errors, but also details about the current sync progress and actions
2. `htop`
    * By default allows monitoring of CPU and memory usage, on both a total and per-process basis
    * Through the **F2 (Setup)** option, you can add additional metrics for display
        * I find the `DISK R/W`, `DISK READ`, and `DISK WRITE` columns to be especially useful for understanding SATA activity
    * Through the **F4 (Filter)** option, you can filter to display results containing the string "erigon"
3. `sudo watch -n 2 sensors`
    * Outputs data from the Raspberry Pi temperature sensor, every 2 seconds
    * Requires `sudo apt install lm-sensors` first
4. `slurm -i eth0`
    * Given the name of a network interface, continuously displays data of download and upload rates. Includes a (terminal-based) graph of the instantaneous rates over time.
    * Requires `sudo apt install slurm` first

<br />
<br />

## **STEPS TO BACK UP (AFTER SYNC COMPLETION):**

When the initial sync has completed, I recommend backing up the Erigon chain data (and other related files).

If the live node state becomes corrupted in the future (or if you want to run an additional node) it is possible to restore from this backup, instead of waiting for the initial sync process to complete again.

1. `sudo fdisk -l`
    1. To list the disks available
2. `sudo mkdir /mnt/backup`
    1. Create a new directory (within `/mnt/`) at which the backup disk will be mounted
3. `sudo mount /dev/sdb2 /mnt/backup`
    1. To mount the chosen disk at `/mnt/backup` (replace `/dev/sdb2` with your chosen disk)
4. `sudo cp -rv /home/ethereum /mnt/backup`
    1. To copy (and print a line for each copied file) the entire contents of `/home/ethereum` into the newly mounted disk

<br />
<br />

## **STEPS TO RESTART SYNC:**

In the case of data corruption or other problems, you can run the following commands to stop Erigon and delete the existing data directory, then reboot to restart the sync from the beginning.
1. `sudo systemctl stop supervisor`
    1. **NOTE:** Use `sudo systemctl stop erigon` instead if `supervisor` is not being used
2. `sudo rm -rf /home/ethereum/.erigon`
3. `sudo reboot`
    1. To resume Erigon without a reboot, use `sudo systemctl start supervisor`

<br />
<br />

## ACKNOWLEDGEMENTS
* **The Ethereum on ARM community** for all of their research in creating the ARM64 image and for their documentation, especially the guide to managing Ethereum clients
    * https://ethereum-on-arm-documentation.readthedocs.io/en/latest/user-guide/managing-clients.html
* Chase Wright ([**@mysticryuujin**](https://twitter.com/mysticryuujin)) for his "Getting Started with Erigon on Ubuntu" blogpost
    * https://chasewright.com/getting-started-with-turbo-geth-on-ubuntu/
