
import cv2
import numpy as np
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

lower_red1 = np.array([0, 120, 70])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 120, 70])
upper_red2 = np.array([180, 255, 255])

class CloakTransformer(VideoTransformerBase):
    def __init__(self):
        self.bg = None

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img = cv2.flip(img, 1)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = mask1 + mask2
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))

        if self.bg is None:
            self.bg = img
            return img

        img[np.where(mask==255)] = self.bg[np.where(mask==255)]
        return img

st.title("Invisible Cloak App")
st.write("कैमरे के सामने से हट जाएँ जब background capture हो रहा हो।")

webrtc_streamer(key="cloak", video_transformer_factory=CloakTransformer)
