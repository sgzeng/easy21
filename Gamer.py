class Gamer(object):

    def __init__(self, name="", display=False):
        self.name = name
        self.cards = []
        self.showDisplay = display
        self.b_aceNum = 0
        self.r_aceNum = 0
        self.learningMethod = None
        self.policy = None
        self.role = None

    def __str__(self):
        return self.name

    def _cardValue(self, card) -> int:
        assert isinstance(card, tuple) and len(card) == 2
        value = 0
        try:
            value = int(card[0])
        except Exception as e:
            if card[0] == 'A' and card[1]:
                value = 11
            elif card[0] == 'A' and not card[1]:
                value = 1
            elif card[0] in ['J', 'Q', 'K']:
                value = 10
            else:
                # this should not happen
                print(e)
        finally:
            # black: True red: False
            assert value > 0
            if not card[1]:
                value = -value
            return value

    def calculatePoints(self) -> int:
        points = 0
        for card in self.cards:
            points += self._cardValue(card)
        return points

    def calculateFinalPoints(self):
        points = 0
        assert self.r_aceNum * self.b_aceNum >= 0
        for card in self.cards:
            points += self._cardValue(card)
        aceNum = self.r_aceNum + self.b_aceNum
        if points > 21 and aceNum > 0:
            while points > 21:
                aceNum -= 1
                points -= 10
                if aceNum <= 0:
                    break
        return points

    def receive(self, cards=()):
        for card in cards:
            assert isinstance(card, tuple) and len(card) == 2
            if card[0] == 'A' and card[1]:
                self.b_aceNum += 1
            elif card[0] == 'A' and not card[1]:
                self.r_aceNum += 1
            self.cards.append(card)

    def dischargeCards(self):
        self.cards.clear()
        self.b_aceNum = 0
        self.r_aceNum = 0

    def showInfo(self):
        self._info("<%s> is %s now holding: %s" % (self.role.value, self, self.cards))

    def _info(self, msg, show=False):
        assert isinstance(msg, str) and len(msg) > 0
        if (self.showDisplay or show) and msg is not None:
            print(msg)
