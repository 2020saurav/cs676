import cv2
import pymeanshift as ms

img_name = "test"
original_image = cv2.imread(img_name + ".png")
sk = "Gaussian"
rk = "Gaussian" # other : Uniform
i = 1
for sr in range(2,20,8):
    for rr in range(2,20,8):
        for m in range(1,50,10):
            (segmented_image, labels_image, number_regions) \
                = ms.segment(original_image, spatial_radius=sr,
                    range_radius=rr, min_density=m,
                    skernel=sk, rkernel=rk)

            cv2.imwrite(img_name+"_" + sk[0] + rk[0] +"_"+str(i)+".jpg", segmented_image)
            print i,'\t',sr,'\t',rr,'\t',m, '\t'+sk[0]+'\t'+rk[0]+'\t', number_regions
            i+=1

