import time
import logging

class HardwareInterface:
    def __init__(self, protocol="modbus"):
        self.protocol = protocol
        self.devices = {}
        logging.basicConfig(level=logging.INFO)

    def connect(self, device_id, device_type, address):
        try:
            logging.info(f"Connecting to {device_type} at {address} via {self.protocol}...")
            self.devices[device_id] = {'type': device_type, 'status': 'connected', 'address': address}
            return True
        except Exception as e:
            logging.error(f"Failed to connect to {device_id}: {e}")
            return False

    def read_data(self, device_id, data_point):
        if device_id in self.devices and self.devices[device_id]['status'] == 'connected':
            try:
                if data_point == 'grid_voltage':
                    if time.time() % 20 < 10:
                        return 0
                    return 220
                if data_point == 'battery_level':
                    return 75
                if data_point == 'solar_production':
                    return 10
            except Exception as e:
                logging.error(f"Error reading {data_point} from {device_id}: {e}")
                return None
        return None

    def send_command(self, device_id, command):
        if device_id in self.devices and self.devices[device_id]['status'] == 'connected':
            logging.info(f"Sending command '{command}' to device {device_id}")
            return True
        return False
