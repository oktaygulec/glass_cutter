## GLOBAL VARIABLES ##
print("ENTER DIMENSIONS")
plate_width = 0
plate_height = 0
isPlateDimensionsOK = False
while isPlateDimensionsOK == False:
    plate_width = int(input("WIDTH: "))
    plate_height = int(input("HEIGHT: "))
    if plate_width < 1 or plate_height < 1:
        print("The dimensions you entered should be greater than 0. Enter again.")
        isPlateDimensionsOK = False
    else:
        isPlateDimensionsOK = True

plate = [[0 for i in range(plate_width)] for j in range(plate_height)]
cutGlassesList = []
totalUsedPlateAmount = 0
waste = 0


## FUNCTIONS ##


def create_glasses(amount):
    glasses = []
    i = 0
    while i < amount:
        print("------------------------------------------------------------")
        print("ENTER PRODUCT DIMENSIONS")
        glassWidth = int(input("WIDTH: "))
        glassHeight = int(input("HEIGHT: "))
        glass = [glassWidth, glassHeight]

        if glassWidth < 1 or glassHeight < 1:
            print("The dimensions you entered should be greater than 0. Enter again.")
            continue
        if glass[0] > plate_width or glass[1] > plate_height:
            rotatedGlass = [glass[1], glass[0]]
            if (rotatedGlass[0] > plate_width or rotatedGlass[1] > plate_height):
                i -= 1
                print(
                    "The dimensions you entered is bigger than the plate. Enter again.")
            else:
                glasses.append(rotatedGlass)
        else:
            glasses.append(glass)
        i += 1
    return glasses


def cut_glass(startX, endX, startY, endY, id):
    for i in range(startY, endY):
        for j in range(startX, endX):
            plate[i][j] = id


def find_next_cut_position(width, height):
    for i in range(plate_height):
        for j in range(plate_width):
            if plate[i][j] == 0:
                endX = j+width
                endY = i+height

                if endX <= plate_width and endY <= plate_height:
                    if plate[endY-1][endX-1] != 0:
                        break
                    else:
                        # returns the indexes
                        return [[j, i], [endX, endY]]
                else:
                    # rotate and try again
                    endX = i+width
                    endY = j+height
                    if endX <= plate_height and endY <= plate_width:
                        if plate[endX-1][endY-1] != 0:
                            break
                        else:
                            return [[j, i], [endY, endX]]
                    else:
                        i += 1
                        break
    # return -1 if its not a fit
    return -1


def calculate_remaining_space():
    counter = 0
    for i in range(plate_height):
        for j in range(plate_width):
            if plate[i][j] == 0:
                counter += 1
    return counter


def print_plate():
    print("_________________________________________________________________________")
    for i in range(plate_height):
        for j in range(plate_width):
            print(plate[i][j], end=" ")
        print()


# TEST DATAS #
# FOR TEST AND TO GET A NICE PRINT ON CLI (30, 10) #
# glasses = [
#     [5, 5], [20, 10], [3, 8], [4, 1], [15, 9], [2, 4], [4, 9],
#     [3, 5], [8, 1], [4, 4], [3, 3], [5, 5], [12, 3], [3, 3], [3, 1], [2, 1]
# ]

isAmountOK = False
amount = 0
while isAmountOK == False:
    amount = int(input("ENTER AMOUNT: "))
    if amount < 1:
        print("The amount you entered should be greater than 0. Enter again.")
        isAmountOK = False
    else:
        isAmountOK = True

glasses = create_glasses(amount)
sortedGlasses = sorted(glasses, reverse=True, key=lambda x: x[0]*x[1])
# PREPARE PLATES #
while len(sortedGlasses) > 0:
    i = 0
    counter = 1
    while i < len(sortedGlasses):
        pos = find_next_cut_position(sortedGlasses[i][0], sortedGlasses[i][1])
        if pos == -1:
            i += 1
            continue
        startX = pos[0][0]
        startY = pos[0][1]
        endX = pos[1][0]
        endY = pos[1][1]
        cut_glass(startX, endX, startY, endY, counter)
        sortedGlasses.pop(i)
        cutGlassesList.append({
            "plate": totalUsedPlateAmount + 1,
            "id": counter,
            "startX": startX,
            "endX": endX,
            "startY": startY,
            "endY": endY
        })
        counter += 1

    print_plate()
    totalUsedPlateAmount += 1
    waste = calculate_remaining_space()
    plate = [[0 for i in range(plate_width)] for j in range(plate_height)]
print("_________________________________________________________________________")
print("CUT GLASSES")
for cg in cutGlassesList:
    print(cg)
print("_________________________________________________________________________")
print("TOTAL USED PLATE AMOUNT: " + str(totalUsedPlateAmount))
print("WASTE/REMAINING SPACE (UNIT): " + str(waste) + " unit")
input("Application closing...")
