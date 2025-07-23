import random

answers = random.sample([1,2,3,4,5],5)
while True:
    inp = input("guess the order: \n")
    g = [int(i) for i in inp.split()]

    c = sum([a == b for a, b in zip(answers, g)])
    print(f"Your score: {c} out of 5")
    if c == 5:
        print("Congratulations! You've guessed the correct order!")
        break
    else:
        print("Try again!")