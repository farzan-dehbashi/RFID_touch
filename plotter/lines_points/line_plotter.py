import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv('input.csv')
df.plot.line(x='Distance from the chip (cm)',y='RSS (dB)', grid=True, title = 'Sliding antenna on a full wave-length bended transmission line',linestyle='--', marker='o')
#'Tag 1 (Half length)','Tag 2 (Half length)'
plt.ylim((-70,-35))

plt.grid(True)
plt.show()