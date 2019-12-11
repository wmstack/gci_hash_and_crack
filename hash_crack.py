#!/usr/bin/env python3
import os
import sys

import inspect
import termcolor

#hashing library
import hashlib

#some scraping
from lxml import html
import requests
from fake_useragent import UserAgent
ua = UserAgent()

def hasher():
    #hashing options
    hash_options = {
    "1":hashlib.md5,
    "2":hashlib.sha1,
    "3":hashlib.sha224,
    "4":hashlib.sha256,
    "5":hashlib.sha384,
    "6":hashlib.sha512
    }

    #nifty hack to remove indentation
    print(inspect.cleandoc(
        """
        What kind of HASHING
        1.md5
        2.sha1
        3.sha224
        4.sha256
        5.sha384
        6.sha512
        """
    ))
    
    #get number
    while True:
        hash_option = input("Enter the number : ")
        if hash_option in hash_options.keys():
            break
        else:
            print("Not one of the numbers. try again")

    plain_str = input("Enter the thing to be Hashed : ")

    hash_value = hash_options[hash_option](plain_str.encode("utf-8")).hexdigest()

    print("{}  =  {}".format(plain_str, hash_value))
    
def offline_crack(hash_string, hash_function):
    password_list_path = os.path.abspath(os.path.realpath(
        input("Enter the name of password list : ")
    ))

    with open(password_list_path, "r") as password_list:
        for line in password_list:
            if hash_function(line.rstrip().encode("utf-8")).hexdigest() == hash_string:
                print( 
                    termcolor.colored("[+] found --> {}  =  {}"
                    .format(line.rstrip(),hash_string) ,"green"
                    )
                )
                break
        else:
            print("Couldn't find password with the same hash")

def online_crack(hash_string, hash_function, hash_name):
    url = "https://hashtoolkit.com/reverse-hash/?hash={}".format(hash_string)
    try:
        html_file = requests.get(url,headers={'User-Agent':ua.chrome}).text
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)
    tree = html.fromstring(html_file)
    
    nodes = tree.xpath("//span[@title='decrypted {} hash']".format(hash_name))
    if len(nodes)>0:
        cracked_hash = nodes[0].text
        print( 
                termcolor.colored("[+] found --> {}  =  {}"
                .format(cracked_hash.rstrip(),hash_string) ,"green"
                )
            )
    else:
        print("Couldn't crack online, cracking offline")
        return offline_crack(hash_string, hash_function)
        

def crack_hasher():

    #number of bits and the corresponding hash function
    hash_bit_sizes = dict([
        (128,{"name": "md5", "function": hashlib.md5}),
        (160,{"name": "sha1", "function": hashlib.sha1}),
        (224,{"name": "sha224", "function": hashlib.sha224}),
        (256,{"name": "sha256", "function": hashlib.sha256}),
        (384,{"name": "sha384", "function": hashlib.sha384}),
        (512,{"name": "sha512", "function": hashlib.sha512}),
    ])

    hash_string = input("Enter the hash: ")

    #number of bits from hex
    if  not len(hash_string)*4 in hash_bit_sizes.keys():
        print("Unknown hash")
        return

    hash_dict =hash_bit_sizes[len(hash_string)*4]
    hash_function = hash_dict["function"]
    hash_name = hash_dict["name"]

    while True:
        online_crack_yn = input("Use online {} Cracking tool? [y/n] : ".format(hash_name))+" "
        if online_crack_yn[0].lower() == 'y':
            return online_crack(hash_string, hash_function, hash_name)
        elif online_crack_yn[0].lower() == 'n':
            return offline_crack(hash_string, hash_function)
        
while True:
    a= input("To Hash press 1 and to Crack Hash press 2 : ")
    
    if a=="1":
        hasher()
    elif a=="2":
        crack_hasher()
    else:
        print("Not 1, or 2")