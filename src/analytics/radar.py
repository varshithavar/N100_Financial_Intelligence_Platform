import matplotlib.pyplot as plt
import numpy as np


categories=[
"ROE",
"ROCE",
"NPM",
"D/E",
"FCF",
"PAT CAGR",
"Revenue CAGR",
"Score"
]


angles=np.linspace(
0,
2*np.pi,
len(categories),
endpoint=False
)


fig=plt.figure()

ax=plt.subplot(
111,
polar=True
)


ax.plot(
angles,
values
)


ax.fill(
angles,
values,
alpha=.25
)


plt.savefig(
"reports/radar_charts/company_radar.png"
)
