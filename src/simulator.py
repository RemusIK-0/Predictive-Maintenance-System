import time
import random
from database_manager import DatabaseManager

def run_simulator():
    db = DatabaseManager()
    sensor_id = 'Engine_01'

    base_temp = 50.0
    base_vib = 0.5
    base_press = 100.0
    wear_factor = 0.0

    print(f"Simulator is starting for {sensor_id}...")

    try:
        while True:
            wear_factor += 0.01

            temp = base_temp + (wear_factor * 2) + random.uniform(-1,1)
            vib = base_vib + (wear_factor * 0.5) + random.uniform(-0.1,0.1)
            press = base_press + (wear_factor * 0.2) + random.uniform(-2,2)

            failure = 1 if (temp > 85 or vib > 4.0) else 0

            db.insert_record(sensor_id, round(temp, 2), round(vib, 2), round(press, 2), failure)

            status = 'CRITIC' if failure == 1 else 'OK'
            print(f'{status} Temp: {temp} | Vib: {vib} | Press: {press}')

            if failure == 1:
                print('Equipment damaged | Reset simulator...')
                wear_factor = 0
                time.sleep(5)
            time.sleep(1)
    except KeyboardInterrupt:
        print('\nProccess stoped.')

if __name__ == '__main__':
    run_simulator()