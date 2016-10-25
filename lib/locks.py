import multiprocessing, os.path, json

CLUSTERS = "clusters"
ID = "id"

class Locks:
    def __init__(s, lockFileName):
        s.lockFileName = lockFileName
        s.mutex = multiprocessing.Lock()
        s.clean()

    def clean(s):
        s.lockData = None
        s.lockClusters = None
        s.nextId = None

    def acquire(s):
        s.mutex.acquire()
        if not os.path.isfile(s.lockFileName):
            with open(s.lockFileName, "wb") as lockFile:
                lockFile.write("{}")
        with open(s.lockFileName, "rb") as lockFile:
            s.lockData = json.load(lockFile)
        if not s.lockData.has_key(ID):
            s.lockData[ID] = 0
        s.nextId = s.lockData[ID] + 1
        if not s.lockData.has_key(CLUSTERS):
            s.lockData[CLUSTERS] = {}
        s.lockClusters = s.lockData[CLUSTERS]

    def write(s):
        with open(s.lockFileName, "wb") as lockFile:
            json.dump(s.lockData, lockFile)

    def release(s):
        s.clean()
        s.mutex.release()

    def strNextId(s):
        return "id{0}".format(s.nextId)

    def hasCluster(s, cluster):
        return s.lockClusters.has_key(cluster)

    def size(s, cluster):
        count = 0
        if s.hasCluster(cluster):
            for id, data in s.lockClusters[cluster].iteritems():
                count = count + len(data)
        return count

    def items(s, cluster):
        items = []
        if s.hasCluster(cluster):
            for id, data in s.lockClusters[cluster].iteritems():
                items = items + data
        return items

    def addItems(s, cluster, items):
        s.lockData[ID] = s.nextId
        if not s.hasCluster(cluster):
            s.lockClusters[cluster] = {}
        s.lockClusters[cluster][s.strNextId()] = items

    def removeItems(s, strId):
        found = False
        for clusterName, clusterData in s.lockClusters.iteritems():
            if clusterData.has_key(strId):
                del clusterData[strId]
                found = True
        return found
