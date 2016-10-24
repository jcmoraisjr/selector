import json

class Clusters:
    def __init__(s, clustersFile="", clustersInline=""):
        if clustersFile != "":
            with open(clustersFile, "rb") as f:
                s.clustersData = json.load(f)
        elif clustersInline != "":
            s.clustersData = json.loads(clustersInline)
        else:
            raise Exception("Either --cluster-file or --cluster-inline must be declared")

    def hasCluster(s, cluster):
        return s.clustersData.has_key(cluster)

    def size(s, cluster):
        return len(s.clustersData[cluster])

    def acquireUnlocked(s, qty, cluster, lockItems):
        if qty <= 0:
            return []
        availItems = []
        i = 0
        for item in s.clustersData[cluster]:
            if not item in lockItems:
                availItems = availItems + [item]
                i = i + 1
                if i == qty:
                    break
        return availItems
