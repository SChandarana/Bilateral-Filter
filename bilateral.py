import cv2

def main():
    image1 = 'test1.png'
    image2 = 'test2.png'
    sigmaS = 10
    sigmaI = 0.1
    diameter = 20
    source = cv2.imread(image1,cv2.IMREAD_UNCHANGED)
    highSpace = cv2.bilateralFilter(source,diameter, 20, 1000)
    lowSpace = cv2.bilateralFilter(source,diameter, 20, 1)
    highInt = cv2.bilateralFilter(source,diameter, 1000, 20)
    lowInt = cv2.bilateralFilter(source,diameter, 1, 20)
    lowD = cv2.bilateralFilter(source,3, 80, 80)
    highD = cv2.bilateralFilter(source,diameter, 80, 80)
    cv2.imwrite("highS.jpg", highSpace)
    cv2.imwrite("lowS.jpg", lowSpace)
    cv2.imwrite("highI.jpg", highInt)
    cv2.imwrite("lowI.jpg", lowInt)
    cv2.imwrite("highD.jpg", highD)
    cv2.imwrite("lowD.jpg", lowD)
    source2 = cv2.imread(image2)
    best = cv2.bilateralFilter(source2,diameter, 40, 10)
    cv2.imwrite("best.jpg",best)

        
main()
