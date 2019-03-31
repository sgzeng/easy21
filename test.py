from Environment import *

if __name__ == "__main__":
    showDisplay = True
    player = Player("Bob", showDisplay)
    dealer = Dealer("Alice", showDisplay)
    arena = Arena(showDisplay)
    arena.playOnetimeGame(player, dealer)
