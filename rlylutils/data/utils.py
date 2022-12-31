from itertools import combinations, permutations

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
