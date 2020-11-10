import cv2
import numpy as np
import os
import math
import scipy.spatial
import scipy.ndimage
import scipy.signal
from scipy.signal import fftconvolve
from skimage import morphology, filters
import pandas as pd
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
os.system("cls||clear")


class estimateActivity:
    def testWithAString(self):  # this is just a very basic stub to prinout
        print("Check if this works")

    def countActivity(
        self, inputImage1, inputImage2, dataFrame1):
        inputImageA = inputImage1
        inputImageB = inputImage2
        dataFrameWithActivity = dataFrame1.copy()
        dataFrameWithActivity["activityStatus"] = ""
        for index, row in dataFrameWithActivity.iterrows():
            sub1 = cv2.GaussianBlur(
                inputImageA[row.bbox0:row.bbox2,row.bbox1:row.bbox3], (3, 3), 0.5
            )

            sub2 = cv2.GaussianBlur(
                inputImageB[row.bbox0:row.bbox2,row.bbox1:row.bbox3], (3,3), 0.5
            )
            
            sub1 = cv2.normalize(sub1, None, 0, 255, cv2.NORM_MINMAX)
            
            # result = cv2.matchTemplate(
            #     sub1.astype(np.uint8), sub2.astype(np.uint8), cv2.TM_CCOEFF_NORMED
            # )
            result = self.normxcorr2(sub1.astype(np.float64),sub2.astype(np.float64), mode="full")
            result[result<0]=0 
            result=1-result
            corrStrength = np.array([np.float32(result[sub1.shape[0]-1,sub1.shape[1]-1])])
            
            corrStrength = np.absolute(corrStrength)
            # result = cv2.matchTemplate(
            #     sub1.astype(np.uint8), sub2.astype(np.uint8), cv2.TM_CCOEFF_NORMED
            # )
            # corrStrength = np.array([result[0, 0]])
            # corrStrength[corrStrength < 0] = 0
            # corrStrength = np.absolute(corrStrength)

            dataFrameWithActivity["activityStatus"][index] = corrStrength
        return dataFrameWithActivity

    def normxcorr2(self,template, image, mode="full"):
    
            if np.ndim(template) > np.ndim(image) or  len([i for i in range(np.ndim(template)) if template.shape[i] > image.shape[i]]) > 0:
                pass

            template = template - np.mean(template)
            image = image - np.mean(image)

            a1 = np.ones(template.shape)
            ar = np.flipud(np.fliplr(template))
            out = scipy.signal.fftconvolve(image, ar.conj(), mode=mode)
            
            image = scipy.signal.fftconvolve(np.square(image), a1, mode=mode) - np.square(scipy.signal.fftconvolve(image, a1, mode=mode)) / (np.prod(template.shape))

            image[np.where(image < 0)] = 0

            template = np.sum(np.square(template))
            out = out / np.sqrt(image * template)

            out[np.where(np.logical_not(np.isfinite(out)))] = 0
    
            return out

    # # 2D convolution using the convolution's FFT property
    # def conv2(self,a,b):
    #     ma,na,_ = a.shape
    #     mb,nb,_ = b.shape
    #     return fft.ifft2(fft.fft2(a,[2*ma-1,2*na-1])*fft.fft2(b,[2*mb-1,2*nb-1]))

    # # compute a normalized 2D cross correlation using convolutions
    # # this will give the same output as matlab, albeit in row-major order
    # def normxcorr2(self,b,a):
    #     c = self.conv2(a,np.flipud(np.fliplr(b)))
    #     a = self.conv2(a**2, ones(b.shape))
    #     b = sum(b.flatten()**2)
    #     c = c/sqrt(a*b)
    #     return c




    # def normxcorr2(self, template, image):
    # # """
    # # Computes the normalised cross-correlation of matrices template and image.
    # # The matrix image must be larger than the matrix template
    # # The resulting matrix contains correlation coefficients and its values may range from -1.0 to 1.0.
    # # :param template: the smaller matrix to be cross-correlated with the image.
    # # :param image: the bigger matrix
    # # :return: N-D matrix contains correlation coefficients and its values may range from -1.0 to 1.0.
    # # """

    #     def shift_data(arr):
    #         min_arr = np.min(arr)
    #         if min_arr < 0:
    #             arr -= min_arr
    #         return arr

    #     def local_sum(A, m, n):
    #         B = np.pad(A, ((m, m), (n, n)), mode='constant', constant_values=0)
    #         s = np.cumsum(B, axis=0)
    #         c = s[m:-1, :] - s[:-m - 1, :]
    #         s = np.cumsum(c, axis=1)
    #         local_sum_A = s[:, n:-1] - s[:, :-n - 1]
    #         return local_sum_A

    #     if np.ndim(template) > np.ndim(image) or \
    #             len([i for i in range(np.ndim(template)) if template.shape[i] > image.shape[i]]) > 0:
    #         raise ValueError("Template larger than image. Arguments are swapped.")

    #     template = shift_data(template)
    #     image = shift_data(image)

    #     cross_corr = fftconvolve(np.rot90(template, 2), image)
    #     m, n = template.shape
    #     mn = m * n

    #     local_sum_A2 = local_sum(image ** 2, m, n)
    #     local_sum_A = local_sum(image, m, n)

    #     diff_local_sums = (local_sum_A2 - (local_sum_A ** 2) / mn)
    #     denom_A = np.sqrt(np.maximum(diff_local_sums, 0))

    #     denom_T = np.sqrt(mn - 1) * np.std(template, ddof=1)
    #     denom = denom_T * denom_A
    #     numerator = cross_corr - local_sum_A * template.sum() / mn

    #     out = np.zeros(numerator.shape)
    #     tol = np.sqrt(np.spacing(np.max(np.abs(denom))))
    #     i_nonzero = np.where(denom > tol)
    #     out[i_nonzero] = numerator[i_nonzero] / denom[i_nonzero]

    #     out[np.where((np.abs(out) - 1) > np.sqrt(np.spacing(1)))] = 0
    #     return out

