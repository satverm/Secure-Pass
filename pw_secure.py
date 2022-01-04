# This program is used to store and retrieve the password in a secured way by using a pass-phrase.
# The logic is to hash the pass-phrase and then generate the hashes for each character of the password using the pass-phrase hash.
# Various methods would be uesd to ensure that the stored hashes are all unique even if the password and the passphrase for any two userid/service are same.
# Random values are used not for security but to make the hashes look random and make if difficult to find the number of characters in hte password.
# To retrieve the password, the pass-phrase is entered by the user and the characters of the password are recovered back by gemerating the 
# hashes and comparing with the stored hashes.
# Sqlite3 database can be used to store the data in a file for persistance and use by other functions. 

import hashlib as hs
import sqlite3 as sq
import random as rd

dbfile= 'pw_wallet_1_00.db'  # The file name can be changed by the user here only to have different names.
lim_min, lim_max = 100000,200000   # The difference between ran_min and ran_max cab be made large to increase the time for retrieving the passworod and also
# to randomise the hashes so that they are different for same password and passphrase. The security is related only to the passphrase without which even with
# the data of hashes there is no way to find the passwords.
## These limits can also be used as a smart feature to store the passwords using some big value but a small range of say 1000 and use the 
## same during retrieving process. So this can act as additional way of increasing diffuculty for others to retrieve the passwords.
fake_hash_limit = 10    # Adds random number of fake hashes in the database.

# First, let's define functions for storing the password
def secure_pw(user_name= None, service= None, passwd= None, pass_phrase= None, ran_min= None, ran_max= None):
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
            pass_phrase = input("Enter the passphrase: ")
            print("Write the pass phrase in a paper for future refrence.")
            pass_phrase1 = input("Enter the pass phrase again to confirm: ")
            if pass_phrase == pass_phrase1:
                break
            else:
                print("The pass phrase entered by you don't match !! Try again...")
    if ran_min== None:
        ran_min = lim_min
    if ran_max == None:
        ran_max = lim_max
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
    ran_int = rd.randint(1,fake_hash_limit)
    for i in range(ran_int):
        temp_str1 = str(rd.randbytes(10))
        ran_hsh = hs.sha256(temp_str1.encode('utf-8')).hexdigest()
        pw_hsh_lst.append(ran_hsh)
    pw_record = [user_name,service, str(pw_hsh_lst)]
    store_record(pw_record)
    return(pw_record)

def ret_pw(sel_id = None, pass_phrase= None, ran_min= None, ran_max= None):
    print("The program will  retrieve the password by using the passphrase\n")
    if sel_id == None:
        sel_id = str(input("To see the userid and service name press Y/y:"))
        if sel_id.lower() == 'y':
            print(get_all_records())
        sel_id = input("Enter the id  to retrieve the password: ")
    # Now get the record from the database for the selected id and retrieve password using the passphrase
    rec_list = sel_rec(sel_id)
    pw_hash_list = rec_list[3]
    if pass_phrase == None:
        pass_phrase = input("Enter the pass phrase: ")
    ps_phr_hsh = hs.sha256(pass_phrase.encode('utf-8')).hexdigest()
    if ran_min == None:
        ran_min = lim_min
    if ran_max == None:
        ran_max = lim_max
    n_count =0
    pword = ''
    for item in pw_hash_list:
        tmp_chk = False
        n_count +=1
        for i in range(128): 
            tmp_chk = False
            for j in range(ran_min,ran_max+1):
                temp_str = str(j) + chr(i) + chr(n_count) + str(ps_phr_hsh)
                chk_hsh = hs.sha256(temp_str.encode('utf-8')).hexdigest()
                if item[1:-1] == chk_hsh:
                    pword += chr(i)
                    print("character{} is {}".format(n_count,chr(i)))
                    tmp_chk = True
                    break
            if tmp_chk == True:
                break
        if pword =='':
            print("The pass phrase is incorrect !!")
            break
        else:
            if tmp_chk == False:
                print("The password is: {}".format(pword))
                break
    return(pword)

 

# Function for storing the data in a file
def store_record(record = None):
    if record == None:
        record = secure_pw()
    con = sq.connect(dbfile)
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS pwTAB(userID integer primary key autoincrement not null, UserName text, Service text, pwHash text)''')
    cur.execute('INSERT INTO pwTAB(UserName,Service,pwHash) VALUES(?,?,?)',record)
    con.commit()
    con.close()
    print("Password Wallwt updated")

def sel_rec(sel_id = None):
    if sel_id == None:
        sel_id = input("Enter the id for which password is to be found: ")
    con = sq.connect(dbfile)
    cur = con.cursor()
    cur.execute('SELECT * FROM pwTAB WHERE userID = (?)',(sel_id,))
    record = cur.fetchone()
    con.close()
    tmp_str = str(record[3])
    tmp_str1 = tmp_str.strip("[]")
    hash_list = tmp_str1.split(', ')
    rec_list= [record[0],record[1], record[2],hash_list]
    return(rec_list)

def get_all_records():
    con = sq.connect(dbfile)
    cur = con.cursor()
    cur.execute('SELECT * FROM pwTAB')
    record = cur.fetchall()
    con.close()
    return(record)

#print("Enter the details for storing a password")

#secure_pw()
#store_record()
#get_all_record()
print("The program is used to store and retrieve passwords securely")



