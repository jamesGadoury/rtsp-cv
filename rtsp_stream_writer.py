import cv2
from time import time
from os import getenv

class RTSPStreamWriter:
    def __init__(self, rtsp_link, file_path):
        print(f'RTSPStreamWriter.__init__ called with rtsp_link={rtsp_link}, file_path={file_path}')
        self.rtsp_link = rtsp_link
        self.file_path = file_path

        # Create a VideoCapture object
        self.capture = cv2.VideoCapture(self.rtsp_link)

        if not self.capture.isOpened():
            return

        self.frame_width = int(self.capture.get(3))
        self.frame_height = int(self.capture.get(4))
        self.out = cv2.VideoWriter(file_path, cv2.VideoWriter_fourcc('M','J','P','G'), 29, (self.frame_width,self.frame_height))


    def __repr__(self):
        return f'(RTSPStreamWriter: rtsp_link:{self.rtsp_link}, file_path{self.file_path}, res: {self.frame_height},{self.frame_width})'


    def read_frame_and_write(self):
        if not self.capture.isOpened():
            return

        # Capture frame-by-frame
        ret, frame = self.capture.read()

        if ret:
            self.out.write(frame)

    
def test_can_write_stream():
    writer = RTSPStreamWriter(rtsp_link=getenv('RTSP_LINK'), file_path='test_stream.avi')    
    start = time()

    assert writer.capture.isOpened()

    # waiting for roughly 5 seconds to pass, doesn't have to be super accurate
    while time() - start < 5:
        writer.read_frame_and_write()

