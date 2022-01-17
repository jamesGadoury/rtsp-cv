from argparse import ArgumentParser
from rtsp_stream_writer_service import RTSPStreamWriterService


if __name__ =='__main__':
    parser = ArgumentParser(prog='PROG')
    sub_parsers = parser.add_subparsers(title='command', dest='command', help='command help')

    # create parser for each command (this also exposes them as valid command args)
    start_parser = sub_parsers.add_parser('start', help='start command help')
    stop_parser = sub_parsers.add_parser('stop', help='stop command help')
    status_parser = sub_parsers.add_parser('status', help='status command help')

    # add arguments to start parser
    start_parser.add_argument('rtsp_link', type=str, help='link to the rtsp stream')
    start_parser.add_argument('--file_path', type=str, help='path to write file', default='main.avi')

    args = parser.parse_args()

    service = RTSPStreamWriterService('RTSPStreamWriterService', pid_dir='/tmp')

    # creating a sub parser for each valid command introduces implicit error handling
    # for invalid commands being passed at command line

    if args.command == 'start':
        print('Starting service.')
        service.set_parameters(rtsp_link=args.rtsp_link, file_path=args.file_path)
        service.start()
    
    if args.command == 'stop':
        print('Stopping service.')
        service.stop(block=True)

    if args.command == 'status':
        print('Service is running.') if service.is_running() else print('Service is not running.')