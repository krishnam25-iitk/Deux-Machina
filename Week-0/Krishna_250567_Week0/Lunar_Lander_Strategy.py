import gymnasium as gym
# from gymnasium.wrappers import RecordVideo

# Initialise the environment
env = gym.make("LunarLander-v3", render_mode="human")
# env = RecordVideo(env, "./videos/")

# Get the first observation -> Initial State
observation, info = env.reset()
# Here observation is the current state of the environment (i.e, the position and velocity of the lander)
# observation is a numpy array of 8 floats representing the x coordinate, y coordinate, x velocity, y velocity, lander angle, angular velocity, left leg contact, right leg contact
# You can use a subset of these values to create your own strategy for landing the lunar lander.
# For example, I am using the x coordinate and y coordinate to create a simple strategy.

x_coord = observation[0]
y_coord = observation[1]
x_vel = observation[2]
y_vel = observation[3]
rot_in_deg = (observation[4]*180)/3.1416
ang_vel = (observation[5]*180)/3.1416

# action = 0 -- No action
# action = 1 -- Tilt Left
# action = 2 -- Fire Main Engine
# action = 3 -- Tilt Right

print("Initial Observation:", observation)
run = True
total_reward = 0
while(run):

    # For Checking the instantaneous Readings:
    # print("ang = ", rot_in_deg,", ang_vel =", ang_vel, ",x_vel = ", x_vel, ",y_vel = ", y_vel)
    
    # MY STRATEGY:

    # To make the fall Slow (without desturbing the x_vel)
    if (rot_in_deg>-3 and rot_in_deg<3) and (y_vel<-0.15):
        action = 2
    # To stop the lander going to high
    elif y_vel > 0.15: # Maintaining Y_vel
        action = 0 
    # Making Rotations Smooth 
    elif ang_vel>15:
        action = 3 
    elif ang_vel<-15:
        action = 1 
    # To Reduce Max Tilt of the Lander (Making Motions Smooth)
    elif rot_in_deg > 10:
        action = 3 
    elif  rot_in_deg < -10:
        action = 1 
    # Maintaing Max Decending Velocity
    elif y_vel < -0.4: 
        action = 2
    # Slowing down the motion in x
    elif x_vel > 0.2:
        if rot_in_deg < 3:
            action = 1 
        elif rot_in_deg > 10: 
            action = 3
        else: action = 2
    elif x_vel < -0.2:
        if rot_in_deg > -3:
            action = 3  
        elif rot_in_deg < -10:
            action = 1 
        else: action = 2
    # Moving Lander to the Landing Region
    elif x_coord > 0.1:
        if rot_in_deg < 3:
            action = 1
        elif rot_in_deg > 10: 
            action = 3
        else: action = 2 
    elif x_coord < -0.1:
        if rot_in_deg > -3:
            action = 3 
        elif rot_in_deg < -10:
            action = 1 
        else: action = 2
    # For Soft Landing
    elif y_vel < -0.075 and y_coord < 0.4: 
        action = 2
    #For Slowing motion in -y
    elif y_vel < -0.2: 
        action = 2
    # For Remaining Cases
    else: 
        action = 0 

    # step (transition) through the environment with the action
    # receiving the next observation, reward and if the episode has terminated or truncated
    observation, reward, terminated, truncated, info = env.step(action)
    
    x_coord = observation[0]
    y_coord = observation[1]
    x_vel = observation[2]
    y_vel = observation[3]
    rot_in_deg = (observation[4]*180)/3.1416
    ang_vel = (observation[5]*180)/3.1416

    total_reward += reward
    # If the episode has ended then we can reset to start a new episode
    if terminated or truncated:
        observation, info = env.reset()
        run = False
    if y_coord>5: run = False

print("Total Reward:", total_reward)
env.close()
