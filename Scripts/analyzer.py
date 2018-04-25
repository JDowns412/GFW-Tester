from scapy.all import *
import json, sys, os, pdb, random, re, threading

def prime():
    exNum = -1

    os.chdir("../Results")
    with open("expNum.json", 'r') as f:
        temp = json.load(f)
        exNum = temp["number"]

    # pdb.set_trace()
    # if ("exp%d_MetaResults.json" % exNum not in os.listdir()):
    #     # we need to create it
    #     out = {"tried" : 0, "allowed" : 0, "blocked" : 0, "errors" : 0}
    #     with open ("exp%d_MetaResults.json" % exNum, 'w') as fp:
    #             json.dump(out, fp, indent=4)

    return exNum

def work(chunk, loc, counter):


    print("Thread %d started working on %s" % (counter, chunk))
    # pdb.set_trace()
    # exNum = prime()
    exNum = 0
    
    with open("../%s/%s" % (loc, chunk), "r") as f:
        hostnames = json.load(f)

        results = {"meta" : {"tried" : 0, "allowed" : 0, "blocked" : 0, "errors" : 0}, "domains" : {}}
        #hostnames = ["www.falundafa.org","www.yahoo.com"]
        count = 0
        for hostname in hostnames:
            count += 1
            if (count % 25 == 0):
                print(str(count), " done on ", chunk, " by thread ", str(counter))
            try:
                ans = dns_req(hostname)
                if (len(ans)>=1):
                    # it's blocked
                    results["meta"]["blocked"] += 1

                    # removing this to decrease json size:
                    # results[hostname]["blocked"] = True
                    # if it's present in the results dict, we know it was blocked. If it's not, it's not blocked
                    ipid = ans[len(ans)-1][1][IP].id
                    ttl = ans[len(ans)-1][1][IP].ttl
                    results["domains"][hostname] = {}
                    results["domains"][hostname]["ttl"] = ttl
                    results["domains"][hostname]["ipid"] = ipid
                    results["domains"][hostname]["responses"] = len(ans)
                else:
                    # it's not blocked
                    results["meta"]["allowed"] += 1

                # it was tested successfully
                results["meta"]["tried"] += 1

            except Exception as exception:
                with open("../Logs/Experiment_%s.log" % str(exNum), 'a') as log:
                    name = repr(exception).split('(')[0]
                    print("%s exception encountered while testing %s" % (name, hostname))
                    log.write("%s exception encountered while testing %s\n" % (name, hostname))
                    # pdb.set_trace()
                # there was an error while testing the hostname
                results["meta"]["errors"] += 1

        # dump the results
        with open("../Out/results_%s.json" % chunk.replace(".json",""), 'w') as fp:
            json.dump(results, fp, indent=4)

    #     # dump the meta results
    #     with open("exp%d_MetaResults.json" % exNum, 'w') as fp:
    #         json.dump(meta, fp, indent=4)


    #     pdb.set_trace()

    # # once we've finished with all the chunks, we're done. Increment the experiment number
    # with open("expNum.json", 'r+') as f:
    #     temp = json.load(f)
    #     temp["number"] += 1
    #     json.dump(temp, f, indent=4)c


def dns_req(url):
    # should we use only theses IPs?
    ips = ["111.13.101.208", "125.39.240.113", "61.135.157.156", "202.114.64.5", "166.111.4.100", "162.105.131.196", "202.120.224.115", "106.11.47.20", "140.207.228.45", "118.178.213.186", "218.62.26.196"]
    ans,unans = sr(IP(dst=ips[random.randint(0,len(ips)-1)])/UDP(dport=53)/DNS(rd=1,qd=DNSQR(qname=url)),verbose=0,multi=1,timeout=1)
    return ans

def reader(file_name):
    with open(file_name) as f:
        return json.load(f)

def test():
    ips = ["111.13.101.208", "125.39.240.113", "61.135.157.156", "202.114.64.5", "166.111.4.100", "162.105.131.196", "202.120.224.115", "106.11.47.20", "140.207.228.45", "118.178.213.186", "218.62.26.196"]

    for ip in ips:
        ans, unans = sr(IP(dst=ip)/UDP(dport=53)/DNS(rd=1,qd=DNSQR(qname="baidu.org")),verbose=0,multi=1,timeout=2)
        if (len(ans) != 0):
            print("Response received, %s is a DNS capable IP" % ip)
        else:
            print("%s passed the test" % ip)

# this is the function that will spawn all of the worker threads
def split():

    loc = "Inbound"
    processes = []
    counter = 0
    for chunk in os.listdir("../%s" % loc):
        counter += 1
        if (counter % 100 == 0):
            # wait for all threads to finish executing
            print("Waiting for spawned threads to finish")
            for proc in processes:
                proc.join()
            processes = []
            print("Done")

        new_process = threading.Thread(target=work, args=(chunk, loc, counter,))
        processes.append(new_process)
        new_process.start()

    

    # with open("../Results/expNum.json", 'r+') as f:
    #     temp = json.load(f)
    #     temp["number"] += 1
    #     json.dump(temp, f, indent=4)

if __name__ == "__main__":
    # main()
    # test()
    split()

# thought: after determining blocked domains, go back and build a list of the top 1M sights and which are blocked by china
# do it for top US sights too