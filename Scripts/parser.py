import os, json, math, pprint

def parse(length):
    # change to the directory where the Alexa lists are
    os.chdir("../Data")

    files = []
    data = {}
    domains = set()
    results = {"sites" : []}

    for file in os.listdir():
        if (file.split(".")[-1] == "py" or file.split(".")[-1] == "json"):
            # ignore the file, since we don't want to evaluate on a python file
            pass
        else: #it is a file we want to parse in alexa domains
            # we build the results dictionary as we go, file by file
            files.append(file)

    # iterate over all of the files in the directory
    for file in files:
        with open(file, 'r') as f:
            country = file.split("-")[1]
            data[country] = []
            # read in the data from the entire file into this temporary list
            for line in f:
                if (len(line) > 0):
                    data[country].append(line)

    # now that data contains all of the top sites in one place (and we don't 
    # have to open up files anymore), we can aggregate a psudo top 500 list.
    # I have no way of knowing which sites are the most popular overall, but 
    # I can take the top 500/[# of data files] from each file to get the top
    # sites that I could guess. 
    # TODO: Later we can apply proportions to these sites based on #users/country
    # pprint.pprint(data)

    # print("\n")

    
    # we want to aggregate roughly this many sites together
    goalLength = length
    num = 0
    while (len(results["sites"]) <= (goalLength + goalLength%len(data))):
        # print(num)
        # take off an even number of sites per country
        for country in data:
            # print(num)
            if (data[country][num].split(".")[0] not in domains):
                domains.add(data[country][num].split(".")[0])
                results["sites"].append(data[country][num].strip())
        num += 1

    # check the length of the results "top" sites list
    print("aggregated the \"top\" %d sites." % len(results["sites"]))

    # dump the results
    with open("top%dEven.json" % goalLength, 'w') as fp:
        json.dump(results, fp, indent=4)


if __name__ == "__main__":
    goalLength = 5
    parse(goalLength)