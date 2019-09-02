# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 17:48:01 2019

@author: Ibrainscn
"""

import random

##############################################################################
## roll dice game:
def rollDice():
    roll = random.randint(1,100)
    if roll == 100:
        print(roll,'roll was 100, you lose. What are the odds?! Play again!')
        return False
    elif roll <=50:
        print(roll,'roll was 1-50, you lose. Play again!')
        return False
    elif 50 < roll < 100:
        print(roll, 'roll was 51-100, you win! Play more!')
        return True
    
    
def simple_bettor(funds, initial_wager, wager_count):
    value = funds
    wager = initial_wager
    currentWager = 0
    
    while currentWager < wager_count:
        if rollDice():
            value += wager
        else:
            value -= wager
            
        currentWager += 1
        print('Funds:', value)
    
simple_bettor(10000, 100, 100)

##############################################################################
## Roulette game:
class FairRoulette():
    def __init__(self):
        self.pockets = []
        for i in range(1,37):
            self.pockets.append(i)
        self.pocketOdds = len(self.pockets) - 1
        
    def spin(self):
        self.ball = random.choice(self.pockets)
        
    def betPocket(self, pocket, amt):
        if str(pocket) == str(self.ball):
            return amt*self.pocketOdds
        else:
            return -amt
        
    def __str__(self):
        return 'Fair Roulette'
    
def playRoulette(game, numSpins, pocket, bet, toPrint):
    totpocket = 0
    for i in range(numSpins):
        game.spin()
        totpocket += game.betPocket(pocket, bet)
    if toPrint:
        print(numSpins, 'spins of', game)
        print('Expected return betting', pocket, '=', str(100*totpocket/numSpins) + '%\n')
    return (totpocket/numSpins)
    
random.seed(0)
game = FairRoulette()
for numSpins in (100,1000000):
    for i in range(3):
        playRoulette(game, numSpins, 2, 1, True)
    
#############################################################################
## Two Subclasses of Roulette game:
class EuRoulette(FairRoulette):
    def __init__(self):
        FairRoulette.__init__(self)
        self.pockets.append('0')
    def __str__(self):
        return 'European Roulette'
    
class AmRoulette(EuRoulette):
    def __init__(self):
        EuRoulette.__init__(self)
        self.pockets.append('00')
    def __str__(self):
        return 'American Roulette'
    
random.seed(0)
game1 = FairRoulette()
game2 = EuRoulette()
game3 = AmRoulette()

for numSpins in (100, 100000):
    for i in range(3):
        playRoulette(game1, numSpins, 2, 1, True)
        playRoulette(game2, numSpins, 2, 1, True)
        playRoulette(game3, numSpins, 2, 1, True)

#############################################################################
## Applying Empirical Rule to Roulette game:
def findPocketReturn(game, numTrials, trialSize, toPrint):
    pocketReturns = []
    for t in range(numTrials):
        trialVals = playRoulette(game, trialSize, 2, 1, toPrint)
        pocketReturns.append(trialVals)
    return pocketReturns

def getMeanAndStd(X):
    mean = sum(X)/float(len(X))
    tot = 0.0
    for x in X:
        tot += (x - mean)**2
    std = (tot/len(X))**0.5
    return mean, std

random.seed(0)
numTrials = 20
resultDict = {}
games = (FairRoulette, EuRoulette, AmRoulette)
for G in games:
    resultDict[G().__str__()] = []
for numSpins in (100, 1000, 10000, 100000):
    print('\nSimulate', numTrials, 'trials of',
          numSpins, 'spins each')
    for G in games:
        pocketReturns = findPocketReturn(G(), numTrials,
                                         numSpins, False)
#        expReturn = 100*sum(pocketReturns)/len(pocketReturns)
#        print('Exp. return for', G(), '=',
#             str(round(expReturn, 4)) + '%')
        
        mean, std = getMeanAndStd(pocketReturns)
        resultDict[G().__str__()].append((numSpins, 100*mean, 100*std))
        print('Exp. return for', G(), '=', str(round(100*mean, 3))
              + '%,', '+/-', str(round(100*1.96*std,3)) 
              + '% with 95% confidence')
             
