# -*- coding: utf-8 -*-
import json
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# 現在時刻から200日分のdatetimeインデックスを作成
with open("disorder.mjson", 'r') as f:
    json_dict = {i: json.loads(line) for i, line in enumerate(f)}


score = json_dict[1]["mobidb_consensus"]["disorder"]["predictors"][1]["scores"]
x_range = np.arange(0, len(score), 1)
y_range = np.arange(0, 1, 0.1)

plt.plot(score, color='black', linestyle='solid', alpha=0.5)

for i in range(len(x_range)):
    if score[i] > 0.5:
        plt.scatter(i, score[i], marker='.', c="red")
    else:
        plt.scatter(i, score[i], marker='.', c="blue")



plt.title('Score-Plot Test', fontsize = 20)
plt.xlabel('score', fontsize = 16)
plt.ylabel('array number', fontsize = 16)
plt.grid(True)
plt.show()