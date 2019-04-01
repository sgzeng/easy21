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
        return dealer_first_card_value, playerPoints, self.b_aceNum, self.r_aceNum

    def naivePolicy(self):
        if self.calculatePoints() >= 17:
            return Action.stick
        else:
            return Action.hit
