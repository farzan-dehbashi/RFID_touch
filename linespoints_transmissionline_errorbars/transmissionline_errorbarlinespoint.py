import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('in.csv')
fig, axs = plt.subplots(2)
axs = df.plot(x='location',y='tag4', rot=0, label='Tag2', color='m')

axs.set_title('RSSI of chips in a full length transmission line')


plt.xticks([0,5,10,15,20,25,30])
plt.ylim((-75,-35))
plt.show()


