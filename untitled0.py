#impoerting the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify

#part 1 building a blockchain
class Blockchain:
    
    def __init__(self):
        self.chain = []  #initialising the chain,creating the chain
        #create the genesis block
        self.create_block(proof = 1, previous_hash = '0') #0 and 1 are the arbitrary values
        #we need two arguments one is to maintain the prrof and other is to maintain the hash of previous block
        
        
    def create_block(self, proof, previous_hash):
        #we are going t make a dictionary that will define each block in the blockchainwith its four essential keys
        #1.index
        #2.timestamp
        #3.proof of block
        #4.previous hash
        # we can add anything to this not only the above 4
        block = {'index': len(self.chain)+1 ,
                 'timestamp': str(datetime.datetime.now()),#datetime ek library hai which will give the current time
                 'proof': proof,#argument leta hai
                 'previous_hash': previous_hash}
        self.chain.append(block)#chain is a list so we all need the append function to add in the list of block
        return block
    
    
    def get_previous_block(self):
        return self.chain[-1]
    
    ###what wxactly is proof of work == proof of work is something tht the miner shave to solve a question 
    # and then the mining is possible if they match the exact number that we have save din the proof block
    #define a question challenging to solve but easy to verify
    def proof_of_work(self, previous_proof):
        new_proof = 1
        #new variable to check whether the new new proof is right or not
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof*2 - previous_proof*2).encode()).hexdigest()
            #to check first four didgits are xeroes and then our mining will be sucessfull
            if hash_operation[:4] == '0000':
                check_proof = True
            #if the hash operation mai mila hua galta hua to else check mai newproof ko ek se 
            #increment karke we will check for new value and verify whether that the proof matches
            else:
                new_proof += 1
        return new_proof
    
    #check 2 things
    #four leading zeroes
    #prevoius hash of each block = hash of previous block
    def hash(self, block):
        encoded_block= json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    def is_chain_valid(self,chain):
        previous_block=chain[0]
        block_index = 1
        while block_index<len(chain):
            block = chain[block_index]
            if block['previous_hash']!= self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(new_proof*2 - previous_proof*2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index +=1
        return True
    
    
    
    
    
    
#flask based web appliation
#creating a web app

app = Flask(__name__)


#creating a blockchain
blockchain = Blockchain()
#mining a new block
@app.route('/mine_block', methods = ['GET'])    
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    #postman mai ho jaayega ye implement interface ki tarah kaam karta hai
    response = {'message':'Congratulations u just mined a block!',
                'index': block['index'],
                'timestamp':block['timestamp'],
                'proof':block['proof'],
                'previous_hash':block['previous_hash']}
    return jsonify(response), 200;  #http codes check karlo 200 is for ok


# creating full blockchain
@app.route('/get_chain')
def get_chain():
    response = {'chain':blockchain.chain,
                'length':len(blockchain.chain)}
    return jsonify(response), 200;

@app.route('/home')  
def home():  
    response = {'chain':blockchain.chain,
                'length':len(blockchain.chain)}
    return "yo";

app.run(host='0.0.0.0',port= 5000) 
#running the app
