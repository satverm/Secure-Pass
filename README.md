# Secure-Pass
The project is for learning and is under development.
This will include codes related with storing usernames and passwords in a secure way.
## Note: if you store a password with some range specified at the beginning of the code and then try to retrieve the password from a range which does not fall within the original range then the passwords can't be retrieved. If you don't remember the range, you can try with some big range say 100000 to 200000 to retrieve the passwords. Bigger numbers are defined so that it takes more time for some one else to retrieve the password provided he also knows the passphrase.

## Updates: 
Full terminal/Text based UI completed.
## Smart Secure: Secure the password by making the lim_min and lim_max variable very large and a difference of atleast 10,000 between them (for example 800000 and 810000) and then revert the code to the default value of 1000 and 2000.
## To do
Add the code for the passwords and the passphrase to be meeting some parameters such as having atleast one integer, special characters, minimum length etc..

Make some form of documentation so that it follows the systems engineering model, this means to add documents such as requirements,specifications..

Options to store multiple users, service and password pairs using arrays, database etc.

Having a user interface to interact with the code and store and retrieve passwords.

Having the option to define administrators, users etc with various privileges for storing and retrieving the passwords

Option to define pairs of passphrases (more than two people storing different passphrase for the same data and make the password be retrievable only with all the persons entering their passphrase) This can work like a merkle tree and a single merle root hash can be used in the code and finally just one hash to store the password or some data or key for later retrievel and use. This can become a fork where the merkle root of passphrases or keys is stored as hash and used for authentication by two or more persons rater than retrieving the password. In that case the functions may be completely modified.

Using the concept of block chain to store the data in such a way that the data of individuals is stored using the hashing power of the network

Encrypting the database file itself.

Move Todo list out of Readme.md to todo.org




