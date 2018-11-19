import sys
import time
import random
from blockchain import BlockChain
import string
import re

from datetime import datetime, date, time
import sqlite3
import time as time
import networkx as nx
import matplotlib.pyplot as plt

contract_source_code = '''
pragma solidity ^0.4.18;
 contract Record{
     uint noblock;    
    event TaskIno(
        bytes32 task_id,
        bytes32 indexed input_value,
        bytes32 task1,
        bytes32 indexed output,
        bytes32 account,
        bytes32 time
       );
     event Invalidation(
        string type1,
        string time,
        string data
    );
     event MyBlock(
        bytes32 indexed invalid_block
    );
     constructor () public{
     }
         function storeData(bytes32 _task_id, bytes32 _input_value, bytes32 _task, bytes32 _output, bytes32 _account, bytes32 _time) public {
        emit TaskIno(_task_id, _input_value, _task, _output, _account, _time);
 }
    function InvalidationBlock(string _type,string _time,string _data){
        emit Invalidation(_type, _time, _data);
    }
     function InvalidBlock(bytes32 _block_hash){
        emit MyBlock(_block_hash);
}
}
'''

block = BlockChain("http://127.0.0.1:8545", contract_source_code)

block.DeployContract()

# Nitin: Creating DB connection and creating the table each time this code is run.
conn = sqlite3.connect('local.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
curr = conn.cursor()
curr.execute("DROP TABLE transactions")
curr.execute('''CREATE TABLE transactions
          (trans_id TEXT PRIMARY KEY,
          input_value TEXT,
          task TEXT,
          output_value TEXT,
          account TEXT,
          time_ TEXT,
          transHash TEXT,
          valid TEXT)''')

#Nitin: API to search by output field in DB
def searchByOutput_DB(output_param):
    t = curr.execute("SELECT * FROM transactions WHERE output_value = ?", (output_param,)).fetchone()
    return t

returnResult = ""


def calculate_time():
    iterations= int(sys.argv[1])
    max_number = int(sys.argv[2])

    generate_random(iterations,max_number)
def generate_random(itr,max):
    start_time = time.time()
    for x in range (itr):
        i=random.randint(1,max+1)
        tmp="tmp-"+str(i)+"-0" # tmp: random generated blockchain output that needs to be searched
        # Wen: adding API here
        print(block.search_by_output_field(bytes(tmp,"utf-8")))  #search in blockchain network
        print(searchByOutput_DB('tmp')) #search in local database
     
    stop_time=time.time()

    average_time= (stop_time-start_time)/itr
    print(average_time)



if __name__ =="__main__":
    calculate_time()

