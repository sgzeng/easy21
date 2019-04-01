from Environment import *
import math


class MCPlayer(Player):

    def __init__(self, name="", display=False):
        super(MCPlayer, self).__init__(name, display)
        self.stateValue = {}
        self.stateCounter = {}
        self.learningTimes = 0
        self.policy = self.epsilonGreedyPolicy
        self.learnEnv = self.learnQ

    def learnQ(self, episode, reward):
        for state, action in episode:
            stateName = str(state.dealer_first_card_value) + "_" + str(state.playerPoints) \
                        + "_" + str(state.b_aceNum + state.r_aceNum) + "_" + action.value
            if stateName not in self.stateCounter.keys():
                self.stateCounter[stateName] = 0
            self.stateCounter[stateName] = self.stateCounter.get(stateName, 0) + 1
            if stateName not in self.stateValue.keys():
                self.stateValue[stateName] = 0
            goal_t = reward
            self.stateValue[stateName] = self.stateValue.get(stateName, 0) + (goal_t - self.stateValue.get(stateName, 0))/self.stateCounter[stateName]
        self.learningTimes += 1

    def resetMem(self):
        self.stateValue.clear()
        self.stateCounter.clear()
        self.learningTimes = 0

    def epsilonGreedyPolicy(self, state, epsilon=None):
        playerPoints = self.calculatePoints()
        if playerPoints >= 21:
            return Action.stick
        if playerPoints < 12:
            return Action.hit
        else:
            s = str(state.dealer_first_card_value) + "_" + str(state.playerPoints) \
                + "_" + str(state.b_aceNum + state.r_aceNum)
            Q = self.stateValue
            if epsilon is None:
                epsilon = 1.0 / (1 + 4 * math.log10(1 + self.learningTimes))
            hitV = stickV = 0
            for stateName, value in Q.items():
                stateNameList = stateName.rpartition('_')
                if s == stateNameList[0] and stateNameList[1] == "hit":
                    hitV = value
                elif s == stateNameList[0] and stateNameList[1] == "stick":
                    stickV = value
                else:
                    hitV = stickV = 0
            if hitV > stickV:
                return Action.hit
            elif hitV < stickV:
                return Action.stick
            else:
                return Action.hit