import traci
from sumolib import checkBinary
import matplotlib.pyplot as plt
import numpy as np

sumoBinary = checkBinary('sumo')
trajectory = []
traci.start([sumoBinary, '-c', 'simulation.sumocfg'])
density = np.zeros(3600, )
velocity = np.zeros(3600, )
occupancy = np.zeros(3600, )
for i in range(3600):
    traci.trafficlight.setPhase('gneJ20', 0)
    traci.simulation.step()
    density[i, ] = traci.edge.getLastStepVehicleNumber('lane10_2') / 160 * 1000 / 5
    velocity[i, ] = traci.edge.getLastStepMeanSpeed('lane10_2') * 3.6
    occupancy[i, ] = traci.edge.getLastStepOccupancy('lane10_2')
volume = np.multiply(density, velocity)
coef = np.polyfit(density, volume, 2)
traci.close()
volume_fit = np.polyval(coef, density)
plt.scatter(density, volume, s=5, c='#9DC3E7')
plt.plot(density, volume_fit, color='#D76364', linewidth=3)
plt.xlabel('密度/(veh/km/ln)', fontproperties='simsun', size=16)
plt.ylabel('流率/(veh/h/ln)', fontproperties='simsun', size=16)
plt.xlim([0, 55])
plt.ylim([0, 2400])
plt.xticks([0, 10, 20, 30, 40, 50], fontproperties = 'Times New Roman', size=12)
plt.yticks([0, 400, 800, 1200, 1600, 2000, 2400], fontproperties = 'Times New Roman', size=12)
plt.grid(color='#A9B8C6', linestyle=':')
plt.show()