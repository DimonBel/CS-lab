import random

iteration = {
    1: 1,
    2: 1,
    3: 2,
    4: 2,
    5: 2,
    6: 2,
    7: 2,
    8: 2,
    9: 1,
    10: 2,
    11: 2,
    12: 2,
    13: 2,
    14: 2,
    15: 2,
    16: 1,
}

print(iteration.keys())
print(iteration[16])

k_random = ""

while len(k_random) < 56:
    # добавляем случайно выбранный символ 0 или 1
    k_random += str(random.randint(0, 1))

print(len(k_random))
print(k_random)

kplus = input("Enter kplus value: ")
if len(kplus) == 56:

    print(iteration)
    print(kplus)

    c0 = ""
    d0 = ""
    for i in range(len(kplus) // 2):
        c0 += str(kplus[i])

    for i in range(len(kplus) // 2):
        d0 += str(kplus[i + len(kplus) // 2])

    print(c0)
    print(d0)

    i_value = int(input("Write i value: "))
    if i_value < 17 and i_value > 1:
        print("i value is correct")
        count = 0
        for i in iteration.keys():
            if i <= i_value:
                count += iteration.get(i)
                print(iteration.get(i))
            else:
                break

        print("-------------------------------")
        print(iteration.get(i_value))

        print("-------------------------------")
        print(count)

        c_new = c0[count:] + c0[:count]
        d_new = d0[count:] + d0[:count]

        print(c_new + " C of iteration: " + str(i_value))
        print(d_new + " D of iteration: " + str(i_value))

        for i in range(i_value + 1):
            c_all = c0[i:] + c0[:i]
            d_all = d0[i:] + d0[:i]
            print("-------------------------------")
            print(c_all + " C iteration: of " + str(i))
            print(d_all + " D iteration: of " + str(i))
    else:
        print("i value must be between 1 and 16")

else:
    print("kplus must be 56 characters long")
