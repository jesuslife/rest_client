import cv2
import requests
import sys



def main():
    # file_path = 'test5.jpg'
    # files = {'image': (file_path, open(file_path, 'rb'), "image/jpeg")}

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
                    # multipart/form-data
                    response = requests.post(URL, 
                                             files={'image': ('image.jpg', frame_encoded, 'image/jpeg'), 'Content-Type': 'image/jpeg'})

                    # response = requests.post(URL, files={'image': ('', frame_encoded), 'type': 'image/jpeg'})
                except Exception as e:
                    sys.exit('%s' % e)

                # Check the response
                if response.ok and response.json()['response'] != -1:
                    print(response.status_code, response.json())
                    data = response.json()
                    cytoplasm_centroid = data['response']['cytoplasm_centroid']
                    zp_inner_point = data['response']['zp_inner_point']
                    zp_outer_point = data['response']['zp_outer_point']
                    cy_left_end_point = data['response']['cytoplasm_left_end_point']

                    poi_list = [cytoplasm_centroid, zp_inner_point, zp_outer_point, cy_left_end_point]

                    for poi in poi_list:
                        frame = cv2.circle(frame,
                                           (poi[0], poi[1]),
                                           radius=2,
                                           color=(0, 255, 0),
                                           thickness=-1)

                elif response.ok and response.json()['response'] == -1:
                    print(response.status_code, response.json())
                else:
                    print('Response code: %s ' % response.status_code)
            else:
                print('Error in frame encoding')

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
            