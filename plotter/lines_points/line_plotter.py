import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv('input.csv')

#df.plot.line(x='Distance from the chip (cm)',y='RSS (dB)', grid=True, title = 'Flat slider (32cm)',linestyle='--', marker='o')
#'Tag 1 (Half length)','Tag 2 (Half length)'
#plt.ylim((-70,-35))
x = np.arange(0,2*np.pi,0.1)   # start,stop,step
y = np.cos(x)

plt.plot(x,y)
plt.grid(True)
plt.show()