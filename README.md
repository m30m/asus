How to run the project:

Create a python3 virtual environment

Install the requirements by `pip install -r requirements`

Run the project:

`python app.py`


## Object Entities

### Device
Represent a general device, which may be an Actuator or a Sensor. This object entity possesses the following attributes: `device_id`, `state_type` and `value_range`. The `state_type` can be `continuous` or `discrete`. 

The `value_range` for `discrete` types is captured by a python `list`.

The `value_range` for `continuous` type is captured either by a `tuple` specifying `min` and `max` as `(min, max)` or by `None`, which indicates the variable can contain any real number.

### Actuator

This class inherits `Device` and most notably implements the function `set_state`, which allows the central server to update an actuator's status. The update is only executed after checking the assigned value is of the appropriate `state_type` and within the relevant `value_range`.

`Door` and `Lamp` are entities inheriting from the `Actuator` class and representing the project's actuators.

### Sensor:

This class inherits the device and most notably implements the function `recieve_state`, which allows the central server to update its perception of the environment based on the received sensory input from the connected clients.

`Proximity`, `Noise`, and `Motion` are entities inheriting `Sensor` representing the sensors defined in the project.

Note: All instances of `Sensor` and `Actuator`, namely `Door`, `Lamp`, `Proximity`, `Noise`, and `Motion` implement a `build_rule` function which specifies for our front end and rule engine the representation rules for these entities.

## Client/Server communication

Initialization

First, the client sends a `init` message with the following parameters:
`type`:
`state`:

Sending New State: `update_state`

`state`

Receiving New actions `act`
`state`
