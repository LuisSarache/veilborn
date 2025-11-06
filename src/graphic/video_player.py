import tkinter as tk
from PIL import Image, ImageTk
import cv2
import os

class VideoPlayer:
    def __init__(self, canvas, root, video_path, on_complete):
        self.canvas = canvas
        self.root = root
        self.video_path = video_path
        self.on_complete = on_complete
        self.cap = None
        self.is_playing = False
        
    def play(self):
        if not os.path.exists(self.video_path):
            self.on_complete()
            return
            
        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap.isOpened():
            self.on_complete()
            return
            
        self.is_playing = True
        self.canvas.delete("all")
        self._show_frame()
        
    def _show_frame(self):
        if not self.is_playing:
            return
            
        ret, frame = self.cap.read()
        if not ret:
            self.stop()
            return
            
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (1280, 720))
        img = Image.fromarray(frame)
        self.photo = ImageTk.PhotoImage(img)
        self.canvas.create_image(640, 360, image=self.photo)
        
        self.root.after(33, self._show_frame)
        
    def stop(self):
        self.is_playing = False
        if self.cap:
            self.cap.release()
        self.on_complete()
