from Gamer import *
from MetaData import *

class Dealer(Gamer):

    def __init__(self, name="Dealer", display=False ):
        super(Dealer, self).__init__(name, display)
        self.role = Role.dealer
        self.policy = self.dealerPolicy

    def show_firstCard(self) -> int:
        if self.cards is None or len(self.cards) == 0:
            return 0
        return self._cardValue(self.cards[0])

    def dealerPolicy(self):
        if self.calculatePoints() >= 17:
            return Action.stick
        else:
            return Action.hit
