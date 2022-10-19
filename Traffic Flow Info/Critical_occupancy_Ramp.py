import traci
from sumolib import checkBinary
import numpy as np
import matplotlib.pyplot as plt

sumoBinary = checkBinary('sumo')
traci.start([sumoBinary, '-c', 'simulation.sumocfg'])
volume = np.zeros(3600, )
occupancy = np.zeros(3600, )
for i in range(3600):
    traci.trafficlight.setPhase('gneJ20', 0)
    traci.simulation.step()
    density = traci.edge.getLastStepVehicleNumber('lane15_1') / 246 * 1000
    velocity = traci.edge.getLastStepMeanSpeed('lane15_1') * 3.6
    volume[i, ] = density * velocity
    occupancy[i, ] = traci.edge.getLastStepOccupancy('lane15_1')
coef = np.polyfit(occupancy, volume, 2)
traci.close()
volume_fit = np.polyval(coef, occupancy)
plt.scatter(occupancy, volume, s=5, c='#D76364')
plt.xlabel('占有率/(%)', fontproperties='simsun', size=16)
plt.ylabel('流率/(veh/h/ln)', fontproperties='simsun', size=16)
plt.xlim([0, 0.30])
plt.ylim([0, 2000])
plt.xticks([0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30], fontproperties = 'Times New Roman', size=12)
plt.yticks([0, 400, 800, 1200, 1600, 2000], fontproperties = 'Times New Roman', size=12)
plt.grid(color='#A9B8C6', linestyle=':')
plt.show()