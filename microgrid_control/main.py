import time
import logging
from hardware.hal import HardwareInterface
from core.control_engine import ControlEngine

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting Microgrid Control System...")

    hardware_interface = HardwareInterface(protocol="modbus")
    
    hardware_interface.connect('main_meter', 'grid_meter', '192.168.1.10')
    hardware_interface.connect('transfer_switch', 'ats', '192.168.1.11')
    hardware_interface.connect('battery_system', 'inverter', '192.168.1.12')

    control_engine = ControlEngine(hardware_interface)

    try:
        while True:
            control_engine.run_cycle()
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("System shutdown initiated by user.")
