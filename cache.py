from sys import argv
import os.path

class Cache:
    def __init__(self):
        self.cacheFile = "./seenProperties.csv"
        fileContents = str(self.readFile())
        self.cache = set(fileContents.split('\n'))

    def readFile(self):
        if os.path.isfile(self.cacheFile):
            with open(self.cacheFile, 'rb') as f:
                return f.read()
        else:
            return ''

    def appendToFile(self,sourceId):
        with open(self.cacheFile, "a") as myfile:
            myfile.write(sourceId + '\n')

        self.cache.add(sourceId)

    def markPropertyAsSeen(self,sourceId):
        self.appendToFile(sourceId)

    def haveSeenProperty(self,sourceId):
        return sourceId in self.cache

if __name__ == "__main__":
    self = Cache()
    print(self.haveSeenProperty("trev"))
    self.markPropertyAsSeen("trev")
    print(self.haveSeenProperty("trev"))
