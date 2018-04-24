from scapy.all import *
import json, sys, os, pdb, random, re

def prime():
    exNum = -1

    os.chdir("../Results")
    with open("expNum.json") as f:
        temp = json.load(f)
        exNum = temp["number"]

    # pdb.set_trace()
    if ("exp%d_MetaResults.json" % exNum not in os.listdir())
        # we need to create it
        out = {"tried" : 0, "allowed" : 0, "blocked" : 0, "errors" : 0}
        with open ("exp%d_MetaResults.json" % exNum, 'w') as fp:
                json.dump(out, fp, indent=4)

    return exNum

def main():

    exNum = prime()
    
    for chunk in os.listdir("../Parsed")
        with open("../Parsed/%s" % chunk, "r") as f:
            with open("../Parsed/%s" % chunk, "r") as m:
                hostnames = json.load(f)
                meta = json.load(m)

                results = {}
                #hostnames = ["www.falundafa.org","www.yahoo.com"]
                for hostname in hostnames:
                    try:
                        ans = dns_req(hostname)
                        if (len(ans)>=1):
                            # it's blocked
                            meta["blocked"] += 1
                            # removing this to decrease json size:
                            # results[hostname]["blocked"] = True
                            # if it's present in the results dict, we know it was blocked. If it's not, it's not blocked
                            ipid = ans[len(ans)-1][1][IP].id
                            ttl = ans[len(ans)-1][1][IP].ttl
                            results[hostname]["ttl"] = ttl
                            results[hostname]["ipid"] = ipid
                            results[hostname]["responses"] = len(ans)
                        else:
                            # it's not blocked
                            meta["allowed"] += 1

                        # it was tested successfully
                        meta["tried"] += 1

                    except Exception as exception:
                        with open("../Logs/Experiment_%s.log" % str(exNum), 'a') as log:
                            name = repr(exception).split('(')[0]
                            print("%s exception encountered while testing %s" % (name, hostname))
                            log.write("%s exception encountered while testing %s" % (name, hostname))
                        # there was an error while testing the hostname
                        meta["errors"] += 1

        # dump the results
        with open("results_%s.json" % chunk, 'w') as fp:
            json.dump(results, fp, indent=4)

        # dump the meta results
        with open("exp%d_MetaResults.json" % exNum, 'w') as fp:
            json.dump(meta, fp, indent=4)


        pdb.set_trace()

def dns_req(url):
    # should we use only theses IPs?
    ips = ["111.13.101.208", "125.39.240.113", "61.135.157.156", "202.114.64.5", "166.111.4.100", "162.105.131.196", "202.120.224.115", "106.11.47.20", "140.207.228.45", "118.178.213.186", "218.62.26.196"]
    ans,unans = sr(IP(dst=ips[random.randint(0,len(ips)-1)])/UDP(dport=53)/DNS(rd=1,qd=DNSQR(qname=url)),verbose=0,multi=1,timeout=5)
    return ans

def reader(file_name):
    with open(file_name) as f:
        return json.load(f)

if __name__ == "__main__":
    main()

# thought: after determining blocked domains, go back and build a list of the top 1M sights and which are blocked by china
# do it for top US sights too