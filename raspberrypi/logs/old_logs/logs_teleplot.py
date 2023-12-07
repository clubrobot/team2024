from multiprocessing import Process, Queue



def f(q):
    q.put([42, None, 'hello'])
    print(q.get(timeout=100))
    print("ngmgr")

if __name__ == '__main__':
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    print(q.get())    # prints "[42, None, 'hello']"
    q.put([42, None, 'test'])
    p.join()