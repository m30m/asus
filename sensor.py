from device import Device
from state import device_names


class Sensor(Device):
    def __init__(self, sensor_id, value_type, value_range):
        super().__init__(sensor_id, value_type, value_range)

    def get_state(self):
        return self.state

    def get_state_label(self):
        raise NotImplemented

    def receive_state(self, state):
        self.state = state


class Motion(Sensor):
    type = 'motion'

    def __init__(self, sensor_id):
        super().__init__(sensor_id, "discrete", ["motion", "no motion"])

    def build_rule(self):
        return {
            'type': 'radio',
            'label': 'Motion Sensor: %s' % device_names.get(self.device_id, self.type),
            'id': self.device_id,
            'choices': [{'label': "No Motion", 'value': False}, {'label': "Motion detected", 'value': True}]
        }

    def get_state_label(self):
        if self.get_state():
            return 'Motion Detected'
        else:
            return 'No Motion'


class Noise(Sensor):
    type = 'noise'

    def __init__(self, sensor_id):
        super().__init__(sensor_id, "discrete", ["no noise", "noise"])

    def build_rule(self):
        return {
            'type': 'radio',
            'label': 'Noise Sensor: %s' % device_names.get(self.device_id, self.type),
            'id': self.device_id,
            'choices': [{'label': "No Suspicious Noise", 'value': False},
                        {'label': "Suspicious Noise Detected", 'value': True}]
        }

    def get_state_label(self):
        if self.get_state():
            return 'Suspicious Noise Detected'
        else:
            return 'No Suspicious Noise'


class Proximity(Sensor):
    type = 'proximity'

    def __init__(self, sensor_id):
        super().__init__(sensor_id, "continuous", None)

    def build_rule(self):
        return {
            'type': 'numeric',
            'label': 'Prxomity Sensor: %s' % device_names.get(self.device_id, self.type),
            'id': self.device_id,
        }

    def get_state_label(self):
        return 'Proximity: %s' % self.get_state()
