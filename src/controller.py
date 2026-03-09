"""
PID feedback controller and first-order plant simulator.
Plant model: dy/dt = -a*y + b*u   (default a=2, b=3)
"""


class PIDController:
    def __init__(self, Kp, Ki, Kd, dt):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.dt = dt
        self.integral = 0.0
        self.prev_error = 0.0

    def compute(self, setpoint, measurement):
        error = setpoint - measurement
        self.integral += error * self.dt
        derivative = (error - self.prev_error) / self.dt
        self.prev_error = error
        return self.Kp * error + self.Ki * self.integral + self.Kd * derivative


def simulate(setpoint=1.0, duration=10.0, dt=0.01, a=2.0, b=3.0,
             Kp=3.0, Ki=2.0, Kd=0.1, u_max=10.0, u_min=-10.0, verbose=True):
    """Simulate the PID controller on the first-order plant and return (times, outputs)."""
    pid = PIDController(Kp=Kp, Ki=Ki, Kd=Kd, dt=dt)

    y = 0.0
    t = 0.0
    steps = int(duration / dt)
    times, outputs = [], []

    if verbose:
        print(f"{'Time':>8} {'Output':>10} {'Error':>10} {'Control':>10}")
        print("-" * 42)

    log_times = set(round(i * duration / 20, 4) for i in range(21))

    for _ in range(steps):
        u = pid.compute(setpoint, y)
        u = max(u_min, min(u_max, u))
        dydt = -a * y + b * u
        y += dydt * dt
        t = round(t + dt, 6)
        times.append(t)
        outputs.append(y)

        if verbose and any(abs(t - lt) < dt / 2 for lt in log_times):
            error = setpoint - y
            print(f"{t:8.3f} {y:10.4f} {error:10.4f} {u:10.4f}")

    if verbose:
        print("-" * 42)
        print(f"Final output: {y:.6f}  (setpoint: {setpoint})")
        print(f"Steady-state error: {abs(setpoint - y):.2e}")

    return times, outputs
