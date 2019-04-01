import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


def evaluatePolicy(episodes, stateValue=None, stateCounter=None):
    '''
    Evalute a policy at given state using incremental Monte Carlo
    Discounted factor: 1
    And mid state reward is 0
    '''
    if not stateValue:
        stateValue = {}
    if not stateCounter:
        stateCounter = {}
    for episode, reward in episodes:
        for state, action in episode:
            stateName  = str(state.dealer_first_card_value) + "_" + str(state.playerPoints) \
                         + "_" + str(state.b_aceNum + state.r_aceNum)
            if stateName not in stateCounter.keys():
                stateCounter[stateName] = 0
            stateCounter[stateName] = stateCounter.get(stateName, 0) + 1
            if stateName not in stateValue.keys():
                stateValue[stateName] = 0
            goal_t = reward
            stateValue[stateName] = stateValue.get(stateName, 0) + (goal_t - stateValue.get(stateName, 0))/stateCounter[stateName]
    return stateValue


def drawValueFunction(stateValue, haveAce = True):
    assert isinstance(stateValue, dict)
    valueDic = {}
    for state, value in stateValue.items():
        statelist = state.split('_')
        if statelist[-1] != '0' and not haveAce:
            continue
        newStateName = statelist[0] + '_' + statelist[1]
        if value > valueDic.get(newStateName, 0):
            valueDic[newStateName] = value
    fig = plt.figure()
    ax = Axes3D(fig)
    x = np.arange(1, 11, 1)
    y = np.arange(1, 30, 1)
    X, Y = np.meshgrid(x, y)
    row, col = X.shape
    Z = np.zeros((row, col))
    for i in range(row):
        for j in range(col):
            Z[i, j] = valueDic.get(str(i) + "_" + str(j), 0)
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, color="lightgray")
    plt.show()
