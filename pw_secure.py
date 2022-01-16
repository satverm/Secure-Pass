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

dbfile= 'pw_wallet_1_01.db'  # The file name can be changed by the user here only to have different names.
lim_min, lim_max = 1000,2000   # The difference between ran_min and ran_max can be made large to increase the time for retrieving the passworod and also
# to randomise the hashes so that they are different even for same password and passphrase pairs. The security is provided by the passphrase without which even with
# the data of hashes there is no way to find the passwords.
## These limits can also be used as a smart feature to store the passwords using some big value but a small range of say 1000 and use the 
## same during retrieving process. So this can act as additional way of increasing diffuculty for others to retrieve the passwords.
fake_hash_limit = 10    # Adds random (1-10)number of fake hashes in the database.
#print("The program is used to store and retrieve passwords securely\n")

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
    #store_record(pw_record)
    print("The password has been secured and stored in database\n")
    return(pw_record)

def ret_pw(sel_id = None, pass_phrase= None, ran_min= None, ran_max= None):
    print("The program will  retrieve the password by using the passphrase\n")
    if sel_id == None:
        sel_y = str(input("To see the userid and service name press Y/y:"))
        if sel_y.lower() == 'y':
            get_all_records()
        sel_id = input("Enter the id  to retrieve the password: ")
    # Now get the record from the database for the selected id and retrieve password using the passphrase
    if get_all_records(sel_id) == []:
        print("The selected ID is not present!!")
    else:
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
                    print("\nThe password is: {}".format(pword))

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
    print("Password Wallet updated")

def del_rec(sel_id = None):
    if sel_id == None:
        print("The records stored in the database are: ")
        get_all_records()
        sel_id = (input("Enter the id for which record is to be deleted: "))
    else:
        get_all_records(sel_id)
    sel_rec = get_all_records(sel_id)
    #print(sel_rec)
    if sel_rec == []:
        print("The selected ID is not present !!")
    else:
        con = sq.connect(dbfile)
        cur = con.cursor()
        cur.execute('DELETE FROM pwTAB WHERE userID = (?)',(sel_id,))
        con_del = input("Press Y/y to  confirm deleting the selected record: ")
        if con_del.lower() == 'y':
            con.commit()
            print("The selected id {} has been deleted!!".format(sel_id))
        else:
            print("The selected record has not been deleted.")
        con.close()

def update_rec(sel_id = None):
    if sel_id == None:
        print("The records stored in the database are: ")
        get_all_records()
        sel_id = input("Enter the id for which password is to be updated: ")
    else:
        print("The selected record is as under: ")
        get_all_records(sel_id)
    if get_all_records(sel_id) ==[]:
        print("The entered ID is not present!!")
    else:
        rec_to_updt = sel_rec(sel_id)
        updated_rec = secure_pw(rec_to_updt[1],rec_to_updt[2])
        con = sq.connect(dbfile)
        cur = con.cursor()
        cur.execute('UPDATE pwTAB  SET pwHASH = (?) WHERE userID = (?)',(updated_rec[2],sel_id,))
        con_updt = input("Press Y/y to  confirm updating the selected record: ")
        if con_updt.lower() == 'y':
            con.commit()
            print("The selected id {} has been updated!!".format(sel_id))
        else:
            print("The selected record has not been updated.")
        con.close()

def sel_rec(sel_id = None):
    if sel_id == None:
        sel_id = input("Enter the id  to select the record: ")
    if get_all_records(sel_id) == []:
        print("The entered ID is not present!!")
        rec_list =[]
    else:
        con = sq.connect(dbfile)
        cur = con.cursor()
        cur.execute('SELECT * FROM pwTAB WHERE userID = (?)',(sel_id,))
        record = cur.fetchone()
        con.close()
        tmp_str = str(record[3])
        tmp_str1 = tmp_str.strip("[]")
        hash_list = tmp_str1.split(', ')
        rec_list= [record[0],record[1], record[2],hash_list]
        #print(rec_list)
    return(rec_list)

def get_all_records(sel_id= None):
    con = sq.connect(dbfile)
    cur = con.cursor()
    if sel_id != None:
        #sel_id = input("Enter the id  to select the record: ")
        cur.execute('SELECT * FROM pwTAB WHERE userID = (?)',(sel_id,))
        record = cur.fetchall()
    else:
        cur.execute('SELECT * FROM pwTAB')
        record = cur.fetchall()
    for item in record:
        print("ID={}    | UserName={}      | Service= {}".format(item[0],item[1],item[2]))
    con.close()
    return(record)

def pw_ui():
    print("\n***The program is used for storing and retrieving your password***")
    con = sq.connect(dbfile)  # will create a database file if not present
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS pwTAB(userID integer primary key autoincrement not null, UserName text, Service text, pwHash text)''')
    cur.execute("SELECT * FROM pwTAB")
    data_chk = cur.fetchone()
    if data_chk == None:
        no_data = True
        print("There is no data stored at present in the database!!")
        print("A new database file: {} has been created !!".format(dbfile))
    else:
        no_data = False
    con.commit()
    con.close()
    task_list = ["0: Exit","1: Store Password","2: Update password","3: Delete Password Record","4: Retrieve Password", "5: View Usernames ID"]
    #print(task_list)
    while True:
        print("\nFollowing tasks can be performed:-")
        for item in task_list:
            print(item)
        if no_data == True:
            # Give option to exit (todo)
            print("Enter the details for storing a new record for securing password.")
            sel_y = input("Enter Y/y to continue or Enter/Return/any key to abort: ")
            if sel_y.lower() == 'y':
                sel_task = '1'
                print("A new record will be created !!")
            else:
                print("Program finished ..")
                break
        else:
            sel_task = str(input("\nEnter the number for the Selected Task: "))
        
        if sel_task == '1':
            store_record()
            no_data = False
        elif sel_task == '2':
            update_rec()
        elif sel_task == '3':
            del_rec()
        elif sel_task == '4':
            ret_pw() #todo: avoid double printing of selected record
        elif sel_task == '5':
            get_all_records()
        elif sel_task == '0':
            print("The program completed!!")
            break
        else:
            print("No valid input recieved, Exiting the program!!")
            break
def main():
    pw_ui()

if __name__ == "__main__":
        main()


#print("Let's run the UI code..\n")
#print(len(get_all_records()))
#pw_ui()
#secure_pw()
#store_record()
#ret_pw()
#sel_rec()
#get_all_records(1)



