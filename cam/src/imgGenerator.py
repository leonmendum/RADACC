import random

import cv2.cv2 as cv
import numpy as np

# demonstrate readlines()

import cv2  # Not actually necessary if you just want to create an image.

blank_image = np.zeros((4000, 4000, 3), np.uint8)
blank_image[:] = (245, 245, 245)

# paint rooms:
rooms = [((100, 100), (2500, 1000)),
         ((1500, 1000), (3250, 3500)),
         ((3250, 1000), (3750, 3000)),
         ((250, 1000), (1500, 2500)),
         ((2500, 250), (3750, 1000))]
count = 1
for room in rooms:
    # colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    colour = (0, 0, 0)
    cv.rectangle(blank_image, room[0], room[1], colour, 3)
    textCoordsX = int(room[0][0] + ((room[1][0] - room[0][0]) / 2))
    textCoordsY = int(room[0][1] + ((room[1][1] - room[0][1]) / 2))
    print(f"room: {room}, center: {(textCoordsX, textCoordsY)}")
    cv.putText(blank_image, f"Room {count}", (textCoordsX, textCoordsY),
               cv.FONT_HERSHEY_SIMPLEX, 0.5, colour, 2)

    count += 1

cv.imshow("blankMap", blank_image)

cv2.imwrite('../../visuals/roomMap.png', blank_image)
print("")


key = cv.waitKey(0)
# if the `q` key was pressed, break from the loop
cv.destroyAllWindows()
