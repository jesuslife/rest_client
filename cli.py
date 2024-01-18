import cv2
import requests
import sys
import urllib3
from urllib3.exceptions import (ConnectTimeoutError, MaxRetryError,
                                NewConnectionError, SSLError,
                                ReadTimeoutError, )


def main():
    # file_path = 'test5.jpg'
    # files = {'image': (file_path, open(file_path, 'rb'), "image/jpeg")}

    timeout = urllib3.Timeout(connect=2.0,
                          read=7.0
                          #total=TIMEOUT_TOTAL)
    )
    status_forcelist = frozenset({})
    allowed_methods = frozenset({'HEAD', })

    retries = urllib3.Retry(total=10,
                        connect=5,
                        read=2,
                        redirect=5,
                        # status=REQUEST_RETRIES,
                        # other=REQUEST_RETRIES,
                        allowed_methods=allowed_methods,
                        status_forcelist=status_forcelist,
                        backoff_factor=0.1,
                        respect_retry_after_header=False,
                        )
    retries.RETRY_AFTER_STATUS_CODES = frozenset({})


    # Read video file
    cap = cv2.VideoCapture(VIDEO_PATH)

    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error opening video stream or file")

    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret:

            # Display the resulting frame
            # cv2.imshow('Frame', frame)
            # frame = cv2.resize(frame, dsize=(960, 540))

            # Encode the frame as JPEG format
            success, frame_encoded = cv2.imencode('.jpg', frame)

            if success:
                # Put the encoded frame in a POST request
                try:
                    try:
                        response = requests.post(url=URL,
                                                 files={'image': ('image.jpg', frame_encoded, 'image/jpeg'), 'Content-Type': 'image/jpeg'},
                                                 timeout=timeout,
                                                )
                    except MaxRetryError as error:
                        raise error.reason
                except NewConnectionError as error:
                    print('NewConnectionError', error.__str__())
                except ConnectTimeoutError as error:
                    print('ConnectTimeoutError', error.__str__())
                except SSLError as error:
                    print('SSLError', error.__str__())
                except ReadTimeoutError as error:
                    print('ReadTimeoutError', error.__str__())

            # Display the resulting frame
            cv2.imshow('Frame', frame)

            # Press Q on keyboard to  exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Break the loop
        else:
            break

    # Release the video capture object
    cap.release()

    # Close all the frames
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # Main parameters
    # URL = 'http://127.0.0.1:8000/api/zpdrilling/'
    # URL = 'http://192.168.100.52:8000/api/zpdrilling/'
    URL = 'http://192.168.100.28:8080/api/zpdrilling/'
    VIDEO_PATH = 'clip.mp4'

    # Main function call
    main()
