import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import zmq
import numpy as np

class CameraBridge(Node):
    def __init__(self):
        super().__init__('camera_bridge')
        
        # Tworzymy dwa osobne tematy do publikowania w ROS
        self.color_pub = self.create_publisher(Image, '/camera/color/image_raw', 10)
        self.depth_pub = self.create_publisher(Image, '/camera/depth/image_raw', 10)
        self.bridge = CvBridge()
        
        self.zmq_context = zmq.Context()
        self.socket = self.zmq_context.socket(zmq.SUB)
        self.socket.connect("tcp://localhost:5555")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "")
        
        self.timer = self.create_timer(0.01, self.timer_callback)

    def timer_callback(self):
        try:
            # Petla odbierajaca wszystkie oczekujace wiadomosci z gniazda ZMQ
            while True:
                topic, frame_data = self.socket.recv_multipart(flags=zmq.NOBLOCK)
                
                if topic == b"color":
                    nparr = np.frombuffer(frame_data, np.uint8)
                    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    if img is not None:
                        msg = self.bridge.cv2_to_imgmsg(img, encoding="bgr8")
                        msg.header.frame_id = "camera_link"
                        self.color_pub.publish(msg)
                        
                elif topic == b"depth":
                    # Rozkodowanie 16-bitowej tablicy o wymiarach 480x640
                    depth_img = np.frombuffer(frame_data, dtype=np.uint16).reshape((480, 640))
                    msg = self.bridge.cv2_to_imgmsg(depth_img, encoding="16UC1")
                    msg.header.frame_id = "camera_link"
                    self.depth_pub.publish(msg)
                    
        except zmq.Again:
            pass

def main(args=None):
    rclpy.init(args=args)
    node = CameraBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
