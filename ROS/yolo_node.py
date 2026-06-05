import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from ultralytics import YOLO

class YoloDetector(Node):
    def __init__(self):
        super().__init__('yolo_detector')
        self.subscription = self.create_subscription(
            Image,
            '/camera/color/image_raw',
            self.image_callback,
            1)
        self.publisher_ = self.create_publisher(Image, '/camera/color/yolo_image', 1)
        self.bridge = CvBridge()
        self.model = YOLO('/home/humus/Desktop/Studia/rocks_detection/Detection/runs/detect/depthai_model/yolo_rocks_btr_noise/weights/best.pt')
        self.frame_counter = 0

    def image_callback(self, msg):
        self.frame_counter += 1
        
        if self.frame_counter % 3 != 0:
            return

        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        results = self.model(cv_image)
        annotated_frame = results[0].plot()
        yolo_msg = self.bridge.cv2_to_imgmsg(annotated_frame, encoding="bgr8")
        yolo_msg.header = msg.header
        self.publisher_.publish(yolo_msg)

def main(args=None):
    rclpy.init(args=args)
    node = YoloDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
