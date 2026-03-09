"""
Simple PID Feedback Controller
Simulates controlling a first-order plant: dy/dt = -a*y + b*u
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


def simulate(setpoint=1.0, duration=10.0, dt=0.01):
    # Plant: first-order system dy/dt = -a*y + b*u
    a, b = 2.0, 3.0

    # PID gains
    pid = PIDController(Kp=3.0, Ki=2.0, Kd=0.1, dt=dt)

    y = 0.0  # initial output
    t = 0.0
    steps = int(duration / dt)

    print(f"{'Time':>8} {'Output':>10} {'Error':>10} {'Control':>10}")
    print("-" * 42)

    log_times = set(round(i * duration / 20, 4) for i in range(21))

    for _ in range(steps):
        u = pid.compute(setpoint, y)
        u = max(-10.0, min(10.0, u))          # actuator saturation
        dydt = -a * y + b * u
        y += dydt * dt
        t = round(t + dt, 6)

        if any(abs(t - lt) < dt / 2 for lt in log_times):
            error = setpoint - y
            print(f"{t:8.3f} {y:10.4f} {error:10.4f} {u:10.4f}")

    print("-" * 42)
    print(f"Final output: {y:.6f}  (setpoint: {setpoint})")
    print(f"Steady-state error: {abs(setpoint - y):.2e}")


if __name__ == "__main__":
    simulate()
