import threading
import os
from time import sleep, ctime, clock
from timeit import timeit, Timer
from math import ceil

class MyThread(threading.Thread):

    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self, name=name)
        self.func = func
        self.args = args
        self.count = 0

    def get_count(self):
        return self.count

    def run(self):
        self.count = self.func(*self.args)


def st_count_bytes(myfile, byte_val, filesize, lock):
    st = MyThread(count_bytes_in_chunk, args=(myfile, byte_val, 0, filesize, lock))
    st.start()
    st.join()

    return st.get_count()

# multi thread counter function
def mt_count_bytes(myfile, byte_val, start, chunk_size, lock, num_threads):
    # create threads
    threads = []
    for i in range(num_threads):
        t = MyThread(count_bytes_in_chunk, args=(myfile, byte_val, start[i], chunk_size, lock))
        threads.append(t)
    
    t1 = clock()
    for t in threads:
        t.start()
    print clock() - t1

    count = 0
    t1 = clock()
    print "t1 =", t1
    for t in threads:      # wait for all threads to finish
        t.join()
        print clock() - t1
        count += t.get_count()
        print t.name, 'finished at:', ctime()
        print t.name, 'count:', t.get_count()
    return count

# multithread helper function
def count_bytes_in_chunk(myfile, byte_val, start, chunk_size, lock):
    # lock allows for seek to work correctly
    myfile.seek(start)
    bytes = myfile.read(chunk_size)

    count = 0
    for byte in bytes:
        if byte == byte_val:
            count += 1
    return count

def count_bytes_in_file():
    # time single thread counter
    filename = raw_input("Enter the name of the file you wish to analyze: ")
    byte_val = raw_input("Enter byte value to count occurences in file: ") 

    myfile = open(filename, 'rb')
    filesize = os.path.getsize(filename)

    lock = threading.Lock()

    # time a single thread byte count
    t1 = clock()
    st_count = st_count_bytes(myfile, byte_val, filesize, lock)
    t2 = clock()
    print "Time for Single Thread: ", t2 - t1
    print "Count byte", byte_val, "occurences:", st_count

    # decides how big to make file segments
    num_threads = 10
    chunk_size = int(ceil(filesize/num_threads))+1
    start = [x for x in range(0, filesize, chunk_size)]

    # times multithreaded count of bytes
    t1 = clock()
    mt_count = mt_count_bytes(myfile, byte_val, start, chunk_size, lock, num_threads)
    t2 = clock()
    print "Time for Multithread:", t2 - t1
    print "Count byte", byte_val, "occurences:", mt_count 

    myfile.close()

if __name__ == '__main__':
    count_bytes_in_file()
