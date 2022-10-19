import traci
from sumolib import checkBinary
import pandas as pd
import numpy as np

def parameter_detection(occupancy1, occupancy2, ave_speed1, ave_speed2, throughout_flow, throughout_id, queue_length,
                        feature, detecting_interval):
    time = traci.simulation.getTime()
    occupancy1 += traci.edge.getLastStepOccupancy('lane10_2')
    occupancy2 += traci.edge.getLastStepOccupancy('lane12')
    ave_speed1 += traci.edge.getLastStepMeanSpeed('lane10_2') * 3.6
    ave_speed2 += traci.edge.getLastStepMeanSpeed('lane12') * 3.6
    throughout_flow, throughout_id = get_throughout_flow(throughout_flow, throughout_id)
    queue_length += get_queue_num()

    if time % detecting_interval == 0:
        occupancy1 = occupancy1 / detecting_interval
        occupancy2 = occupancy2 / detecting_interval
        ave_speed1 = ave_speed1 / detecting_interval
        ave_speed2 = ave_speed2 / detecting_interval
        queue_length = queue_length / detecting_interval
        data = [time, occupancy1, occupancy2, ave_speed1, ave_speed2, throughout_flow, queue_length]
        # 时间、瓶颈区占有率、下游路段占有率、瓶颈区平均车速、下游路段平均车速、下游通过量、匝道排队长度
        feature.append(data)
        occupancy1 = 0
        occupancy2 = 0
        ave_speed1 = 0
        ave_speed2 = 0
        throughout_flow = 0
        throughout_id = ()
        queue_length = 0

    return occupancy1, occupancy2, ave_speed1, ave_speed2, throughout_flow, throughout_id, queue_length, feature


def get_throughout_flow(throughout=0, veh_id=()):
    id_in_detector = traci.inductionloop.getLastStepVehicleIDs('e1Detector_lane12_3_44') + \
                     traci.inductionloop.getLastStepVehicleIDs('e1Detector_lane12_2_45') + \
                     traci.inductionloop.getLastStepVehicleIDs('e1Detector_lane12_1_46') + \
                     traci.inductionloop.getLastStepVehicleIDs('e1Detector_lane12_0_47')
    new_n_detector = list(set(id_in_detector) - set(veh_id))
    throughout = throughout + len(new_n_detector)

    return throughout, id_in_detector

def get_queue_num():
    queue_num = 0
    vehicles_on_ramp = traci.edge.getLastStepVehicleIDs('lane15_1') +\
                       traci.edge.getLastStepVehicleIDs('lane16') +\
                       traci.edge.getLastStepVehicleIDs(':genJ18_0')
    for id in vehicles_on_ramp:
        if traci.vehicle.getSpeed(id) < 3:
                queue_num += 1
    return queue_num

if __name__ == '__main__':
    # redtime_set = np.load('Action Set.npy')
    redtime_set = np.load('Action Set_ALINEA.npy')
    # redtime_set = np.zeros([270,], dtype=np.int32)

    detecting_interval = 20
    feature = []
    occupancy1 = 0
    occupancy2 = 0
    ave_speed1 = 0
    ave_speed2 = 0
    throughout_flow = 0
    throughout_id = ()
    queue_length = 0

    sumoBinary = checkBinary('sumo')
    traci.start([sumoBinary, '-c', 'simulation.sumocfg', '--statistic-output', 'output.xml', '--duration-log.statistics'])
    for i in range(180):
        redtime = redtime_set[i]
        for j in range(20 - redtime):
            traci.trafficlight.setPhase('gneJ20', 0)
            traci.simulation.step()
            occupancy1, occupancy2, ave_speed1, ave_speed2, throughout_flow, throughout_id, queue_length, feature = \
                parameter_detection(occupancy1, occupancy2, ave_speed1, ave_speed2, throughout_flow, throughout_id,
                                    queue_length,
                                    feature, detecting_interval)
        for j in range(redtime):
            traci.trafficlight.setPhase('gneJ20', 1)
            traci.simulation.step()
            occupancy1, occupancy2, ave_speed1, ave_speed2, throughout_flow, throughout_id, queue_length, feature = \
                parameter_detection(occupancy1, occupancy2, ave_speed1, ave_speed2, throughout_flow, throughout_id,
                                    queue_length,
                                    feature, detecting_interval)

    traci.close()
    Feature = pd.DataFrame(feature)
    # Feature.to_csv('Overall Feature_TD3.csv', header=False, index=False)
    Feature.to_csv('Overall Feature_ALINEA.csv', header=False, index=False)
    # Feature.to_csv('Overall Feature_no_control.csv', header=False, index=False)
