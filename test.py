from Environment import *
import utils

if __name__ == "__main__":
    showDisplay = False
    bob = MCPlayer("Bob", showDisplay)
    alice = Dealer("Alice", showDisplay)
    arena = Arena(showDisplay)
    arena.startMultiGame(bob, alice, 10000, True)
    # stateValue = utils.evaluatePolicy(arena.episodes)
    # utils.drawValueFunction(stateValue, False)
