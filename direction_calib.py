from Classes.direction import Compass
import time
import math

a = Compass()
sensor = a.sensor

while True:
    raw_accel_x, raw_accel_y, raw_accel_z = sensor.raw_acceleration
    accel_x, accel_y, accel_z = sensor.acceleration
    raw_mag_x, raw_mag_y, raw_mag_z = sensor.raw_magnetic
    mag_x, mag_y, mag_z = sensor.magnetic

    heading = (math.atan2(sensor.magnetic[1], sensor.magnetic[0]) * 180) / math.pi
    if heading < 0: heading += 360

    print('Acceleration raw: ({0:6d}, {1:6d}, {2:6d}), (m/s^2): ({3:10.3f}, {4:10.3f}, {5:10.3f})'.format(raw_accel_x, raw_accel_y, raw_accel_z, accel_x, accel_y, accel_z))
    print('Magnetometer raw: ({0:6d}, {1:6d}, {2:6d}), (gauss): ({3:10.3f}, {4:10.3f}, {5:10.3f})'.format(raw_mag_x, raw_mag_y, raw_mag_z, mag_x, mag_y, mag_z))
    print('Direction: {}'.format(heading))
    print('')
    time.sleep(1)