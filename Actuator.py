from Device import Device


class Actuator(Device):

    def __init__(self, actuator_id, value_type, value_range, initial_state):
        super().__init__(actuator_id, value_type, value_range)
        self.state = initial_state

    def get_state(self):
        return self.state

    def set_state(self, status):
        if status != self.get_state():
            if self.state_type == "continuous":
                try:
                    float(status)
                except Exception:
                    return
                if (self.range is not None) and (status > self.range[1] or status < self.range[0]):
                    return
            elif self.state_type == "discrete" and (status not in self.range):
                return
            else:
                self.state_type = status


class Lamp(Actuator):
    def __init__(self, actuator_id, initial_state):
        super().__init__(actuator_id, "continuous", (0, 1), initial_state)


class Door(Actuator):
    def __init__(self, actuator_id, initial_state):
        super().__init__(actuator_id, "discrete", ["open", "close"], initial_state)
