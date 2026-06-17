from time import *
import random as r

def mistake(par, usertest):
    cnt = 0
    for i in range (len(par)):
        try:
            if par[i] != usertest[i]:
                cnt += 1
        except:
            cnt += 1
    return cnt
def speed(time_s, time_e, user_t):
    time3 = time_e - time_s
    time3 = round(time3, 2)
    speed = len(user_t) / time3
    return round(speed, 2)
while True:
    ch = input("Do you want to start the typing speed calculator? (y/n): ")
    if ch.lower() == 'y':
        test = ["hello guyz welcome to typing speed calculator", "my name is daksh", "welcome to the python world"]
        test1 = r.choice(test)
        print("*****typing speed calculator*****")
        print(test1)
        print()
        print()
        time1 = time()
        test2 = input("Start typing here for the speed testing:")
        time2 = time()
        print("speed:", speed(time1, time2, test2), "W/Sec")
        print("errors:" ,mistake(test1, test2))
        print("accuracy:", round((1 - (mistake(test1, test2) / len(test1))) * 100, 2), "%")
    elif ch.lower() == 'n':
        print("Exiting the typing speed calculator. Goodbye!")
        break
    else:
        print("Invalid input. Please enter 'y' to start or 'n' to exit.")