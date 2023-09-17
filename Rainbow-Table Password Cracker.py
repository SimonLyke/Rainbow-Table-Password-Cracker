import random
import hashlib
from datetime import datetime
import sympy

#Password Length
#password space size = AN+AN-1+...A0
#where A is the length of the alphabet and N is the length of the password

char_list = "abcdefghijklmnopqrstuvwxyz"
char_dict = { 'a':0, 'b':1, 'c':2,'d':3, 'e':4, 'f':5, 'g':6, 'h':7, 'i':8, 'j':9, 'k':10, 'l':11, 'm':12, 'n':13,
              'o':14, 'p':15, 'q':16, 'r':17, 's':18, 't':19, 'u':20, 'v':21, 'w':22, 'x':23, 'y':24, 'z':25 }

num_list = "0123456789"
num_dict = { '0':0, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9 }

comb_list = "abcdefghijklmnopqrstuvwxyz0123456789"
comb_dict = { 'a':0, 'b':1, 'c':2,'d':3, 'e':4, 'f':5, 'g':6, 'h':7, 'i':8, 'j':9, 'k':10, 'l':11, 'm':12, 'n':13,
              'o':14, 'p':15, 'q':16, 'r':17, 's':18, 't':19, 'u':20, 'v':21, 'w':22, 'x':23, 'y':24, 'z':25, '0':26,
              '1':27, '2':28, '3':29, '4':30, '5':31, '6':32, '7':33, '8':34, '9':35 }

#using dictionaries allows for easier string conversion into numbers base 26 and 10
# an example here would be
#password = 'abz'
#using the dictionary we can do
#for char in password:
#   sum += char_list[char]
# the result here would be 0 + 1 + 25  = 26

char_len = len( char_list )
num_len = len( num_list )
comb_len = len( comb_list )
chain_len = 5000
chain_num = ''
# chain_len * 20,000 = 100,000,000 which is 100 million. this satisfies the requirements in assignment spec
# since 20,000 satisfies less than half of the possible passwords for 6 digit passwords it has changed to  40,000
# this number needs to be altered for other password lengths, otherwise it will either generate very little percentage
# of possible passwords for long password lengths, or end up with too many collisions exhausting all the possible
# passwords of smaller password lengths and then never reach its target number of chains so wont store them in file.
pw_len = ''
pw_space_size = 0
prime = 0
chosen_dict = {}
chosen_list = []
dict_name = ""

#global variables are necessary in this small file to reduce the amount of arguments passed to nested functions

def init(): # initializes important values needed for calculations
    get_pw_len()
    get_pw_space_size()
    get_prime()
    get_dict()

def get_dict():
    global chosen_dict
    global chosen_list
    global dict_name
    while True:
        choice = input("Please Choose Dictionary - (1) Char Only - (2) Num Only - (3) Combined --> ")
        if choice is "1":
            chosen_dict = char_dict
            chosen_list = char_list
            dict_name = "char"
            return
        elif choice is "2":
            chosen_dict = num_dict
            chosen_list = num_list
            dict_name = "num"
            return
        elif choice is "3":
            chosen_dict = comb_dict
            chosen_list = comb_list
            dict_name = "combined"
            return
        else:
            print("\nValue Entered Is Not A Valid Choice!")


def get_table_length():
    global chain_num
    #global pw_len # once again password length is already defined globally but without declaring as global in this scope it is not found
    recommended_length = (len(chosen_list) ** pw_len)/chain_len
    print(f"Recommended Table Length = {recommended_length}")
    while not chain_num.isnumeric(): # check if entered string is numerical digits only if not loop until it is
        chain_num = input("Please Enter Number Of Chains To Generate For Rainbow Table --> ")
    chain_num = int(chain_num)



def get_pw_space_size(): # this function calculates the password space size using password length
    global pw_space_size

    for i in range( pw_len+1 ):
        pw_space_size += ( comb_len**i ) # comb_len = 36 as its alphabet combined with unique digits
    print( f"Password Space Size = {pw_space_size}" )