if __name__ == "__main__":
    estimateActivity().testWithAString()
    out=estimateActivity().normxcorr2(cv2.imread(r'C:\Users\drink\Desktop\Nemalife-Python-GUI\model\analysismodules\onion.png',cv2.IMREAD_GRAYSCALE), cv2.imread(r'C:\Users\drink\Desktop\Nemalife-Python-GUI\model\analysismodules\pears.png',cv2.IMREAD_GRAYSCALE))
    print("abc")
    # inputImage = cv2.imread("croppedImage.jpg")
    # unpickled_df1 = pd.read_pickle("pandasFrame1Pickled.pkl")

    # unpickled_df1.columns = (
    #     unpickled_df1.columns.str.strip()
    #     .str.lower()
    #     .str.replace(" ", "_")
    #     .str.replace("(", "")
    #     .str.replace(")", "")
    #     .str.replace("-", "")
    # )
    # colorInputImage = inputImage#np.stack((np.array(inputImage),) * 3, -1)
    # mixedImage = np.fliplr(cv2.imread("croppedImage.jpg"))
    # mixedImage[:, 700:900] = mixedImage[:, 710:910]
    # mixedImage[:, 1:200] = 0
    # newTable = estimateActivity().countActivity(
    #     inputImage, mixedImage, unpickled_df1)
    # for index, row in newTable.iterrows():
    #         print(row.activityStatus)
    #         cv2.rectangle(
    #             colorInputImage,
    #             (row.bbox1, row.bbox0),
    #             (row.bbox3, row.bbox2),
    #             plt.cm.jet(row.activityStatus)[:,:3][0]*255,
    #             2,
    #         )
      

    # cv2.imshow("withObjects", colorInputImage)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

