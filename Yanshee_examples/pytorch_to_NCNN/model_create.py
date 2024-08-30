import argparse
import numpy as np
import torch
from torchvision import transforms
import cv2
import os
from mobilenetv1 import MobileNetV1
#from faceDet.FaceDetect import FaceDet
from torch.autograd import Variable

def FindKeyFace(dets):  #Find the most important one in multiple faces
    if len(dets) ==1:
        return 0
    biggest_w =0
    id =-1
    for i in range(len(dets)):
        w =dets[i][2] -dets[i][0]
        if w>biggest_w:
            biggest_w=w
            id =i
    return id

def face_crop(img, box):  #Square cutting of face, with the length and width to be kept at 1:1 due to training. In case of crossing the boundary, use black for filling
	h = img.shape[0]
	w = img.shape[1]
	x1, y1, = box[:2]
	w1 =box[2] -x1
	h1 =box[3] -y1
	maxwh = w1 if w1 > h1 else h1
	xmin = int(np.clip(x1 + w1 / 2 - maxwh / 2, 0, w - 1))
	ymin = int(np.clip(y1 + h1 / 2 - maxwh / 2, 0, h - 1))
	xmax = int(np.clip(xmin + maxwh, 0, w - 1))
	ymax = int(np.clip(ymin + maxwh, 0, h - 1))
	# pdb.set_trace()
	img2 = img[ymin: ymax, xmin: xmax, :]
	roi_w = xmax - xmin
	roi_h = ymax - ymin
	roi = max(roi_w, roi_h)
	ex_w = int((roi - roi_w) // 2)
	ex_h = int((roi - roi_h) // 2)
	img2 = cv2.copyMakeBorder(img2, ex_h, ex_h, ex_w, ex_w, cv2.BORDER_CONSTANT, value=(0, 0, 0))
	#img2 =cv2.resize(img2,(64,64))
	return img2

def t_img():
    #img_path = './collectData/0/0-1400.jpg'
    #img_path = './collectData/1/1-81.jpg'
    #img_path = './collectData/2/2-355.jpg'

    # Model loading
    model_path = '/home/oneai/work/mask_train_det_v1.0/models/checkpoint_epoch_20.pth'
    checkpoint = torch.load(model_path)
    mask_backbone =MobileNetV1()
    mask_backbone.load_state_dict(checkpoint)
    mask_backbone.eval()
    #mask_backbone = mask_backbone.cuda() #lhb modified

    batch_size = 1  #Batch size
    input_shape = (3, 224, 224)   #Input data, changed to your own input shape
    x = torch.randn(batch_size, *input_shape)	# Generate tensor
    dummy_input = Variable(torch.randn(1, 3, 224, 224)) # nchw
    export_onnx_file = "test.onnx"			# Destination ONNX file name
    input_names = [ "inputs"]
    output_names = [ "outpute" ]
    torch.onnx.export(mask_backbone,  dummy_input, export_onnx_file, verbose=True, input_names=input_names, output_names=output_names)

    # Face detection model initialization
    #mydet = FaceDet()
    #mydet.init()

    #scale = 255.
    #mean = 0.5

    #img = cv2.imread(img_path)
    #img_raw = img.copy()
    #dets = mydet.predict(img_raw)  #Face detection
    #if len(dets) < 1:
    #    print('no face in the srceen!')

    #key_id = FindKeyFace(dets)    #Find the most important one in all faces

    # Face clipping and data preprocessing
    #img_crop = face_crop(img_raw, dets[key_id])
    #img_crop = cv2.resize(img_crop, (224, 224))
    #img_crop = cv2.resize(img_raw, (224, 224))
    #img_crop = cv2.cvtColor(img_crop, cv2.COLOR_BGR2RGB)
    #img_crop = img_crop / scale
    #img_crop -= mean
    #img_crop = torch.from_numpy(img_crop).permute(2, 0, 1).contiguous().float()
    #img_crop = img_crop.unsqueeze(0)
    #img_crop = img_crop.unsqueeze(0).cuda()  # lhb

    #Mask status recognition
    #fmask = mask_backbone(img_crop)
    #print(fmask)
    #fmask = np.argmax(fmask.cpu().detach().numpy()[0])

    #m3 =''
    #if fmask == 0:
    #    m3 = 'masked'
    #elif fmask == 1:
    #    m3 = 'unmasked'
    #elif fmask == 2:
    #    m3 = 'not masked well'

    #cv2.rectangle(img, (dets[key_id][0], dets[key_id][1]), (dets[key_id][2], dets[key_id][3]), (0, 0, 255), 2)
    #cv2.putText(img, m3, (dets[key_id][0], dets[key_id][1]-20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)
    #cv2.imshow('show', img)
    #cv2.waitKey(0)
    #print('end')

def t_video():
    # Model loading
    model_path = '/home/oneai/work/mask_train_det_v1.0/models/checkpoint_epoch_20.pth'
    checkpoint = torch.load(model_path)
    mask_backbone = MobileNetV1()
    mask_backbone.load_state_dict(checkpoint)
    mask_backbone.eval()
    mask_backbone = mask_backbone.cuda()

    # Face detection model initialization
    mydet = FaceDet()
    mydet.init()

    scale = 255.
    mean = 0.5

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, img = cap.read()  #Video read-in
        if not ret:
            continue

        img_raw = img.copy()
        dets = mydet.predict(img_raw)
        if len(dets) < 1:      #No processing without face
            #print('no face in the srceen!')
            cv2.imshow('show', img)
            cv2.waitKey(1)
            continue

        key_id = FindKeyFace(dets) #Find the most important one in all faces

        # Face clipping and data preprocessing
        img_crop = face_crop(img_raw, dets[key_id])
        img_crop = cv2.resize(img_crop, (224, 224))
        img_crop = cv2.cvtColor(img_crop, cv2.COLOR_BGR2RGB)
        img_crop = img_crop / scale
        img_crop -= mean
        img_crop = torch.from_numpy(img_crop).permute(2, 0, 1).contiguous().float()
        img_crop = img_crop.unsqueeze(0).cuda()

        # Mask status recognition
        fmask = mask_backbone(img_crop)
        print(fmask)
        fmask = np.argmax(fmask.cpu().detach().numpy()[0])
        print("softmax -> ", fmask)

        m3 = ''
        if fmask == 0:
            m3 = 'masked'
        elif fmask == 1:
            m3 = 'unmasked'
        elif fmask == 2:
            m3 = 'not masked well'

        cv2.rectangle(img, (dets[key_id][0], dets[key_id][1]), (dets[key_id][2], dets[key_id][3]), (0, 0, 255), 2)
        cv2.putText(img, m3, (dets[key_id][0], dets[key_id][1] - 20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)
        cv2.imshow('show', img)
        cv2.waitKey(1)

    cap.release()
    print('end')

if __name__ == "__main__":
    t_img()         #Test image

    #t_video()      #Test video
