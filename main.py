# !pip install -q transformers
from transformers import CLIPSegProcessor, CLIPSegForImageSegmentation
from PIL import Image
import requests
# from google.colab.patches import cv2_imshow
import cv2
import os
from PIL import Image
import requests
from fastapi.responses import RedirectResponse
import torch
import uvicorn
import torchvision

from fastapi import FastAPI

app = FastAPI()


processor = CLIPSegProcessor.from_pretrained("CIDAS/clipseg-rd64-refined")
model = CLIPSegForImageSegmentation.from_pretrained("CIDAS/clipseg-rd64-refined")


def promptencoder(prompt_path):
    prompt_image_list=[]
    encoded_prompt_avg=0
    # img=[]
    for i in os.listdir(prompt_path):
        image=cv2.imread(prompt_path+"/"+i)
        prompt_image_list.append(image)
    encoded_prompt_avg+= processor(images=image , return_tensors="pt").pixel_values
    encoded_prompt_avg=encoded_prompt_avg/len(os.listdir(prompt_path))
    return prompt_image_list,encoded_prompt_avg

@app.get("/")
def root():
    paths = "D:\zeroshotapp\my-app\static\cropped"
    os.mkdir(paths) 
    target_path="D:\zeroshotapp\my-app\static\query"
    prompt_path="D:\zeroshotapp\my-app\static\samples"
    for i in os.listdir(target_path):
        image=cv2.imread(target_path+"\\"+i)
        # print(path.split("\\")[-1])
        path=target_path+"\\"+i
        print(path)
        # print(path.split("\\")[-1].split(".")[0])
        img=[]
        # print(image.size)
        for j in range(1,len(os.listdir(prompt_path))+1):
            img.append(image)
        prompt_image_list,encoded_prompt_avg=promptencoder(prompt_path)
        encoded_image = processor(images=img , return_tensors="pt")
        encoded_prompt=processor(images=prompt_image_list, return_tensors="pt")
        encoded_image1 = processor(images=image , return_tensors="pt")
        # predict
        with torch.no_grad():
            outputs = model(**encoded_image, conditional_pixel_values=encoded_prompt.pixel_values)
            outputs1 = model(**encoded_image1, conditional_pixel_values=encoded_prompt_avg)
        preds = outputs.logits.unsqueeze(1)
        preds = torch.transpose(preds, 0, 1)
        preds1 = outputs1.logits.unsqueeze(1)
        preds1 = torch.transpose(preds1, 0, 1)
        lost=0
        # _, ax = plt.subplots(1, 2, figsize=(6, 4))
        # [a.axis('off') for a in ax.flatten()]
        # ax[0].imshow(image)
        for j in range(len(preds[0])):
            lost+=torch.sigmoid(preds[0][j])
        # lost=lost
        lost=torch.sigmoid(lost+preds1[0])
        # print(lost.size)
        # ax[0].imshow(lost)
        newimg=torch.stack((lost, lost,lost), 2)
        # newimg.shape
        torchvision.utils.save_image(lost,fp="D:\zeroshotapp\my-app\static\iirst.jpg")
        imi=cv2.imread("D:\zeroshotapp\my-app\static\iirst.jpg",0)
        image=cv2.imread(path)
        # image = cv2.resize(image, (imi.shape[0],imi.shape[1]),interpolation = cv2.INTER_AREA)
        _, binary_image = cv2.threshold(imi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        contours = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]
        cntrs=[]
        # print(path)
        count=0
        for cntr in contours:
            x,y,w,h = cv2.boundingRect(cntr)
            scale_x = image.shape[1] / imi.shape[1]
            scale_y = image.shape[0] / imi.shape[0]

            # Apply scaling factors to coordinates and dimensions
            x = int(x * scale_x)
            y = int(y * scale_y)
            w = int(w * scale_x)
            h = int(h * scale_y)
            # if(w>=3 and h>=3):
            imgCrop = image[y:y+h, x:x+w]
            cntrs.append([x,y,w,h])
            cv2.imwrite(paths+"\\"+path.split("\\")[-1].split(".")[0]+"_"+str(count)+".jpeg",imgCrop)
            count=count+1

    return {"output":"success"}
                # cv2_imshow(imgCrop)



# if __name__ == "__main__":
#     uvicorn.run(segmenter, host="0.0.0.0", port=8000)
#     # run(hello)