#def is_prime( num ): this function is now obselete as when password length was changed to >6 this function would
                     # infinitely loop. instead we replace this function with library Sympy. sympy.isprime(number)
                     # Sympy's isprime function returns a boolean

def int_to_pw( num ): # this function takes an integer and maps it to a string. length is not static
    string = ""
    while( num >= 0 ):
        remainder = int( num % len( chosen_dict ) )
        string = chosen_list[remainder] + string # this adds a character to the beginning of the existing string
        num = int( num/36 )
        num = num - 1 # this is important in dealing with different lengthed strings
    return string # returns the string to where this function was called from


def add_to_file( chain_list, pw_len ): # this function stores a generated rainbow table into a file named appropriately
                                       # for the password length. if a file does not exist, it creates one.
    length = str( pw_len )
    file_name = f"{dict_name}_table_length_{length}.txt" # for 6 digit password the file name would be table_length_6

    with open(file_name, 'w+') as fp: # using " with open " when dealing with files is good python practice
        for chain in chain_list:
            fp.write(f"{chain[0]},{chain[1]}\n") # writes in format " start_string , end_string "
    fp.close() # close the file when it is no longer needed if it is not already closed
    return file_name


def load_table(length): # this function loads in a rainbow table of given password length and stores table in a list
    table = []
    file_name = f"{dict_name}_table_length_{length}.txt"
    with open(file_name,'r') as fp:
        for line in fp:
            temp_list = line.split(",")
            table.append([temp_list[0],temp_list[1].replace('\n', '')]) # store in list and remove \n character
    fp.close()
    return table


def get_prime(): # this function sets the prime number to be the first prime number that is larger
                 # than password space size
    global prime
    prime = pw_space_size
    while not sympy.isprime( prime ):
        prime += 1
    # edits global variable so nothing needs to be returned

def get_pw_len(): # get password length from user in order to crack hash or generate rainbow table for that pw length
    global pw_len

    while not pw_len.isnumeric(): # check if entered string is numerical digits only if not loop until it is
        pw_len = input("Please Enter Length Of Password To Generate Rainbow Table Or Max Length Of Password To Crack --> ")
    pw_len = int(pw_len)
    print(f"\nPassword Length = {pw_len}")
    # changed global variable so no return needed

def chain_gen(): # Main function for generating rainbow tables

    start_time = datetime.now() # used to calculate time elapsed
    end_strings = []
    start_strings = []
    chain_list = []
    collisions = 0

    init()
    get_table_length()
    print(f"Target No of Chains = {chain_num}")
    print(f"Target Chain Length = {chain_len}\n")


    for i in range( chain_num ): # 0-chain_num
        while True:
            while True: # this is to ensure that the first string of chain is not already done
                rand_str = "" # initialize empty string
                for x in range( pw_len ):
                    rand_str += random.choice( chosen_list ) #generate random string of pw_len size from list of num and chars
                if rand_str not in start_strings:
                    start_strings.append(rand_str)
                    break
            plain_text = rand_str # this is so that "rand_str" remains the first string in the chain
                                      # and "plain_text" will eventually become the last string in the chain

            for pos in range( chain_len ): # 0 - 4999
                plain_text = reduce(hash(plain_text),pos) # hash and then reduce
                # hash and reduce (chain_len) times for chain_num chains
            print(f"\rChains Generated = {i + 1} - Size = {chain_len} - Time Elapsed = {datetime.now() - start_time} "
                  f" - Start String = {rand_str} - End String = {plain_text} - collisions = {collisions}",end=""
                  , flush=True)
            # using end="\r" stops it printing real time, even using flush=True
            # to solve this we start the string with carriage return and dont end it with \n by default

            if i+1 == chain_num:
                break

            elif plain_text not in end_strings: # only add chain if no collision of end strings
                chain_list.append((rand_str,plain_text)) # add start string and end string of chain to chain list
                end_strings.append(plain_text) # faster to iterate over list of single items when checking collisions
                break
            else:
                collisions +=1
                continue # generate new chain WITHOUT ITERATING NUMBER OF CHAINS GENERATED
                         # this allows us to reach the target number of chains regardless of how many collisions


    return add_to_file( chain_list, pw_len ) # return function that stores in file and then returns file name


