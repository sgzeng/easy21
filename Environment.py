from random import shuffle
from queue import Queue
from MetaData import *
from Player import *
from Dealer import *
from tqdm import tqdm
import math
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


class Arena(object):

    blackCards = [('A', True),
                  ('2', True),
                  ('3', True),
                  ('4', True),
                  ('5', True),
                  ('6', True),
                  ('7', True),
                  ('8', True),
                  ('9', True),
                  ('10', True),
                  ('J', True),
                  ('Q', True),
                  ("K", True)
                  ] * 3
    redCards = [('A', False),
                ('2', False),
                ('3', False),
                ('4', False),
                ('5', False),
                ('6', False),
                ('7', False),
                ('8', False),
                ('9', False),
                ('10', False),
                ('J', False),
                ('Q', False),
                ("K", False)
                ] * 1

    def __init__(self, display=False):
        self.showDisplay = display
        # black: True red: False
        self.cardBase = Arena.blackCards + Arena.redCards
        self.__cardQ = Queue(maxsize=52)
        self._cardsUsed = []
        self.episodes = []

    def _loadCards(self, cards):
        shuffle(cards)
        for card in cards:
            self.__cardQ.put(card)

    def dealCards(self, gamer, num):
        cards = []
        for _ in range(0, num):
            if not self.__cardQ.empty():
                cards.append(self.__cardQ.get())
            else:
                self._info("There is no card in queue anymore, reloading...")
                shuffle(self._cardsUsed)
                self._loadCards(self._cardsUsed)
                assert self.__cardQ.qsize() >= 50
                self._cardsUsed.clear()
        self._cardsUsed.extend(cards)
        gamer.receive(cards)
        # self._info("Croupier deal %d cards %s to %s " % (num, cards, gamer))

    def _judgeReward(self, player, dealer):
        '''
        If the dealer goes bust, then the player wins; otherwise,
        the outcome – win (reward +1),
        lose (reward -1), or draw (reward 0) – is the player with the largest sum.
        '''
        playerPoints = player.calculateFinalPoints()
        dealerPoints = dealer.calculateFinalPoints()
        playerIsBusted = (playerPoints > 21) or (playerPoints < 1)
        dealerIsBusted = (dealerPoints > 21) or (dealerPoints < 1)
        if (playerIsBusted and dealerIsBusted) or playerPoints == dealerPoints:
            self._info("<Player> %s points: %d \n<Dealer> %s points: %d"
                       % (player, playerPoints, dealer, dealerPoints))
            self._info("Game draw!")
            return 0
        if playerIsBusted and not dealerIsBusted:
            self._info("<Player> %s points: %d \n<Dealer> %s points: %d"
                       % (player, playerPoints, dealer, dealerPoints))
            self._info("<Player> %s is busted and lose!" % player)
            return -1
        if dealerIsBusted and not playerIsBusted:
            self._info("<Player> %s points: %d \n<Dealer> %s points: %d"
                       % (player, playerPoints, dealer, dealerPoints))
            self._info("<Dealer> %s is busted and <Player> %s win!" % (dealer, player))
            return 1
        if playerPoints > dealerPoints:
            self._info("<Player> %s points: %d \n<Dealer> %s points: %d"
                       % (player, playerPoints, dealer, dealerPoints))
            self._info("<Player> %s win!" % player)
            return 1
        self._info("<Player> %s points: %d \n<Dealer> %s points: %d"
                   % (player, playerPoints, dealer, dealerPoints))
        self._info("<Player> %s lose!" % player)
        return -1

    def cleanArena(self, player, dealer):
        player.dischargeCards()
        dealer.dischargeCards()
        self._cardsUsed.clear()
        self.__cardQ.queue.clear()
        self._loadCards(self.cardBase)

    def playOnetimeGame(self, player, dealer):
        assert player.role == Role.player
        assert dealer.role == Role.dealer
        episode = []
        if player.policy is None:
            self._info("<Player> %s needs a policy" % player)
            return
        if dealer.policy is None:
            self._info("<Dealer> %s needs a policy" % dealer)
            return
        # At the start of the game both the player and the dealer
        # draw one black card (fully observed)
        # black: True; red: False
        self.cleanArena(player, dealer)
        while True:
            self.dealCards(dealer, 1)
            self.dealCards(player, 1)
            if player.cards[0][1] and dealer.cards[0][1]:
                break
            self.recycleGamerCard(dealer, player)
        # Dealer's turn
        while True:
            dealerAction = dealer.policy()
            if dealerAction == Action.hit:
                self.dealCards(dealer, 1)
            if dealerAction == Action.stick:
                break
            dealerPoints = dealer.calculateFinalPoints()
            dealerIsBusted = (dealerPoints > 100) or (dealerPoints < -100)
            if dealerIsBusted:
                break
        # Player's turn
        while True:
            state = player.getState(dealer)
            episode.append(state)
            playerAction = player.policy()
            # if playerAction == Action.hit:
            #     self.dealCards(player, 1)
            player.step(state, playerAction, self)
            # Terminate state
            if playerAction == Action.stick:
                break
            playerPoints = player.calculateFinalPoints()
            playerIsBusted = (playerPoints > 100 or playerPoints < -100)
            if playerIsBusted:
                break
        player.showInfo()
        dealer.showInfo()
        return self._judgeReward(player, dealer), episode

    def recycleGamerCard(self, *gamers):
        if len(gamers) == 0:
            return
        for gamer in gamers:
            self._cardsUsed.extend(gamer.cards)
            gamer.dischargeCards()

    def startMultiGame(self, player, dealer, roundNum, showStatistic=False):
        results = [0, 0, 0] # player wins rounds, dealer wins rounds, draw rounds
        self.episodes.clear()
        for i in tqdm(range(1, roundNum+1)):
            self._info("\n************* Round %d started *************" % i)
            reward, episode = self.playOnetimeGame(player, dealer)
            self.episodes.append(episode)
            if reward > 0:
                results[0] += 1
            elif reward < 0:
                results[1] += 1
            else:
                results[2] += 1
        if showStatistic:
            print("Easy21 played %d rounds in total, draw in %d rounds. \n "
                  "<Player> %s wins %d rounds, <Dealer> %s wins %d rounds\n"
                  "Win rate: %.2f \nLose rate: %.2f"
                  % (i, results[2], player, results[0], dealer, results[1], results[0]/roundNum, results[1]/roundNum))

    def _info(self, msg, show=False):
        assert isinstance(msg, str) and len(msg) > 0
        if self.showDisplay or show:
            print(msg)
