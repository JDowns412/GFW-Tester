import json, os, math, pdb, time

for chunk in os.listdir("../Parsed"):
    print("Splitting %s" % chunk)
    with open("../Parsed/%s" % chunk, "r") as f:
        domains = json.load(f)

    count = 0
    temp = {}
    for domain in domains:
        count += 1
        # split off a new json every 10K domains
        if (count % 100 == 0):
            # pdb.set_trace()
            with open("../Temp/%s_%d.json" % (chunk.replace(".json",""), math.floor(count/100)), "w") as f:
                json.dump(temp, f, indent=4)
            temp = {}
            time.sleep(2)
        else:
               temp[domain] = domains[domain]

    # dump out the leftover domains
    with open("../Temp/%s_%d.json" % (chunk.replace(".json",""), math.floor(count/100)+1), "w") as f:
                    json.dump(temp, f, indent=4)