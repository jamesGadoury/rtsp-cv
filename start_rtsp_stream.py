from redis import StrictRedis
import json
from os import getenv
from argparse import ArgumentParser


def main(rtsp_link: str, file_path: str):
    red = StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True)
    payload = json.dumps({'rtsp_link': rtsp_link, 'file_path': file_path})
    red.publish('start_rtsp_stream_writer', payload)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('rtsp_link', type=str, help='link to the rtsp stream')
    parser.add_argument('--file_path', type=str, default='default.avi', help='path to write the resulting video')

    args = parser.parse_args()
    main(args.rtsp_link, args.file_path)