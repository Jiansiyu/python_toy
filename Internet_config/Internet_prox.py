'''
Created on Jul 1, 2017

@author: newdriver
'''
import json
from multiprocessing import Pool,Lock
from time import sleep

lock=Lock()

class Internet_prox(object):
    '''
    classdocs
    '''


    def __init__(self, prox_file=None):
        '''
        Constructor
        '''
        if prox_file is None:
            self.prox_filename='../Data/prox.txt'
        else:
            self.prox_filename=prox_file
            
    def GetProx(self):
        lock.acquire()
        with open(self.prox_filename,'r+') as proxfile:
            self.jsondata=json.load(proxfile)
            #print type(self.jsondata)
            #swiftdata=jsondata[1]
            #print swiftdata
            proxfile.close()
        
        #self.jsondata[0].append(self.jsondata[0])
        #del self.jsondata[0]
        jsondata_save=[]
        for i in self.jsondata:
            jsondata_save.append(i)
        
        jsondata_save.append(jsondata_save[0])
        jsondata_save.pop(0)
        #print len(jsondata_save)
        
        with open(self.prox_filename,'r+') as proxfile:
            json.dump(jsondata_save,proxfile)
            proxfile.close() 
        lock.release()
        print self.jsondata[0][0]+':'+str(self.jsondata[1][1])
        return self.jsondata[0][0]+':'+str(self.jsondata[1][1])
def run(runid):
    test = Internet_prox()
    test.GetProx(runid=runid)
        
if __name__ == '__main__':
   
    runpool=Pool(10)
    runpool.map(run,[1,2,3,4,5,6,7,8])