from ParteA import ParteA

c = 0
while not(c == 1 or c == 2 or c == 3):
    c = input("1)ParteA 2)ParteB 3)ParteC \n")

if c == 1:
    parteA = ParteA()
    parteA.main()