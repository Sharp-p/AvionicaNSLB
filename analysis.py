import drivers.stubs as stb
import drivers.driver as td
import thirdParty
import time
import math

class Analisys:
    BUFFER_SIZE = 50

    AVG_WEIGHT = 1/BUFFER_SIZE

    # A safe time for the least duration to reach the apogee
    T_SAFE = 7

    baro = td.Baro()

    # if > n the rocket has launched
    launch_counter = 0
    # if > n the rocket has reached the apogee
    return_counter = 0
    # Meters from the sea level of the launch site
    launch_altitude = 1236
    # Last altitudes
    lst_altitude = [0.0] * BUFFER_SIZE

    def __init__(self):
        """ 
        Creates a log file for the flight data and measures the time.
        """
        with open("log.csv", "w") as log:
            # Parameters
            log.write("timestamp,rel_timestamp,altitude,pressure,raw pressure,deviation\n")

            # First line
            buffer = self.get_pressure_buffer()
            filtered_p = self.finite_impulse_response(buffer)
            self.lst_altitude.pop(0)
            self.lst_altitude.append(round(self.calc_altitude(filtered_p), 3))
            log.write(f"NULL,{time.monotonic()},{self.lst_altitude[-1]},{filtered_p},{buffer[-1]},{self.get_deviation()}\n")
        
        self.start_t = time.monotonic()
        self.launch_t = self.start_t
        self.relative_t = 0

    def update_log(self) -> None:
        """
        Manages the readings from the barometer and updates the flight log.
        """
        
        buffer = self.get_pressure_buffer()

        filtered_p = self.finite_impulse_response(buffer)

        altitude = self.calc_altitude(filtered_p)

        with open("log.csv", "+a") as log:

            if self.launch_counter < 10:
                # The rocket has not launched so it updates the launch_counter
                if self.lst_altitude[-1] < altitude:
                    self.launch_counter += 1
                    # Sets the launch time, so current time minus the time that it takes to detect that the rocket has launched
                    self.launch_t = time.monotonic() - 0.5
                else:
                    self.launch_counter = 0
            else:
                # The rocket has launched so now it just updates the time since the launch
                self.relative_t = time.monotonic() - self.launch_t

            if self.return_counter < 10 and self.launch_counter > 9:
                if self.relative_t > self.T_SAFE and self.lst_altitude[-1] > altitude:
                    self.return_counter += 1
                else:
                    self.return_counter = 0

            self.lst_altitude.pop(0)
            self.lst_altitude.append(round(altitude, 3))
            log.write(f"{time.monotonic() - self.start_t},{self.relative_t},{altitude},{filtered_p},{buffer[-1]},{self.get_deviation()}\n")

    def get_pressure_buffer(self) -> list[float]:
        """
        Reads five times from the barometer and returns the buffer.
        """
        buffer = []

        for i in range(self.BUFFER_SIZE):
            buffer.append(self.baro.getPressure())
        return buffer

    def finite_impulse_response(self, impulse: list) -> float:
        """
        Applies a Finite Impulse Response filter to the input impulse, of length 5.
        Returns the filtered value.
        """
        if len(impulse) != self.BUFFER_SIZE:
            raise ValueError("[ERROR] Invalid impulse length.")

        filtered = 0
        for val in impulse:
            filtered += val * self.AVG_WEIGHT
        return filtered
    
    def calc_altitude(self, pressure: float) -> float:
        """ 
        Calculates the altitude from the atmospheric pressure
        """
        mbars = pressure / 100

        feet = 145366.45*(1-(mbars/1013.25)**0.190284)

        meters = feet / 3.281
        return meters

    def get_deviation(self) -> float:
        """
        Calculates the deviation from the last BUFFER_SIZE altitude measurments
        :return: deviation
        """
        mean = sum(self.lst_altitude) / self.BUFFER_SIZE

        sums = 0.0
        for val in self.lst_altitude:
            sums += (val - mean) ** 2
        return math.sqrt(sums / (self.BUFFER_SIZE - 1))

    def get_avg_distance(self) -> float:
        """
        Calculates the average distance from the mean from the last BUFFER_SIZE altitude measurments
        :return: avg distance
        """
        mean_grouped = (sum(self.lst_altitude)) / self.BUFFER_SIZE

        sums = 0.0
        for val in self.lst_altitude:
            sums += math.fabs((val - mean_grouped))
        return sums / self.BUFFER_SIZE

