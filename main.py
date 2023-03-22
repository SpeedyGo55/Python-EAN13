import matplotlib.pyplot as plt
import numpy as np

decimal = "0"
leftOdd = [
    np.array([0, 0, 0, 1, 1, 0, 1]),  # 0
    np.array([0, 0, 1, 1, 0, 0, 1]),  # 1
    np.array([0, 0, 1, 0, 0, 1, 1]),  # 2
    np.array([0, 1, 1, 1, 1, 0, 1]),  # 3
    np.array([0, 1, 0, 0, 0, 1, 1]),  # 4
    np.array([0, 1, 1, 0, 0, 0, 1]),  # 5
    np.array([0, 1, 0, 1, 1, 1, 1]),  # 6
    np.array([0, 1, 1, 1, 0, 1, 1]),  # 7
    np.array([0, 1, 1, 0, 1, 1, 1]),  # 8
    np.array([0, 0, 0, 1, 0, 1, 1])  # 9
]
leftEven = [
    np.array([0, 1, 0, 0, 1, 1, 1]),  # 0
    np.array([0, 1, 1, 0, 0, 1, 1]),  # 1
    np.array([0, 0, 1, 1, 0, 1, 1]),  # 2
    np.array([0, 1, 0, 0, 0, 0, 1]),  # 3
    np.array([0, 0, 1, 1, 1, 0, 1]),  # 4
    np.array([0, 1, 1, 1, 0, 0, 1]),  # 5
    np.array([0, 0, 0, 0, 1, 0, 1]),  # 6
    np.array([0, 0, 1, 0, 0, 0, 1]),  # 7
    np.array([0, 0, 0, 1, 0, 0, 1]),  # 8
    np.array([0, 0, 1, 0, 1, 1, 1])  # 9
]
rightEven = [
    np.array([1, 1, 1, 0, 0, 1, 0]),  # 0
    np.array([1, 1, 0, 0, 1, 1, 0]),  # 1
    np.array([1, 1, 0, 1, 1, 0, 0]),  # 2
    np.array([1, 0, 0, 0, 0, 1, 0]),  # 3
    np.array([1, 0, 1, 1, 1, 0, 0]),  # 4
    np.array([1, 0, 0, 1, 1, 1, 0]),  # 5
    np.array([1, 0, 1, 0, 0, 0, 0]),  # 6
    np.array([1, 0, 0, 0, 1, 0, 0]),  # 7
    np.array([1, 0, 0, 1, 0, 0, 0]),  # 8
    np.array([1, 1, 1, 0, 1, 0, 0])  # 9
]
firstNumber = [
    np.array([0, 0, 0, 0, 0, 0]),  # 0
    np.array([0, 0, 1, 0, 1, 1]),  # 1
    np.array([0, 0, 1, 1, 0, 1]),  # 2
    np.array([0, 0, 1, 1, 1, 0]),  # 3
    np.array([0, 1, 0, 0, 1, 1]),  # 4
    np.array([0, 1, 1, 0, 0, 1]),  # 5
    np.array([0, 1, 1, 1, 0, 0]),  # 6
    np.array([0, 1, 0, 1, 0, 1]),  # 7
    np.array([0, 1, 0, 1, 1, 0]),  # 8
    np.array([0, 1, 1, 0, 1, 0])  # 9
]


def generate_checknumber():
    checknumber = 0
    number = str(input("Number (12 Digits): "))
    if len(number) != 12:
        print("WRONG")
    for i in range(0, 12):
        if i % 2 == 0 or i == 0:
            checknumber += int(number[i])
        else:
            checknumber += int(number[i]) * 3
    print(checknumber)
    checknumber = 10 - (checknumber % 10)

    if checknumber == 10:
        checknumber = 0
    print(checknumber)
    print(number + str(checknumber))
    return number + str(checknumber)


def check_ean13():
    checknumber = 0
    number = str(input("Number (13 Digits): "))
    information = number[:12]

    if len(information) != 12:
        print("WRONG LENGTH")
    for i in range(0, 12):
        if i % 2 == 0 or i == 0:
            checknumber += int(number[i])
        else:
            checknumber += int(number[i]) * 3
    print(checknumber)
    checknumber = 10 - (checknumber % 10)
    print(checknumber)
    if checknumber != int(number[12]):
        print("WRONG CHECKNUMBER")
        return False
    else:
        return number


def make_ean13(number):
    first_digit = number[:1]
    number = number[1:]
    left = number[:6]
    right = number[6:]
    code = np.array([0, 0, 0, 0, 0, 1, 0, 1])
    for i in range(6):
        if firstNumber[int(first_digit)][i] == 0:
            code = np.concatenate((code, leftOdd[(int(left[i]))]))
        else:
            code = np.concatenate((code, leftEven[(int(left[i]))]))
    code = np.concatenate((code, np.array([0, 1, 0, 1, 0])))
    for i in range(6):
        code = np.concatenate((code, rightEven[(int(right[i]))]))
    code = np.concatenate((code, np.array([1, 0, 1, 0, 0, 0, 0, 0])))
    pixel_per_bar = 5
    dpi = 100

    fig = plt.figure(figsize=(len(code) * pixel_per_bar / dpi, 2), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])  # span the whole figure
    ax.set_axis_off()
    ax.imshow(code.reshape(1, -1), cmap='binary', aspect='auto',
              interpolation='nearest')
    plt.show()


if input("Generate Checknumber? (y/n): ") == "y":
    make_ean13(generate_checknumber())
else: # check number
    number = check_ean13()
    if number != False:
        make_ean13(number)