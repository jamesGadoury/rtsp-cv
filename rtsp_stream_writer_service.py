import logging
from logging.handlers import SysLogHandler
import time
import cv2

from service import find_syslog, Service

class RTSPStreamWriterService(Service):
    def __init__(self, *args, **kwargs):
        super(RTSPStreamWriterService, self).__init__(*args, **kwargs)
        self.logger.addHandler(SysLogHandler(address=find_syslog(),
                               facility=SysLogHandler.LOG_DAEMON))
        self.logger.setLevel(logging.INFO)
        self.rtsp_link = None
        self.file_path = None


    def set_parameters(self, rtsp_link, file_path):
        self.logger.info(f'RTSPStreamWriterService.set_parameters called with rtsp_link={rtsp_link}, file_path={file_path}')
        self.rtsp_link = rtsp_link
        self.file_path = file_path


    def process_rtsp_stream(self):
        self.logger.info(f'RTSPStreamWriterService.process_rtsp_stream called with self={self}')
        print('here we are')
        # Create a VideoCapture object
        capture = cv2.VideoCapture(self.rtsp_link)

        if (not capture.isOpened()):
            self.logger.error(f'RTSPStreamWriterService.process_rtsp_stream error: unable to open capture for rtsp_link={self.rtsp_link}')
            return

        frame_width = int(capture.get(3))
        frame_height = int(capture.get(4))

        out = cv2.VideoWriter(self.file_path, cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
        # Read until video is completed
        while(capture.isOpened() and not self.got_sigterm()):
            # Capture frame-by-frame
            ret, frame = capture.read()

            if ret:
                out.write(frame)
            else:
                break
        
        # When everything done, release the video capture object
        capture.release()


    def run(self):
        self.logger.info("RTSPStreamWriterService.run called")
        self.process_rtsp_stream()
