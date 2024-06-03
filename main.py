from rosbags.rosbag1 import Reader
from rosbags.typesys import Stores, get_typestore
import cv2


# Create a typestore and get the string class.
typestore = get_typestore(Stores.ROS1_NOETIC)
file_name = "8_2023-07-29-15-25-00"
file_name = "2024-04-27-11-12-28"
bag_path = '/home/liwei/Workspace/dataset/bag/'
video_path = "/home/liwei/Workspace/dataset/video/"
camera_index = "_dev2"

skip_keyframes = False
# Create reader instance and open for reading.
with Reader(bag_path + file_name + ".bag") as reader:
    with open (video_path + file_name + camera_index + ".h264", 'wb') as f:
        # Iterate over messagROS1_NOETICes.
        for connection, timestamp, rawdata in reader.messages():
            if connection.topic == '/camera/h264_frame' + camera_index:
                msg = typestore.deserialize_ros1(rawdata, connection.msgtype)
                if skip_keyframes is False and msg.encoding == "yuv420p keyframe":
                    skip_keyframes = True
                if skip_keyframes:
                    print(msg.encoding)
                    print(f"key frame time is : {msg.header.stamp.sec + msg.header.stamp.nanosec / 1e9}")
                    f.write(msg.data)

cap = cv2.VideoCapture(video_path + file_name + camera_index + ".h264")
while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow('frame', frame)
    # cv2.write()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
