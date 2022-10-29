import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import scipy.signal as sps

gme_info = yf.Ticker('GME')

gme_df_2y = gme_info.history(period='2y',
                               interval='1h',
                               actions=False)

gme_df_1y = gme_info.history(period='1y',
                               interval='1h',
                               actions=False)
gme_2y = gme_df_2y['Open'].values
time = np.linspace(0, 1, len(gme_2y))

# find peaks and proiminces 
peak_idx, _ = sps.find_peaks(gme_2y)
prom = sps.peak_prominences(gme_2y, peak_idx)
peak_dom = np.array([time[int(i)] for i in peak_idx])
peak_val = np.array([gme_2y[int(i)] for i in peak_idx])

# worthy peaks
peak_pair = np.array([[pid, pp, pd, pv]
                      for pid, pp, pd, pv in zip(peak_idx, prom[0], peak_dom, peak_val)])
peak_pair = peak_pair[peak_pair[:, 1].argsort()[::-1]]

worthy_peak_pair = peak_pair[:10][peak_pair[:10][:,0].argsort()]
worthy_peak_pair = np.delete(worthy_peak_pair, [0, 2, 3, 5], axis=0)

plt.plot(time[int(.6 * len(gme_2y)) : ], gme_2y[int(.6 * len(gme_2y)) : ])
plt.scatter(worthy_peak_pair[:,2][-2:], worthy_peak_pair[:,3][-2:], marker='x', c='red')
plt.show()
