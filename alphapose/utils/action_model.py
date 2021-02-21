import joblib
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def preprocess(person):
    kpts = person['keypoints']
    bbox = person['box']
    kpts = np.array(kpts).reshape(-1,3)[:,:2]
    cpts = (kpts[11] + kpts[12]) / 2
    kpts = kpts - cpts

    x, y, w, h = bbox
    kpts[:,0] = kpts[:,0]/w
    kpts[:,1] = kpts[:,1]/h
    
    return kpts.reshape(1,-1)



def predict_climb(climb_model,person):
    kpts = preprocess(person)
    result = climb_model.predict_proba(kpts)
    result = np.array(result)[:,:,1].reshape(-1)
    return result

def show_text(frame, out_text, org = (50, 50)):
    # font
    font = cv2.FONT_HERSHEY_SIMPLEX 
    
    # org
    org = org
    
    # fontScale
    fontScale = 1
    
    # Blue color in BGR
    color = (255, 0, 0)
    
    # Line thickness of 2 px
    thickness = 2
    
    # Using cv2.putText() method
    cv2.putText(frame, out_text, org, font,  
                    fontScale, color, thickness, cv2.LINE_AA)
    return frame

def show_cn_text(frame, out_text, org = (50, 50), textColor=(255, 0, 0), textSize=30):
    if (isinstance(frame, np.ndarray)):
        frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(frame)
    # 字体的格式
    fontStyle = ImageFont.truetype(
        "NotoSerifCJK-Regular.ttc", textSize, encoding="utf-8")
    # 绘制文本
    draw.text(org, out_text, textColor, font=fontStyle)
    # 转换回OpenCV格式
    return cv2.cvtColor(np.asarray(frame), cv2.COLOR_RGB2BGR)


def show_score(img,person,act_names,act_cn_names):
    x0,y0,w,h = np.array(person["box"],dtype=np.int32)

    score_strs = []
    for idx,act_name in enumerate(act_names):
        if person[act_name] > 0.4:
            score_str = "{}:{}".format(act_cn_names[idx],person[act_name])
            score_strs.append(score_str)
    
    for idx,score_str in enumerate(score_strs):
        img = show_cn_text(img,score_str,(x0,y0-40-40*idx))
    
    thickness=2
    cv2.rectangle(img,(x0,y0),(x0+w,y0+h),(255, 255, 0),thickness)

    return img

class action_model():
    def __init__(self,model_class):
        if model_class == "stand_sit_model":
            self.model_path = "models/stand_sit_model.joblib"
            self.act_names = ['stand','hands_up','raise_left','raise_right','touch_head','sit']
            self.act_cn_names = ['站立','举双手','举左手','举右手','抱头','静坐']
        elif model_class == "cross_model":
            self.model_path = "models/cross_model.joblib"
            self.act_names = ["normal", "cross","throw","aim","handgun","attack"]
            self.act_cn_names = ['正常','翻越','投掷','举枪','手枪','攻击']
        self.act_model = joblib.load(self.model_path)

    def make_act_score(self,result):
        for idx,person in enumerate(result):
            score = predict_climb(self.act_model,person)
            score_sum = 0.0
            # for act_id,act_name in enumerate(self.act_names):
            #     score_sum += score[act_id]
            for act_id,act_name in enumerate(self.act_names):
                person[act_name] = round(score[act_id],2)

    def vis_frame_score(self,orig_img,result):
        for idx,person in enumerate(result):
            orig_img = show_score(orig_img,person,self.act_names,self.act_cn_names)
        return orig_img

    def solve_image(self,result,orig_img):
        self.make_act_score(result)
        img = self.vis_frame_score(orig_img,result)
        return img