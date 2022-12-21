from collections import deque
import qwiic_icm20948
import qwiic_tca9548a
import qwiic_i2c
import time
import sys
import csv

def write_data(deque, writer):
    while deque:
        writer.writerow(deque.popleft())

timestamp = int(time.time())
filename = f'sensor_data_{timestamp}.csv'

def runExample(imus):
    # Initialize the deque and variables for data acquisition
    DEQUE_SIZE = 1000
    ACQ_INTERVAL = 0.01
    data_deque = deque(maxlen=DEQUE_SIZE)

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        f.write('sensor,time,ax,ay,az,gz,gy,gz,mx,my,mz\n')
        while True:
            for i, imu in enumerate(imus):
                mux.enable_channels(i)
                if imu.dataReady():
                    imu.getAgmt()
                    t = time.perf_counter()
                    data_point = [i, t, imu.axRaw, imu.ayRaw, imu.azRaw, imu.gxRaw, imu.gyRaw, imu.gzRaw, imu.mxRaw, imu.myRaw, imu.mzRaw]
                    data_deque.append(data_point)
            write_data(data_deque, writer)
            time.sleep(ACQ_INTERVAL)

if __name__ == '__main__':
    # Initialize the multiplexer
    mux = qwiic_tca9548a.QwiicTCA9548A()

    # Initialize the first ICM20948 sensor
    IMU1 = qwiic_icm20948.QwiicIcm20948()
    mux.enable_channels(1)
    if not IMU1.begin():
        print("The first Qwiic ICM20948 device isn't connected to the system. Please check your connection", file=sys.stderr)

    # Initialize the second ICM20948 sensor
    IMU2 = qwiic_icm20948.QwiicIcm20948()
    # Switch the multiplexer to channel 2
    mux.enable_channels(6)
    if not IMU2.begin():
        print("The first Qwiic ICM20948 device isn't connected to the system. Please check your connection", file=sys.stderr)

   # Add the sensors to a list for easy looping
    imus = [IMU1, IMU2]

    try:
        runExample(imus)
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)