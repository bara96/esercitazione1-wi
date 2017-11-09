from parteA import ParteA
from parteB import ParteB

c = 0
while not(c == 1 or c == 2 or c == 3):
    c = input("1)ParteA 2)ParteB 3)ParteC \n")

if c == 1:
    parteA = ParteA('http://www.reuters.com/')
    parteA.main()
if c == 2:
    parteB = ParteB()
    parteB.main()