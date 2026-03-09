"""
Controller candidate for evolutionary search.

The plant is a first-order system:  dy/dt = -a*y + b*u   (a=2, b=3)
Interface contract (do NOT change):
  - Class name: Controller
  - Constructor signature: __init__(self, dt: float)
  - Method signature:      compute(self, setpoint: float, measurement: float) -> float
  - Actuator saturation is applied externally: u is clipped to [-10, 10]

The single EVOLVE-BLOCK contains both methods so they stay consistent.
"""

import math


class Controller:
    # EVOLVE-BLOCK-START
    def __init__(self, dt: float):
        self.dt = dt
        self.Kp = 3.0
        self.Ki = 2.0
        self.Kd = 0.1
        self.integral = 0.0
        self.prev_error = 0.0

    def compute(self, setpoint: float, measurement: float) -> float:
        error = setpoint - measurement
        self.integral += error * self.dt
        derivative = (error - self.prev_error) / self.dt
        self.prev_error = error
        u = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        return u
    # EVOLVE-BLOCK-END
