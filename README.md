## Running the project:

Create a `python 3` virtual environment.

Install the requirements by `pip install -r requirements`

Run the project by:

`python app.py`
 
Now you may go to http://0.0.0.0:5000 in your browser.

## Object Entities
In the code, we have defined the following Classes.
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

Note: All instances of `Sensor` and `Actuator`, namely `Door`, `Lamp`, `Proximity`, `Noise`, `Motion` and `Face` implement a `build_rule` function which specifies for our front end and rule engine the representation rules for these entities.

Note: `Face` sensor is an extension of the main proposal of system. It can detect emotions of a person and send the amount of happiness(!) of the person to the server!

## Client/Server communication

### Overall Summary

The clients which correspond to IoT objects, whether actuators or sensors are implemented as web pages, each corresponding to an independent process. For the clients' implementation and the client/server communication, we have used the following libraries: `Vue.js`, `Semantic`, `Flask`, and `Websocket`. 

The server is mainly implemented in `app.py` and handles the clients' request in the backend.

### Initializing Communication Channel

First, the client sends a `init` message with `type` of the state and its `value`.

Once this request is received by the server in the function `init` an instance of the `Device` class will be created using the request-id from the web socket as `device_id`, `type` as`state_type`, and `value` as the initial `state` and stored.

This object is used for all further server/client interactions and also in the rule engine. 

Note: the function `init` calls within it the function `update_admin`, which updates the user interface of our server's admin panel with the created device if necessary.

### Updating/Receiving States: 

If the value corresponding to the state of a device, whether an actuator or sensor, is changed, an event listener within our clients will trigger the function`update_state` in `app.py`, which applies the corresponding update in the backend appropriately.

Note: As soon as the state of a device changes, we check using our implemented rule engine the rules associated with or including that device and then re-evaluate the rules, firing(executing) the appropriate actions. 

### Automatic Sensor Streaming Inputs

We allow the user to choose whether they want to manually enter the sensory inputs on the sensor's corresponding web page or want the sensory input to switch to a valid random state in randomly chosen time intervals to appropriately test for the robustness of the implemented rules and system performance. 

This is implemented in the user interface of all web pages corresponding to sensors and is as simple as a click for the user/tester.

## Rule Engine

### Backend

Our rule engine receives a dictionary generated by the rule specifier in the user interface utilizing `Vue.js`. We parse the given dictionary into a tree whose intermediary nods are `all` corresponding to the logical AND or `any` corresponding to the logical OR. The leaves of this tree are atomic boolean expressions which can be evaluated easily. The evaluation of the rule is then done by parsing this tree recursively. 

Note: The boolean expressions are evaluated using the `BooleanExpression` class in `boolexpr.py`, and the tree is implemented using the `Node` class in `tree.py`.

### Frontend

When a new rule is specified in the admin panel, the `update_rules` function is triggered in `app.py`, which will add the rule to the set of existing ones and checks which devices, whether sensor or actuators, are involved. This comes in handy when the state of actuators/sensors change, and the re-evaluation of the rule is necessary. Read the note on Update/Receiving States for more information.

