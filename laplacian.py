# USAGE
# python detect_blur.py --images images

# import the necessary packages
from imutils import paths
import argparse
import cv2

def variance_of_laplacian(image):
    # compute the Laplacian of the image and then return the focus
    # measure, which is simply the variance of the Laplacian
    return cv2.Laplacian(image, cv2.CV_64F).var()


def notblurry():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--images", required=True,
                    help="path to input directory of images")
    ap.add_argument("-t", "--threshold", type=float, default=100.0,
                    help="focus measures that fall below this value will be considered 'blurry'")
    #args = vars(ap.parse_args())
    args = {'images': 'origin', 'threshold': 100.0}
    #print(type(args))

    # loop over the input images
    #for imagePath in paths.list_images(args["images"]):
    for imagePath in paths.list_images("./origin/"):
        # load the image, convert it to grayscale, and compute the
        # focus measure of the image using the Variance of Laplacian
        # method
        image = cv2.imread(imagePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        fm = variance_of_laplacian(gray)
        text = "Not Blurry"
        
        # if the focus measure is less than the supplied threshold,
        # then the image should be considered "blurry"
        #if fm < args["threshold"]:
            #text = "Blurry"
            
        # if not blurry show the image and another save it.
        #cv2.putText(image, "{}: {:.2f}".format(text, fm), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
        #cv2.imshow("Image", image)
        if fm > args["threshold"]:
            #cv2.imshow("Image", image)
            cv2.imwrite("./result/notblurry.png", image)
            #key = cv2.waitKey(0)
        else:
            print("[INFO] 圖像無法識別請於提示音後重新操作")
