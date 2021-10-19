import time
from time import sleep, ctime
import threading


def movie(name):
    print(f"movie run start{name}")
    sleep(5)
    print("movie running end")


def music():
    print("music run start")
    sleep(3)
    print("music running end")


threads = []
t1 = threading.Thread(target=movie, args=('长津湖',))
threads.append(t1)

t2 = threading.Thread(target=music)
threads.append(t2)

print(ctime())

for t in threads:
    t.start()

for t in threads:
    t.join()

print(ctime())

# print(ctime())
# movie()
# music()
# print(ctime())
