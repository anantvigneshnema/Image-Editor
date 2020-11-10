import cv2
import numpy as np
from scipy import ndimage, misc
from scipy.ndimage.filters import gaussian_filter
from skimage.morphology import extrema, local_maxima
import pandas as pd
from itertools import product
from skimage.measure import label, regionprops

# input should be grey image
class returnCircles:
      
     def setInputGreyImage(self,greyImage):
          self.inputGreyImage = greyImage

     def calculateImageGradient(self, inputImage):
          # input image is logical
          kernelGaussian = cv2.getGaussianKernel(5,1.5)
          kernelg = np.outer(kernelGaussian, kernelGaussian.transpose())
          #kernelg = np.outer(kernelGaussian[0], kernelGaussian[1]) 
          inputImage = cv2.filter2D(inputImage,-1,kernelg,borderType = cv2.BORDER_REPLICATE)
          sobely = cv2.getDerivKernels(1,0,3)
          kernely = np.outer(sobely[0], sobely[1])    
          gyImage = cv2.filter2D(inputImage,-1, cv2.flip(kernely,-1),borderType = cv2.BORDER_REPLICATE)
          gyImage = gyImage.astype(np.float32)
          sobelx = cv2.getDerivKernels(0,1,3)
          kernelx = np.outer(sobelx[0], sobelx[1])    
          gxImage = cv2.filter2D(inputImage,-1, cv2.flip(kernelx,-1),borderType = cv2.BORDER_REPLICATE)
          gxImage = gxImage.astype(np.float32)
          gImage = np.sqrt(gxImage*gxImage+gyImage*gyImage)
          return gxImage, gyImage, gImage
          
     def getEdgePixels(self, gImage):
          Gmax = np.max(gImage)
          gImage = gImage/Gmax*255
          rImage = cv2.normalize(gImage,None, 0, 255, cv2.NORM_MINMAX,cv2.CV_8U)
          ret, thresh1 = cv2.threshold(rImage,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU) 
          self.indices = np.where(gImage > ret/255*Gmax)
          self.rowColumnArray = np.column_stack(self.indices)

     def setRadiusRange(self, lowRadius,hiRadius):
         self.radiusRange = np.arange(lowRadius,hiRadius+0.1, 0.5)

     def computeVotesBasedOnPhaseCode(self):
         lnR = np.log(self.radiusRange)
         phi = ((lnR -lnR[0])/(lnR[-1]-lnR[0])*2*np.pi)-np.pi
         oPCA = np.exp(1j*phi)
         self.wO = oPCA/(2*np.pi*self.radiusRange)

     def computeAccumulatorArray(self, gxImage1, gyImage1, gImage1):
        xcStep = np.floor(10**6/len(self.radiusRange))
        lnE = len(self.rowColumnArray) 
        rows_image = len(self.inputGreyImage)
        columns_image =  len(self.inputGreyImage[0])
        self.accumMatrix = np.zeros_like(self.inputGreyImage)
        linearIndex = np.ravel_multi_index(self.indices, self.accumMatrix.shape,order = 'F')
        
        
        for i in range(0,lnE,int(xcStep)):
          Ex_chunk = self.indices[1][i:int(min(i+xcStep,lnE-1))]
          Ey_chunk = self.indices[0][i:int(min(i+xcStep,lnE-1))]
          idxE_chunk = linearIndex[i:int(min(i+xcStep,lnE-1))]
          
          xc = np.round(Ex_chunk.reshape(-1,1)+self.radiusRange*(gxImage1[np.unravel_index(idxE_chunk,gxImage1.shape,'F')]/gImage1[np.unravel_index(idxE_chunk,gImage1.shape,'F')]).reshape(-1,1))
          yc = np.round(Ey_chunk.reshape(-1,1)+self.radiusRange*(gyImage1[np.unravel_index(idxE_chunk,gyImage1.shape,'F')]/gImage1[np.unravel_index(idxE_chunk,gImage1.shape,'F')]).reshape(-1,1))
          
          w = np.repeat([self.wO],len(xc),axis=0)

          inside = ((xc >= 0 ) * (xc < columns_image) * (yc >= 0) * (yc < rows_image))

          #columnWiseSum = (np.sum(inside,axis=1)).reshape(-1,1)
          xc = xc[np.any(inside,axis =1)]
          yc = yc[np.any(inside,axis =1)]
          w =  w[np.any(inside,axis =1)]
          inside = inside[np.any(inside, axis = 1)].astype(int)
          inside = np.ravel(inside, order = 'F')
          xc = np.ravel(xc, order='F')
          yc = np.ravel(yc, order='F')
          w = np.ravel(w, order='F')  
          xc = xc[inside > 0 ]
          yc = yc[inside > 0 ]
          w = w[inside > 0 ]
          #arr = np.concatenate((xc.reshape(-1,1), yc.reshape(-1,1)), axis=1).astype(int)
          #np.ravel_multi_index((xc.astype(int),yc.astype(int)), np.flip(gImage1.shape),order = 'F')

          val = (np.arange(101, 106+1))
          subs = np.array([[0, 0], [1, 1], [2, 1], [0, 0], [1, 1], [3, 0]])
          #indus = self.accum(subs,val,size = [4, 4])
          out = self.accum(np.concatenate((yc.reshape(-1,1), xc.reshape(-1,1)), axis=1).astype(int),w,size = [rows_image, columns_image])
          # tempArray = self.accumarray(pd.DataFrame(np.concatenate((yc.reshape(-1,1), xc.reshape(-1,1)), axis=1).astype(int).tolist()),pd.Series(w), size = [rows_image, columns_image]) 
          self.accumMatrix = self.accumMatrix + out
          xc = yc = w = None
        return self.accumMatrix, gImage1
          
     def chcenter(self):
         accumMatrix, gImage1 = gImage1self.computeAccumulatorArray()



     def accumarray(self,subs, val, size=None, fun=np.sum):
        if len(subs.shape) == 1:
            if size is None:
                size = [subs.values.max() + 1, 0]

            acc = val.groupby(subs).agg(fun)
        else:
            if size is None:
                size = [subs.values.max()+1, subs.shape[1]]

            subs = subs.copy().reset_index()
            by = subs.columns.tolist()[1:]
            
            dataFrameObj = subs.groupby(by=by)['index'].apply(list)
            dataFrameObj.apply(lambda x: val[x].sum())
            for index, item in enumerate(dataFrameObj.items()):
                dataFrameObj.iloc[index] = sum(val[dataFrameObj.iloc[index]])
                #print(index)
            acc = dataFrameObj
            #acc = dataFrameObj.apply(lambda x: val[x].agg(fun))
            acc = acc.to_frame().reset_index().pivot_table(index=0, columns=1, aggfunc='first')
            acc.columns = range(acc.shape[1])
            acc = acc.reindex(range(size[1]), axis=1).fillna(0)

        id_x = range(size[0])
        acc = acc.reindex(id_x).fillna(0)

        return acc

     def accumfindcenters(self,acc, senstivity):
         accumMatrix = np.absolute(acc) # accumulator array
         sigma  = 0.5
         kernel = int(2*np.ceil(2*sigma)+1)
         accumMatrix = cv2.GaussianBlur(accumMatrix , (kernel,kernel),sigmaX=0.5)
         senstivity = 0.93 # default
         Hd = cv2.medianBlur(accumMatrix.astype('float32'),5)
         accumThresh = 1-senstivity
         suppThreshold = np.max(accumThresh-  np.spacing(accumThresh),0)
         Hd = extrema.h_maxima(Hd, suppThreshold)
         bw = (local_maxima(Hd)).astype(int)
         label_img = label(bw, connectivity=bw.ndim)
         s = regionprops(label_img, intensity_image=accumMatrix)
         center = np.empty([len(s),2])
         metric = np.empty([len(s),1])
         for index,i in enumerate(s):
           center[index] = tuple((np.array(s[index].centroid)).astype(int))
           metric[index] = Hd[tuple((np.array(s[index].centroid)).astype(int))]
         return center, metric



     def accum(self,accmap, a, func=None, size=None, fill_value=0, dtype=None):
                """
                An accumulation function similar to Matlab's `accumarray` function.

                Parameters
                ----------
                accmap : ndarray
                    This is the "accumulation map".  It maps input (i.e. indices into
                    `a`) to their destination in the output array.  The first `a.ndim`
                    dimensions of `accmap` must be the same as `a.shape`.  That is,
                    `accmap.shape[:a.ndim]` must equal `a.shape`.  For example, if `a`
                    has shape (15,4), then `accmap.shape[:2]` must equal (15,4).  In this
                    case `accmap[i,j]` gives the index into the output array where
                    element (i,j) of `a` is to be accumulated.  If the output is, say,
                    a 2D, then `accmap` must have shape (15,4,2).  The value in the
                    last dimension give indices into the output array. If the output is
                    1D, then the shape of `accmap` can be either (15,4) or (15,4,1) 
                a : ndarray
                    The input data to be accumulated.
                func : callable or None
                    The accumulation function.  The function will be passed a list
                    of values from `a` to be accumulated.
                    If None, numpy.sum is assumed.
                size : ndarray or None
                    The size of the output array.  If None, the size will be determined
                    from `accmap`.
                fill_value : scalar
                    The default value for elements of the output array. 
                dtype : numpy data type, or None
                    The data type of the output array.  If None, the data type of
                    `a` is used.

                Returns
                -------
                out : ndarray
                    The accumulated results.

                    The shape of `out` is `size` if `size` is given.  Otherwise the
                    shape is determined by the (lexicographically) largest indices of
                    the output found in `accmap`.


                Examples
                --------
                >>> from numpy import array, prod
                >>> a = array([[1,2,3],[4,-1,6],[-1,8,9]])
                >>> a
                array([[ 1,  2,  3],
                    [ 4, -1,  6],
                    [-1,  8,  9]])
                >>> # Sum the diagonals.
                >>> accmap = array([[0,1,2],[2,0,1],[1,2,0]])
                >>> s = accum(accmap, a)
                array([9, 7, 15])
                >>> # A 2D output, from sub-arrays with shapes and positions like this:
                >>> # [ (2,2) (2,1)]
                >>> # [ (1,2) (1,1)]
                >>> accmap = array([
                        [[0,0],[0,0],[0,1]],
                        [[0,0],[0,0],[0,1]],
                        [[1,0],[1,0],[1,1]],
                    ])
                >>> # Accumulate using a product.
                >>> accum(accmap, a, func=prod, dtype=float)
                array([[ -8.,  18.],
                    [ -8.,   9.]])
                >>> # Same accmap, but create an array of lists of values.
                >>> accum(accmap, a, func=lambda x: x, dtype='O')
                array([[[1, 2, 4, -1], [3, 6]],
                    [[-1, 8], [9]]], dtype=object)
                """

                # Check for bad arguments and handle the defaults.
                if accmap.shape[:a.ndim] != a.shape:
                    raise ValueError("The initial dimensions of accmap must be the same as a.shape")
                if func is None:
                    func = np.sum
                if dtype is None:
                    dtype = a.dtype
                if accmap.shape == a.shape:
                    accmap = np.expand_dims(accmap, -1)
                adims = tuple(range(a.ndim))
                if size is None:
                    size = 1 + np.squeeze(np.apply_over_axes(np.max, accmap, axes=adims))
                size = np.atleast_1d(size)

                # Create an array of python lists of values.
                vals = np.empty(size, dtype='O')
                for s in product(*[range(k) for k in size]):
                    vals[s] = []
                for s in product(*[range(k) for k in a.shape]):
                    indx = tuple(accmap[s])
                    val = a[s]
                    vals[indx].append(val)

                # Create the output array.
                out = np.empty(size, dtype=dtype)
                for s in product(*[range(k) for k in size]):
                    if vals[s] == []:
                        out[s] = fill_value
                    else:
                        out[s] = np.sum(vals[s])

                return out


    