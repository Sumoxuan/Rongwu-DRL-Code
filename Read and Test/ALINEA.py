import gym
import traci
import numpy as np
import pandas as pd

def ALINEA(BN_density, cri_density, ramp_flow, Kr_ramp, ramp_capacity, cycle, demand, queue_length, max_length):

    ramp_flow_new = ramp_flow + Kr_ramp * (cri_density - BN_density)
    ramp_flow_queue = -1 / (cycle / 3600) * (max_length - queue_length) + demand / 20 * 3600
    flow = min(max(ramp_flow_new, ramp_flow_queue), ramp_capacity)

    new_green = max(2, int(cycle * (flow / ramp_capacity)))
    red_time = cycle - new_green

    return flow, red_time

def run():
    env = gym.make('RampControl-v0').unwrapped
    action_set = [0]
    ramp_flow = 1800
    state = env.reset()
    for i in range(179):
        occupancy = traci.edge.getLastStepOccupancy('lane10_2') * 100
        demand = state[3]
        queue_length = state[-1]
        ramp_flow, red_time = ALINEA(occupancy, 15, ramp_flow, 70, 1800, 20, demand, queue_length, 120)
        action_set.append(red_time)
        next_state, reward, done, info = env.step(red_time)
        state = next_state
    traci.close()
    action_set = np.array(action_set)
    np.save('Action Set_ALINEA.npy', action_set)
    data = pd.DataFrame(env.trajectory)
    data.to_csv('Trajectory_ALINEA.csv', index=False, header=False)

    return 0

if __name__ == '__main__':
    run()