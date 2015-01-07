import Queue,threading,time,random  
  
class MsgQueue(object):
    """docstring for MsgQueue"""
    @classmethod
    def instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls()
        return cls._instance

    def __init__(self, threadnum = 1, timeout = 3):
        super(MsgQueue, self).__init__()
        self.queue = Queue.Queue()
        self.threadnum = threadnum
        self.stopped = True
        self.threads = []
        self.timeout = timeout
        pass


    def start(self):
        if self.running(): self.stop()
        self.stopped = False
        for x in xrange(0,self.threadnum):
            t = threading.Thread(target = lambda:MsgQueue.run(self))
            self.threads.append(t)
            t.start()
            pass
        pass

    def stop(self, wait = True):
        self.stopped = True
        if wait:
            for t in self.threads:
                if t.isAlive() : t.join()
        self.threads = []
        pass

    def put(self, func, *args):
        self.queue.put((func, args))
        pass

    def running(self):
        return  False == self.stopped

    def run(self):
        print 'run', threading.currentThread().name
        while True:
            try:
                do, args = self.queue.get(True, self.timeout)
                do(*args)
                self.queue.task_done()
            except Exception, e:
                if not self.running():
                    break
                pass
            finally:
                pass
            pass
        print 'run end', threading.currentThread().name
        pass

