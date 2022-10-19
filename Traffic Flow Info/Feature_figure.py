from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
import pandas as pd

features_no_control = pd.read_csv('Overall Feature_no_control.csv', header=None).values
features_ALINEA = pd.read_csv('Overall Feature_ALINEA.csv', header=None).values
features_TD3_based = pd.read_csv('Overall Feature_TD3.csv', header=None).values
time = features_no_control[:, 0]
occupancy1 = features_no_control[:, 1]
occupancy2 = features_ALINEA[:, 1]
occupancy3 = features_TD3_based[:, 1]

l1, = plt.plot(time, occupancy1, linewidth=2, linestyle=':', color='#54B345')
l2, = plt.plot(time, occupancy2, linewidth=2, linestyle='--', color='#5F97D2')
l3, = plt.plot(time, occupancy3, linewidth=2, color='#D76364')

font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc")
plt.xlabel('时间/(s)', fontproperties=font, size=16)
plt.ylabel('瓶颈路段占有率)', fontproperties=font, size=16)
plt.legend(handles=[l1, l2, l3], labels=['No-control', 'ALINEA', 'TD3-based'], prop={'family': 'Times New Roman', 'size':13})

plt.xlim([0, 3600])
plt.ylim([0, 0.25])
plt.xticks([0, 400, 800, 1200, 1600, 2000, 2400, 2800, 3200, 3600], fontproperties = 'Times New Roman', size=12)
plt.yticks([0, 0.05, 0.10, 0.15, 0.20, 0.25], fontproperties = 'Times New Roman', size=12)
plt.grid(color='#A9B8C6', linestyle=':')
plt.show()