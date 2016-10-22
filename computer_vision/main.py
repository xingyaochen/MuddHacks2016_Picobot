import cv2
from glyphdatabase import *
from glyphfunctions import *
from webcam import Webcam
import math

webcam = Webcam()
webcam.start()

QUADRILATERAL_POINTS = 4
SHAPE_RESIZE = 100.0
BLACK_THRESHOLD = 100
WHITE_THRESHOLD = 155

framenum = 0

while True:
    framenum += 1
    # Stage 1: Read an image from our webcam
    image = webcam.get_current_frame()

    # Stage 2: Detect edges in image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5,5), 0)
    edges = cv2.Canny(gray, 100, 200)

    # Stage 3: Find contours
    _, contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    glyph_found = False
    for contour in contours:

        # Stage 4: Shape check
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.01*perimeter, True)
        if len(approx) == QUADRILATERAL_POINTS:
            frame = approx.reshape(4, 2)

            # Stage 5: Perspective warping
            topdown_quad = get_topdown_quad(gray, frame)

            # Stage 6: Border check
            resized_shape = resize_image(topdown_quad, SHAPE_RESIZE)
            try:
                if resized_shape[5, 5] > BLACK_THRESHOLD: continue
            except Exception as e:
                print("There done be errors!")
                print(e)
                print(np.shape(resized_shape))
                continue

            # Stage 7: Glyph pattern
            # try:
            glyph_pattern = get_glyph_pattern(resized_shape, BLACK_THRESHOLD, WHITE_THRESHOLD)
            glyph_found, glyph_rotation, glyph_substitute = match_glyph_pattern(glyph_pattern)
            # except Exception as e:
            #     print("There done be errors!")
            #     print(e)
            #     continue

            if glyph_found:
                # Stage 8: Substitute glyph
                x, y = np.mean(frame[:,0]), np.mean(frame[:,1])
                c = np.array([x, y])
                dc = list(map(lambda item: item - c, list(frame)))
                dtr = sorted(dc , key=lambda x:x[0]*x[1])[-1]
                theta_q1 = math.atan(dtr[0]/dtr[1])/2/math.pi * 360 + (360 - 45)
                theta = (theta_q1 + 90 * glyph_rotation) % 360
                print("\r%6d   %4.4f %4.4f %4.4f"%(framenum, x,y, theta), end="")

            else:
                print("\r%6d dno glyph found"%framenum + " "*30, end="")
    cv2.imshow('2D Augmented Reality using Glyphs', edges)
    cv2.waitKey(10)
