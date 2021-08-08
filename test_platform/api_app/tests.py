from django.test import TestCase

# Create your tests here.

a = {"uid": 1}

pid = a.get("pid", "")

if pid == "":
    print("pid is null")


f = "hello.txt.csv"
bb = f[-3:-1]
print(bb)

# aa = f.split(".")[-1]
# print(aa)
