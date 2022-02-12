#!/usr/bin/python3
# coding=UTF-8
# encoding=UTF-8
import json
import os
import hashlib
import datetime

class Block:
    def __init__(self, index, data, previousHash='00000'):
        self.index = index
        self.timestamp = str(datetime.datetime.now())
        self.data = data
        self.previousHash = previousHash
        self.hash = self.calculateHash()

    def update(self, dic):
        self.__dict__=dic
        return self

    def calculateHash(self):
        return hashlib.sha256(str(self.index).encode('utf-8')
        + self.previousHash.encode('utf-8') 
        + str(self.data).encode('utf-8')
        + self.timestamp.encode('utf-8')).hexdigest()
        
    def isValid(self):
        return self.hash == self.calculateHash()

    def printBlock(self):
        return ("\nBlock #" + str(self.index) 
                + "\nData: " + str(self.data)
                + "\nTimeStamp: " + str(self.timestamp)
                + "\nBlock Hash: " + str(self.hash)
                + "\nBlock Previous Hash: " + str(self.previousHash)
                +"\n---------------")

class BlockChain:
    def __init__(self, file="block.chain"):
        self.chain = [Block(0, "Genesis")]
        self.file=file

    def getLatestBlock(self):
        return self.chain[len(self.chain)-1]

    def getNextIndex(self):
        return self.getLatestBlock().index + 1

    def generateBlock(self, team1, team2, winner, score):
        data = {
            "Team1" : team1,
            "Team2" : team2,
            "Winner" : winner,
            "Score" : score,
        }
        self.chain.append(Block(self.getNextIndex(), data, self.getLatestBlock().hash))

    def isChainValid(self):
        for i in range (1, len(self.chain)):
            if not self.chain[i].isValid():
                return False
            if self.chain[i].previousHash != self.chain[i-1].hash:
                return False
        return True

    def printBlockChain(self):
        return ''.join([self.chain[i].printBlock() for i in range(1, len(self.chain))])

    def save(self):
        if(self.isChainValid()):
            with open(self.file, 'w') as f:
                f.write(json.dumps(self, default=lambda obj: obj.__dict__))
        else:
            print("Not saved the chain!")

    def open(self):
        if(os.path.exists(self.file)):
            with open(self.file) as f:
                data = json.load(f)
                self.__dict__ = data 
                self.chain = [Block("","").update(dic) for dic in data["chain"]]

def main():
    blockchain = BlockChain()
    blockchain.generateBlock("BACON TIME","BURIRAM UNITED","BACON TIME","3-0")
    blockchain.generateBlock("EARENA","PSG ESPORT","PSG ESPORT","1-3")
    blockchain.generateBlock("KOG DIAMOND COBRA","TALON","TALON","2-3")
    blockchain.generateBlock("PSG ESPORT","EVOS ESPORTS","PSG ESPORT","3-2")
    blockchain.generateBlock("GOLDCITY ESPORTS","TALON","GOLDCITY ESPORTS","3-1")
    blockchain.generateBlock("BAZAAR GAMING","KING OF GAMERS CLUB","KING OF GAMERS CLUB","0-3")
    blockchain.generateBlock("BACON TIME","GOLDCITY ESPORTS","BACON TIME","3-2")
    blockchain.generateBlock("EVOS ESPORTS","TALON","TALON","3-0")
    blockchain.generateBlock("BURIRAM UNITED","PSG ESPORT","PSG ESPORT","1-3")
    blockchain.generateBlock("KOG DIAMOND COBRA","EARENA","EARENA","0-3")
    
    while(True) :
        chk = input("Do you want to create new block? (y/n) : ")
        if(chk == 'y') :
            team1 = input("Team1 : ")
            team2 = input("Team2 : ")
            print('If ',team1,' win Press 1')
            print('If ',team2,' win Press 2')
    
            while(True) :
                winner = str(input("Winner : "))
                if(winner == '1') :
                    winner = team1
                    break
                elif(winner == '2') :
                    winner = team2
                    break
            print("Score Team",team1) ; score1 = int(input("Score Team1 : "))
            print("Score Team",team2) ; score2 = int(input("Score Team2 : "))
            score = str(score1)+'-'+str(score2)
            blockchain.generateBlock(team1, team2, winner, score)
            break
        elif(chk=='n') :
            break
        
        else :
            print("Please insert y or n !")
            
        
    print(blockchain.printBlockChain())
    print ("Chain valid? " + str(blockchain.isChainValid()))
    blockchain.save()

    blockchain.chain[1].data = "Hello Darkness my old friend!"
    print(blockchain.printBlockChain())
    print ("Chain valid? " + str(blockchain.isChainValid()))
    blockchain.save()

    test = BlockChain()
    test.open()
    print(test.printBlockChain())
    print ("Chain valid? " + str(test.isChainValid()))
    test.save()

if __name__ == '__main__':
    main()
    
    
    
