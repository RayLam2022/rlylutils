import os
import sys
from itertools import combinations, permutations

from importlib import import_module

try:
    matplotlib = import_module('matplotlib')
except:
    os.system(f'{sys.executable} -m pip install matplotlib')
    matplotlib = import_module('matplotlib')

try:
    sklearn = import_module('sklearn')
except:
    os.system(f'{sys.executable} -m pip install scikit-learn')
    sklearn = import_module('sklearn')

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score


def permut(choice_list: list, pick_num: int):
    """
    排列数生成器
    :param choice_list:
    :param pick_num:
    :return:
    """
    return permutations(choice_list, pick_num)


def combin(choice_list: list, pick_num: int):
    """
    组合数生成器
    :param choice_list:
    :param pick_num:
    :return:
    """
    return combinations(choice_list, pick_num)


def ROC(y_test, y_pred):
    fpr, tpr, tr = roc_curve(y_test, y_pred)
    auc = roc_auc_score(y_test, y_pred)
    idx = np.argwhere(np.diff(np.sign(tpr - (1 - fpr)))).flatten()

    plt.xlabel("FPR")
    plt.ylabel("TPR")
    plt.plot(fpr, tpr, label="AUC=" + str(auc))
    plt.plot(fpr, 1 - fpr, 'r:')
    plt.plot(fpr[idx], tpr[idx], 'ro')
    plt.legend(loc=4)
    plt.grid()
    plt.show()
    return tr[idx]


if __name__ == '__main__':
    l = [3, 6, 7]
    x = combin(l, 2)
    for i in x:
        print(i)
