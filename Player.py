from MetaData import *
from Gamer import *


class Player(Gamer):

    def __init__(self, name="", display=False):
        super(Player, self).__init__(name, display)
        self.role = Role.player
        self.policy = self.naivePolicy

    def getState(self, dealer):
        dealer_first_card_value = dealer.show_firstCard()
        playerPoints = self.calculatePoints()
        return State(dealer_first_card_value, playerPoints, self.b_aceNum, self.r_aceNum)

    def step(self, state, action, env):
        if action == Action.stick:
            return state
        elif action == Action.hit:
            env.dealCards(self, 1)
            return State(state.dealer_first_card_value, self.calculatePoints(), self.b_aceNum, self.r_aceNum)
        else:
            # error state
            return 0, 0, 0, 0

    def naivePolicy(self):
        if self.calculatePoints() >= 17:
            return Action.stick
        else:
            return Action.hit


class State:

    def __init__(self, d_f_c_v, p_P, b_a_N, r_a_N):
        self.dealer_first_card_value = d_f_c_v
        self.playerPoints = p_P
        self.b_aceNum = b_a_N
        self.r_aceNum = r_a_N

    def getRawState(self):
        return self.dealer_first_card_value, self.playerPoints, self.b_aceNum, self.r_aceNum
