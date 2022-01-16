import cv2
from argparse import ArgumentParser

def main(capture, file_path):
    print('main was called!')

    frame_width = int(capture.get(3))
    frame_height = int(capture.get(4))

    out = cv2.VideoWriter(file_path, cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
    # Read until video is completed
    while(capture.isOpened()):
        # Capture frame-by-frame
        ret, frame = capture.read()

        if ret:
            out.write(frame)
        else:
            break
        
            
    # When everything done, release the video capture object
    capture.release()

if __name__ =='__main__':
    parser = ArgumentParser()
    parser.add_argument('rtsp_link', type=str, help='link to the rtsp stream')
    parser.add_argument('--file_path', type=str, help='path to write file', default='main.avi')
    args = parser.parse_args()

	# Create a VideoCapture object
    capture = cv2.VideoCapture(args.rtsp_link)
    
    # Check if camera opened successfully
    if (capture.isOpened()):
        main(capture, args.file_path)
