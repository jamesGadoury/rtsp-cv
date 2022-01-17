from redis import StrictRedis


red = StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True)
red.publish('stop_rtsp_stream_writer', 'blah')
