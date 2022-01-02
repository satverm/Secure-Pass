# This program is used to store and retrieve the password in a secured way by using a pass-phrase.
# The logic is to hash the pass-phrase and then generate the hashes for each character of the password using the pass-phrase hash.
# Various methods would be uesd to ensure that the stored hashes are all unique even if the password and the passphrase for any two userid/service are same.
# Random values are used not for security but to make the hashes look random and make if difficult to find the number of characters in hte password.
# T0 retrieve the password, the pass-phrase is entered by the user and the characters of the password are recovered back by gemerating the 
# hashes and comparing with the stored hashes.
# Sqlite3 database can be used to store the data in a file for persistance and use by other functions. 

import hashlib as hs
import sqlite3 as sq
import random as rd

dbfile= 'pw_wallet_1_00.db'
ran_min, ran_max = 1000, 20000  # The difference between ran_min and ran_max cab be made large to increase the time for retrieving the passworod adn also to randomise the hashes so that they are different for same password and passphrase. The security is related only to the passphrse without which even with the data of hashes there is no way to find the passwords.

# First, let's define functions for storing the password

def secure_pw(user_name= None, service= None, passwd= None, pass_phrase= None, ran_min= None, ran_max= None):    # Todo convert all the functions to have the arguments passed in case requried.
    if user_name == None:
        user_name= input("Enter the username: ")
    if service == None:
        service = input("Enter the service name: ")
    if passwd == None:
        while True:
            passwd = input("Enter the password to store for the given username adn service: ")
            pwd_c = input("Enter the password again to confirm: ")
            if passwd == pwd_c:
                break
            else:
                print("The password do not match !! Try again..")
    if pass_phrase == None:
        while True:
            pass_phrase = input("Enter the pass phrase: ")
            print("Write the pass phrase in a paper for future refrence.")
            pass_phrase1 = input("Enter the pass phrase again to confirm: ")
            if pass_phrase == pass_phrase1:
                break
            else:
                print("The pass phrase entered by you don't match !! Try again...")
    if ran_min== None:
        ran_min = 1000
    if ran_max == None:
        ran_max = 10000
    ps_phr_hsh = hs.sha256(pass_phrase.encode('utf-8')).hexdigest()
    pw_hsh_lst = []
    n_count =0
    for char in passwd:
        n_count +=1
        ran_num= rd.randint(ran_min, ran_max)   # Add a random number string in the hash to randomize the hashes
        temp_str = str(ran_num) + char + chr(n_count) + str(ps_phr_hsh)
        pw_ch_hsh = hs.sha256(temp_str.encode('utf-8')).hexdigest()
        pw_hsh_lst.append(pw_ch_hsh)
    # Code to add random hashes, this can be converted into a function and be called as per requirement, this will enable the flexibility in the code
    ran_int = rd.randint(5,10)
    for i in range(ran_int):
        temp_str1 = str(rd.randbytes(10))
        ran_hsh = hs.sha256(temp_str1.encode('utf-8')).hexdigest()
        pw_hsh_lst.append(ran_hsh)
        
    pw_record = [user_name,service, str(pw_hsh_lst)]
    print(pw_record)
    return(pw_record)

def ret_pw():
    print("The program will  retrieve the password by using the pass phrase")
    sel_id = str(input("To see the userid and service name press Y/y:"))
    
    
    pass_phrase = input("Enter the pass phrase: ")
    pass_phrase1 = input("Enter the pass phrase again to confirm: ")
    if pass_phrase == pass_phrase1:
        print("Write the pass phrase in a paper for future refrence.")
        ps_phr_hsh = hs.sha256(pass_phrase.encode('utf-8')).hexdigest()
        pass_phrase, pass_phrase1 = '', ''
    else:
        print("The pass phrase entered by you don't match")
    #passwd = input("Enter the password to store for the given username adn service: ")
    n_count =0
    for i in range(128): #Later change to listofhash items only
        n_count +=1
        for j in range(128):
            temp_str = chr(i) + chr(n_count) + str(ps_phr_hsh)
            pw_ch_hsh = hs.sha256(temp_str.encode('utf-8')).hexdigest()
            if pw_ch_hsh == target_hash:
                pword += chr(i)
    pw_record = [user_name,service_name, str(pw_hsh_lst)]
    print(pw_record)
    return(pw_record)

# Now let's have a function to retrieve the password\s
def ret_pw():
    get_record = secure_pw()

    pass

# Function for storing the data in a file
def store_record():
    record = secure_pw()
    con = sq.connect(dbfile)
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS pwTAB(userId integer auto_increment primary key not null, UserName text, Service text, pwHash text)''')
    cur.execute('INSERT INTO pwTAB(userid,UserName,Service,pwHash) VALUES(?,?,?,?)',record)
    cur.execute('SELECT * FROM pwTAB')
    print(cur.fetchall())
    con.commit()
    con.close()

def get_all_record():
    con = sq.connect(dbfile)
    cur = con.cursor()
    cur.execute('SELECT * FROM pwTAB')
    record = cur.fetchall()
    con.close()
    return(record)

#print("Enter the details for storing a password")

secure_pw()
#store_record()
##get_all_record()
print("The program is used to store and retrieve passwords securily")



