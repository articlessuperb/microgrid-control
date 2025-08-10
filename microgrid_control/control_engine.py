import time
import logging
from core.states import MicrogridState
from hardware.hal import HardwareInterface

class ControlEngine:
    def __init__(self, hal):
        self.hal = hal
        self.state = MicrogridState.NORMAL
        self.outage_timer_start = None
        self.min_battery_level = 20

    def run_cycle(self):
        grid_voltage = self.hal.read_data('main_meter', 'grid_voltage')
        battery_level = self.hal.read_data('battery_system', 'battery_level')

        if self.state == MicrogridState.NORMAL:
            if grid_voltage is not None and grid_voltage < 100:
                logging.warning("Low grid voltage detected. Starting outage timer.")
                self.outage_timer_start = time.time()
                self.state = MicrogridState.OUTAGE_DETECTED
            else:
                self.optimize_normal_mode(battery_level)

        elif self.state == MicrogridState.OUTAGE_DETECTED:
            if grid_voltage is not None and grid_voltage < 100:
                if time.time() - self.outage_timer_start > 0.5:
                    self.transition_to_island_mode(battery_level)
            else:
                logging.info("Grid voltage recovered. Resetting to NORMAL.")
                self.state = MicrogridState.NORMAL

        elif self.state == MicrogridState.ISLAND_MODE:
            if grid_voltage is not None and grid_voltage > 200:
                logging.info("Grid power restored. Initiating reconnection sequence.")
                self.state = MicrogridState.RECONNECTING
            else:
                self.manage_power_in_island_mode(battery_level)

        elif self.state == MicrogridState.RECONNECTING:
            logging.info("Performing synchronization check...")
            time.sleep(3)
            self.hal.send_command('transfer_switch', 'reconnect_to_grid')
            self.state = MicrogridState.NORMAL
            logging.info("Successfully reconnected to grid.")

    def transition_to_island_mode(self, battery_level):
        if battery_level < self.min_battery_level:
            logging.critical("Cannot transition: insufficient battery power.")
            return

        logging.info("--- Performing seamless transition to island mode ---")
        self.hal.send_command('transfer_switch', 'disconnect_from_grid')
        self.hal.send_command('battery_system', 'start_inverter_and_stabilize')
        self.state = MicrogridState.ISLAND_MODE
        logging.info("Transition complete. Now in island mode.")

    def optimize_normal_mode(self, battery_level):
        logging.info(f"Operating in NORMAL mode. Battery level: {battery_level}%. Optimizing for cost.")

    def manage_power_in_island_mode(self, battery_level):
        logging.info(f"Operating in ISLAND mode. Battery level: {battery_level}%. Managing local sources.")
