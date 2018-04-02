# (on windows) usage: python3 parser.py [USE CASE]
# example (windows) usage: python3 parser.py 3

import os, json, sys
from copy import deepcopy

def parseNew(data):

    results = deepcopy(data)

    for file in os.listdir():
        # if it's the cisco data
        if (file == "top-1m.csv"):
            with open(file, 'r') as f:
                # read in the data from the entire file into this temporary list
                for line in f:
                    if (len(line) > 0):
                        if (line.split(",")[1].rstrip() not in results):
                            results[line.split(",")[1].rstrip()] = {"rank" : int(line.split(",")[0])}

                # report progress
                print("Parsed in top sites from Cisco")

    return results



def parseOld(data):

    files = []
    domains = set()
    ignoreTypes = ["py", "json", "zip", "csv"]

    results = deepcopy(data)

    for file in os.listdir():
        flag = True
        for fType in ignoreTypes:
            if (file.endswith(fType)):
                # ignore the invalid file
                flag = False
            
        if(flag):
            #it is a file we want to parse
            files.append(file)

    # iterate over all of the files in the directory
    for file in files:
        count = 0
        with open(file, 'r') as f:
            country = file.split("-")[1]
            # read in the data from the entire file into this temporary list
            for line in f:
                count += 1
                if (len(line) > 0):
                    if (line not in results):
                        results[line.rstrip()] = {"country" : country, "rank" : count}

            # report progress
            print("Parsed in top sites from %s" % country)

    return results



def parse():
    # change to the directory where the Alexa lists are
    os.chdir("../Data")

    results = {}

    # USAGE CASES: #######################
    # parse old alexa data
    if (sys.argv[1] == "1"):
        results = parseOld(results)

    # parse new data (zone files and cisco data)
    elif(sys.argv[1] == "2"):
        results = parseNew(results)

    # parse both
    elif(sys.argv[1] == "3"):
        results = parseOld(parseNew(results)) 
    

    print("\nSaving results ...", end='')
    
    # dump the results
    with open("domains.json", 'w') as fp:
        json.dump(results, fp, indent=4)

    print("... Done")



if __name__ == "__main__":
    parse()


# TODO: ask josh if he want's "www." in front of his hostnames or not