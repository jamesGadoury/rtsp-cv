import logging
from logging.handlers import SysLogHandler

from service import find_syslog, Service

from rtsp_stream_writer import RTSPStreamWriter

class RTSPStreamWriterService(Service):
    def __init__(self, *args, **kwargs):
        super(RTSPStreamWriterService, self).__init__(*args, **kwargs)
        self.logger.addHandler(SysLogHandler(address=find_syslog(),
                               facility=SysLogHandler.LOG_DAEMON))
        self.logger.setLevel(logging.DEBUG)
        self.writer = None


    def init_writer(self, rtsp_link, file_path):
        self.logger.info(f'RTSPStreamWriterService.init_writer called with rtsp_link={rtsp_link}, file_path={file_path}')
        self.writer = RTSPStreamWriter(rtsp_link=rtsp_link, file_path=file_path)
        if not self.writer.capture.isOpened():
            raise ValueError(f'init_writer called with {rtsp_link} that could not create capture')


    def process_rtsp_stream(self):
        self.logger.info(f'RTSPStreamWriterService.process_rtsp_stream called with self.writer={self.writer}')
        print('here we are')

        # Read until video is completed
        while not self.got_sigterm():
            self.writer.read_frame_and_write()
            self.logger.debug(f'read_frame_and_write called')

        self.logger.debug(f'got_sigterm')



    def run(self):
        self.logger.info("RTSPStreamWriterService.run called")
        self.process_rtsp_stream()
