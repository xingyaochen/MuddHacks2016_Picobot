import cv2
from glyphdatabase import *
from glyphfunctions import *
from webcam import Webcam
import navigationClient
import math

webcam = Webcam()
webcam.start()

QUADRILATERAL_POINTS = 4
SHAPE_RESIZE = 100.0
BLACK_THRESHOLD = 190
WHITE_THRESHOLD = 230

framenum = 0

while True:
    framenum += 1
    # Stage 1: Read an image from our webcam
    image = webcam.get_current_frame()

    # Stage 2: Detect edges in image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3,3), 0)
    # gray = cv2.equalizeHist(gray)
    # gray = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
    edges = cv2.Canny(gray, 100, 200)

    # Stage 3: Find contours
    _, contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # contours = sorted(contours, key=cv2.contourArea, reverse=True)[:100]
    glyph_found = False
    quad_found = False
    for contour in contours:

        # Stage 4: Shape check
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.01*perimeter, True)
        if len(approx) == QUADRILATERAL_POINTS:
            quad_found = True
            frame = approx.reshape(4, 2)

            # Stage 5: Perspective warping
            topdown_quad = get_topdown_quad(gray, frame)
            # Stage 6: Border check
            try:
                resized_shape = resize_image(topdown_quad, SHAPE_RESIZE)
                if resized_shape[5, 5] > BLACK_THRESHOLD:
                    # print("\r%6d border failed %d"%(framenum, resized_shape[5, 5]) + " "*30, end="\n")
                    continue
            except Exception as e:
                # print("There done be errors!")
                # print(e)
                # print(np.shape(resized_shape))
                # print("\r%6d resize exception"%framenum + " "*30, end="\n")
                continue

            # Stage 7: Glyph pattern
            try:
                glyph_pattern = get_glyph_pattern(resized_shape, BLACK_THRESHOLD, WHITE_THRESHOLD)
                # print(glyph_pattern)
                glyph_found, glyph_rotation = match_glyph_pattern(glyph_pattern)
            except Exception as e:
                # print("There done be errors!")
                # print(e)
                # print("\r%6d no glyph pattern exception"%(framenum) + " "*30, end="\n")
                continue

            if glyph_found:
                # Stage 8: Substitute glyph
                x, y = np.mean(frame[:,0]), np.mean(frame[:,1])
                c = np.array([x, y])
                dc = list(map(lambda item: item - c, list(frame)))
                dtr = sorted(dc , key=lambda x:x[0]*x[1])[-1]
                theta_q1 = math.atan(dtr[0]/dtr[1])/2/math.pi * 360 + (360 - 45)
                theta = (theta_q1 + 90 * glyph_rotation) % 360
                navigationClient.socket_send_info(x, y, theta)
                print("\r%6d   %4.4f %4.4f %4.4f ========================="%(framenum, x,y, theta), end="\n")
            else:
                if not glyph_found:
                    # print("\r%6d no glyph found %s"%(framenum, glyph_pattern) + " "*30, end="\n")
                    glyph_found = True

    # if not quad_found:
    #     print("\r%6d no quads found"%framenum + " "*30, end="\n")
    cv2.imshow('2D Augmented Reality using Glyphs', edges)
    cv2.imshow('2D Augmented Reality using Glyphs2', gray)
    cv2.waitKey(10)
