from redis import StrictRedis
from multiprocessing import Process, Value
from rtsp_stream_writer import RTSPStreamWriter
import json

def listen_to_stop_event(redis_protocol: StrictRedis, stop_flag: Value):
    print('listen_to_stop_event called')
    sub = redis_protocol.pubsub()
    sub.subscribe('stop_rtsp_stream_writer')

    for message in sub.listen():
        if message['type'] == 'message':
            stop_flag.value = 1
            print('stop event triggered')
            break

    
def start_rtsp_stream_writer(redis_protocol: StrictRedis, message: dict):
    print(f'start_rtsp_stream_writer called with message={message}')
    assert 'rtsp_link' in message
    assert 'file_path' in message

    print(f'in start_rtsp_stream_writer, message={message}')
    writer = RTSPStreamWriter(rtsp_link=message.get('rtsp_link'), file_path=message.get('file_path'))

    if not writer.capture.isOpened():
        print(f'error! failure to start stream writing!')
        return

    # next we create a new process for listening to the stop event
    stop_flag = Value('i', 0)
    listen_process = Process(target=listen_to_stop_event, args=(redis_protocol, stop_flag))
    listen_process.start()

    while stop_flag.value == 0:
        if not writer.capture.isOpened():
            print('writer capture failed to stay open')
            listen_process.terminate()
            break
        writer.read_frame_and_write()
    listen_process.join()
    print('finished in start_rtsp_stream_writer')


def main():
    print('main was called!')

    red = StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True)

    sub = red.pubsub()
    sub.subscribe('start_rtsp_stream_writer')
    processes = []
    for message in sub.listen():
        print(f'in main: message={message}')
        if message['type'] == 'message':
            p = Process(target=start_rtsp_stream_writer, args=(red, json.loads(message['data'])))
            p.start()
            processes.append(p)

    for process in processes:
        process.join()


if __name__ =='__main__':
    main()