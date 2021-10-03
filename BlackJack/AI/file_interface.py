class File:
    def __init__(self, name, manager):
        self.name = name
        self.number_of_readers = manager.Value('i', 0)
        self.reader_lock = manager.Lock()
        self.read_event = manager.Event()
        self.write_event = manager.Event()
        self.lock = manager.Lock()
        self.read_event.set()
        self.write_event.set()
    
    def read(self):
        self.write_event.wait()
        
        self.reader_lock.acquire()
        self.number_of_readers.value += 1
        self.reader_lock.release()

        self.read_event.clear()
        file = open(self.name, 'r')
        content = file.read()
        file.close()
        
        self.reader_lock.acquire()
        self.number_of_readers.value -= 1
        if self.number_of_readers.value == 0:
            self.read_event.set()
        self.reader_lock.release()

        return content
    
    def append(self, text):
        self.write_event.clear()
        self.read_event.wait()
        file = open(self.name, 'a')
        file.write(str(text))
        file.close()
        self.write_event.set()
