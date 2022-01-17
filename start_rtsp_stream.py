from redis import StrictRedis
import json
from os import getenv


red = StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True)
payload = json.dumps({'rtsp_link': getenv('RTSP_LINK'), 'file_path': 'blah.avi'})
red.publish('start_rtsp_stream_writer', payload)
