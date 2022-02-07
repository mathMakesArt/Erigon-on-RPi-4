import pigpio
import time
import subprocess

# CONFIGURATION VARIABLES
GPIO_NUM = 24
WAIT_SECONDS = 10.0
SHUTDOWN_SECONDS = 6300.0 # 105 minutes
FLAG_INITIAL_SYNC = False

def main():

    # Initialization of variables with default values
    flagPinOff = False
    flagShutdown = False
    offSecondsCount = 0.0
    pi = pigpio.pi()

    # Exit early if unable to establish a GPIO connection
    if not pi.connected:
        print("UNABLE TO CONNECT TO GPIO.")
        exit()

    # Set pin mode and pulldown resistor state
    pi.set_mode(GPIO_NUM, pigpio.INPUT)
    pi.set_pull_up_down(GPIO_NUM, pigpio.PUD_DOWN)

    # Loop until power is lost for greater than SHUTDOWN_SECONDS seconds
    while(flagShutdown == False):
        currentVal = pi.read(GPIO_NUM)                 # Read the designated pin
        flagPinOff = (currentVal == 0)           # Update flagPinOff
        print("currentVal = " + str(currentVal) + ", offSecondsCount = " + str(offSecondsCount)) # Print to console
        time.sleep(WAIT_SECONDS)                 # Wait for WAIT_SECONDS seconds

        # If the designated pin detects no signal, increment offSecondsCount and check against SHUTDOWN_SECONDS
        if flagPinOff:
            offSecondsCount += WAIT_SECONDS
            if (offSecondsCount >= SHUTDOWN_SECONDS):
                flagShutdown = True
        # Reset offSecondsCount if the designated pin detects a signal
        else:
            offSecondsCount = 0

    # Set of actions to carry out during safe shutdown routine
    # 1. Ending the supervisor task
    print("\n\n\nENDING SUPERVISOR WITH: sudo systemctl stop supervisor\n\n\n")
    stopSupervisor = subprocess.Popen(["sudo", "systemctl", "stop", "supervisor"], stdout=subprocess.PIPE)
    print(stopSupervisor.communicate())

    # 2. Clearing the Erigon data directory (ONLY in initial sync mode)
    if FLAG_INITIAL_SYNC:
        print("\n\n\nENDING SUPERVISOR WITH: sudo rm -rf /home/ethereum/.erigon\n\n\n")
        clearData = subprocess.Popen(["sudo", "rm", "-rf", "/home/ethereum/.erigon"], stdout=subprocess.PIPE)
        print(clearData.communicate())

    # 3. Safe shutdown of NASPi device
    print("\n\n\nINITIALIZING SAFE SHUTDOWN WITH: sudo /usr/local/bin/x-c1-softsd.sh\n\n\n")
    safeShutdown = subprocess.Popen(["sudo", "/usr/local/bin/x-c1-softsd.sh"], stdout=subprocess.PIPE)
    print(safeShutdown.communicate())

main()
