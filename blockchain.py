#!/usr/bin/python3
# coding=UTF-8
# encoding=UTF-8
import json
import os
import hashlib
import datetime

#B6210236 เอกปวีร์ อุ่นภักดิ์ 
#B6238124 สุชาวดี เที่ยงตรง
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
        return ("\n-------Block #" + str(self.index) 
                + "-------\nData: " + str(self.data)
                + "\nTimeStamp: " + str(self.timestamp)
                + "\nBlock Hash: " + str(self.hash)
                + "\nBlock Previous Hash: " + str(self.previousHash)
                +"\n")
        
    def printBlockTeam(self,name):
        if(self.data['Team1'] == name or self.data['Team2'] == name) :
            return ("\n-------Block #" + str(self.index) 
                + "-------\nData: " + str(self.data)
                + "\nTimeStamp: " + str(self.timestamp)
                + "\nBlock Hash: " + str(self.hash)
                + "\nBlock Previous Hash: " + str(self.previousHash)
                +"\n")
        else :
            return (False)

class BlockChain:
    def __init__(self, file="block.chain"):
        self.chain = [Block(0,"Genesis")]
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
    
    def invalidIndex(self):
         for i in range (1, len(self.chain)):
            if not self.chain[i].isValid():
                return i
            if self.chain[i].previousHash != self.chain[i-1].hash:
                return i
            
    def printValid(self):
        if(self.isChainValid()) :
            return "Verification : Verificated"
        elif(not self.isChainValid()) :
            return "Verification : not Verificated\nInvalid at Block #"+str(self.invalidIndex())
        
    def chkln(self):
        print(len(self.chain))
    
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
            
    def findTeam(self,name) :
        for i in range(1, len(self.chain)) :
            if(self.chain[i].printBlockTeam(name)) :
                print(self.chain[i].printBlockTeam(name))

def main():
    global blockchain 
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
    
    blockchain.open()
    while(True) :
        chk = input("\n-----ROV Pro League Data-----\n1 : View Current Blockchain\n2 : Create new Block\n3 : Find Team Data\n4 : Data Changing Testing\n5 : Show blockchain and invalid blockchain (example)\nPress exit to stop program \nWhich one do you want? : ")
        if(chk=='1') :
            print(blockchain.printBlockChain())
            print (blockchain.printValid())
            blockchain.save()
            continue
        
        elif(chk == '2') :
            team1 = input("Team1 : ")
            team1 = team1.upper()
            team2 = input("Team2 : ")
            team2 = team2.upper()
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
            while(True) :
                print("Score Team",team1," (0-4)") ; score1 = input(" : ")
                if(score1.isnumeric()) :
                    score1 = int(score1)
                    if(score1 >= 0 and score1 <= 4) :
                        break
            while(True) :
                print("Score Team",team2," (0-4)") ; score2 = input(" : ")
                if(score2.isnumeric()) :
                    score2 = int(score2) 
                    if(score2 >= 0 and score2 <= 4) :
                        break 
             
             
            score = str(score1)+'-'+str(score2)
            blockchain.generateBlock(team1, team2, winner, score)
            blockchain.save()
            continue
        
        elif(chk=='3') :
            name = input("Find Team : ")
            name = name.upper()
            blockchain.findTeam(name)
            blockchain.save()
            continue
        
        elif(chk=='4') :
            while(True) :
                n = input("block no. : ")
                if(n.isnumeric()) :
                    if(n.isnumeric() and int(n) > len(blockchain.chain)) :
                        print("Don't have enough block!")
                    elif(n.isnumeric() and int(n) < len(blockchain.chain)) :
                        break 
            message = str(input("data : "))
            blockchain.chain[int(n)].data = message
            print(blockchain.printBlockChain())    
            print (blockchain.printValid())
            blockchain.save()
            blockchain.open()
            continue
        
        elif(chk=='5') :
            #testold = BlockChain()
            blockchain.open()
            print('***Before test***')
            print(blockchain.printBlockChain())
            print (blockchain.printValid())
            blockchain.save()
            
            print('\n***Invalid Testing (edited blockchain) Block 2***')
            blockchain.chain[2].data = "Hello ka Ajarn Parin /|\\"
            print(blockchain.printBlockChain())
            print (blockchain.printValid())
            blockchain.save()
            
            print('\n\n***After Test***')
            #testnew = BlockChain()
            blockchain.open()
            print(blockchain.printBlockChain())
            print (blockchain.printValid())
            blockchain.save()
            continue
        
        elif(chk=='exit') :
            break
        
        else :
            print("Try again!")
            continue
            

if __name__ == '__main__':
    main()
    
    
    