def hash( string ): # turn string into bytes and then into SHA-1 Hash
    hashed_bytes = hashlib.sha1( string.encode( 'utf-8' ) )
    hashed_string = hashed_bytes.hexdigest()
    return hashed_string # return hash of string


def reduce( hash, pos ): # reduce turns hash into new string - HAS TO BE REPRODUCIBLE - which it is
    #MAP TO INTEGER
    global pw_len

    length = pw_len # this is necessary aswell as declaring pw_len a global. despite not needing pw_len to be mutable
                    # referencing it without declaring it as global within the scope as  " hash[:pw_len] "  did not work
                    # this is NECESSARY and unsure why as reading the variables value without declaring it
                    # works in other functions above. however we assign the value to length as we dont want to change
                    # the value of pw_len so length will be used for all changes within this scope
    num = 0
    temp = 0
    for x in hash: # generate integer based on all characters of the hash - reduces collisions
        temp += comb_dict[x] # this is combined list ONLY as hashes contain both letters and numbers

    temp = temp % len(comb_dict) # use pos to change outcome - reduces collisions
    for i in hash:
        num += comb_dict[i] * ( len(comb_dict) ** ( length+1))
        length = length+1
        num = (num+(pos*temp)) % prime
    return int_to_pw(num) # return function that generates string based on integer created here and then returns string


def find_pw_in_chain( line, position ): # uses chain that contains password and position to reproduce chain and find pw

    string = line[0]

    for pos in range(position): # hash and reduce until password is found
        hashed = hash(string)
        string = reduce(hashed,pos)
    return string # return password from chain


def crack_hash(): # main function for cracking the SHA-1 hash
    global pw_len # we append pw_len in the function so we declare the global scope here
    init()

    while True:
        hash_to_crack = input("Please Input Valid SHA-1 Hash To Be Cracked --> ")
        if len(hash_to_crack) != 40:  # valid SHA-1 hashes are ALWAYS 40 characters long - User Input Checking
            print("Please Enter Valid SHA-1 Hash")
        else:
            hash_to_crack = hash_to_crack.lower()
            break

    start_time = datetime.now()  # for use in calculating time elapsed

    for i in range(1,pw_len+1): #e.g  if pw len is 6 it will go 1 - 6, iterates through all tables until password length
        pw_len = i

        table = load_table(pw_len) # load rainbow table from file for given password length
        print(f"\nTable Length = {len(table)+1}  -  Password Length = {pw_len}")

        for rev_pos in reversed(range(chain_len)): # 4999 - 0    reversed position as it works backwards
            print(f"\rPos = {rev_pos} - Time Elapsed = {datetime.now() - start_time}", end='', flush=True)
            string = hash_to_crack

            for pos in range(rev_pos,chain_len): #rev_pos - 4999 ( ends at 0-4999 ) how many reductions need to take place
                if pos != rev_pos:
                    string = hash(string) # if pos == rev_pos then string is already a hash
                string = reduce(string,pos)

            for line in table: # check if reductions have found end string in list of chains
                if string == line[1]: # there can only be one match of end string as we throw away duplicate end string chains
                    password = find_pw_in_chain(line,rev_pos)
                    if hash(password) == hash_to_crack:
                        print(f"\n\nPassword = {password}")
                        return True
                    break



def main(): # MAIN FUNCTION this is the users main UI for choosing options - includes User Input Checking
    while True:
        print("Rainbow Table SHA-1 Password Cracker\n")
        choice = input("Please Choose Option (1) Generate Rainbow Table - (2) Crack Password - (3) Exit --> ")

        if choice is "1":
            file_name = chain_gen()
            print(f"\nTable Generated - Stored In File - {file_name}")
            exit(1)

        elif choice is "2":
            if crack_hash():
                exit(1)
            else:
                print("\nPassword Unable To Be Cracked, Try Generating Longer Rainbow Tables\n")
                exit(0)

        elif choice is "3":
            exit(1)

        else:
            print("\nValue Entered Is Not A Valid Choice!")


if __name__ == "__main__": # python code executes ALOT faster within functions so everything is in a function
    main()