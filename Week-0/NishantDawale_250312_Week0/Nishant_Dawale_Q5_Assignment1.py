import gymnasium as gym

# Initialise the environment
env = gym.make("LunarLander-v3", render_mode="human")

# Initialise the environment
observation, info = env.reset()
# initialize variables from the first observation
x_vel = observation[2]
y_vel = observation[3]
angle = observation[4]
print("Initial Observation:", observation)
run = True
total_reward = 0
while run:
    # Lateral control (try to reduce horizontal displacement/velocity)
    if x_vel < -0.03:
        action = 3  # Fire right engine to move right
    elif x_vel > 0.03:
        action = 1  # Fire left engine to move left

    # Vertical control (main engine) gives it priority if descending too fast or too low
    if y_vel < -0.3:
        action = 2

    # Small correction for angle: if tilted strongly, use side engines to counteract
    if abs(angle) > 0.2:
        if angle > 0:
            action = 3  # tilt right -> fire right engine to correct
        else:
            action = 1  # tilt left -> fire left engine to correct

    # step (transition) through the environment with the action
    observation, reward, terminated, truncated, info = env.step(action)

    # update state variables for next decision
    x_vel = observation[2]
    y_vel = observation[3]
    angle = observation[4]

    total_reward += reward

    # If the episode has ended then we can reset to start a new episode
    if terminated or truncated:
        observation, info = env.reset()
        run = False

print("Total Reward:", total_reward)
env.close()
