from Device import Device


class Sensor(Device):
    def __init__(self, sensor_id, value_type, value_range):
        super().__init__(sensor_id, value_type, value_range)

    def get_state(self):
        pass


class Motion(Sensor):
    def __init__(self, sensor_id):
        super().__init__(sensor_id, "discrete", ["motion", "no motion"])


class Noise(Sensor):
    def __init__(self, sensor_id):
        super().__init__(sensor_id, "discrete", ["motion", "no motion"])


class Proximity(Sensor):
    def __init__(self, sensor_id):
        super().__init__(sensor_id, "continuous", None)
