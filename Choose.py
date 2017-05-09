##Choose written by Dogpetkid
##Prompts a question (q) with 2 choices (oop1 and oop2)
##and returns a string (str = 1) or integer (str = 0)
##Note, oop1 and oop2 must be strings even if an integer is returned
def choose2(q,oop1,oop2,str):
    choice = ''
    c1 = oop1
    c2 = oop2
    while (choice != oop1 and choice != oop2):
        print (q + " (" + (c1) + " or " + (c2) + ")")
        choice = input()
    if (str == 0):
        choice = int(choice)
    return choice

##Promts a question with 3 choices
def choose3(q,oop1,oop2,oop3,str):
    choice = ''
    c1 = oop1
    c2 = oop2
    c3 = oop3
    while (choice != oop1 and choice != oop2 and choice != oop3):
        print (q + " (" + (c1) + " or " + (c2) + " or " + (c3) + ")")
        choice = input()
    if (str == 0):
        choice = int(choice)
    return choice

##Checks if a value is anywhere in an array
def check(choice,oop,i):
    bool = False
    while i>0:
        if choice == str(oop[i-1]):
            bool = True
        i = i - 1
    return bool

##Checks if there is a value anywhere that is not the same
def same(choice,oop,i):
    bool = True
    while i>0:
        if choice != str(oop[i-1]):
            bool = False
        i = i - 1
    return bool


##Prompts a question with n choices where oopn is an array of strings
def choosen(q,oopn,str):
    choice = ''
    n = len(oopn)
    i = n
    while (False == check(choice,oopn,n)):
        i = n
        print (q + " Choose from...:")
        while i > 0:
            print(oopn[i-1])
            i = i - 1
        choice = input()
    if (str == 0):
        choice = int(choice)
    return choice

##Prompts a question but does not give options
def chooseh(q,oopn,str):
    choice = ''
    n = len(oopn)
    i = n
    while (False == check(choice,oopn,n)):
        i = n
        print (q)
        choice = input()
    if (str == 0):
        choice = int(choice)
    return choice
