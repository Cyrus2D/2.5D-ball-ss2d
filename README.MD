# Run the simulator
```bash
python main.py
```

# Variables
Important variables for the simuation is in config.py.

```pyhton3
# Energy Loss when the ball hits the ground.
ball_energy_loss_ground_collide = 0.7

# Ball decay in air and ground
ball_air_decay = 0.94

# Gravity accel that is applied on ball when it is on the air.
gravity = Vector(0, -0.2)

# Ball size
ball_size = 0.085

# Player size
player_size = 0.3

# Player height
player_height = 1.8

# Epsilon number for some equations.
epsilon = 1.0e-10
```