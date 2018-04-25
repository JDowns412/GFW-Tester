import json, os, math, pdb, time

for chunk in os.listdir("../Temp"):
    print("Splitting %s" % chunk)
    with open("../Temp/%s" % chunk, "r") as f:
        domains = json.load(f)

    count = 0
    temp = {}
    num = 6000
    for domain in domains:
        count += 1
        # split off a new json every 10K domains
        if (count % num == 0):
            # pdb.set_trace()
            print("Split progress: ", str(count/ len(domains)))
            with open("../Inbound/%s_%d.json" % (chunk.replace(".json",""), math.floor(count/num)), "w") as f:
                json.dump(temp, f, indent=4)
            temp = {}
            time.sleep(2)
        else:
               temp[domain] = domains[domain]

    # dump out the leftover domains
    with open("../Inbound/%s_%d.json" % (chunk.replace(".json",""), math.floor(count/num)+1), "w") as f:
                    json.dump(temp, f, indent=4)