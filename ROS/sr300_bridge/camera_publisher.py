import cv2
import zmq
import pyrealsense2 as rs
import numpy as np

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")

ctx = rs.context()
devices = ctx.query_devices()
print(f"Znaleziono urządzeń RealSense: {len(devices)}")
for dev in devices:
    print(f" - {dev.get_info(rs.camera_info.name)}")

if len(devices) == 0:
    print("BŁĄD: Biblioteka pyrealsense2 nie widzi żadnej kamery. Sprawdź kabel i lsusb.")
    exit()

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

try:
    print("Próbuję uruchomić strumienie...")
    pipeline.start(config)
    print("Strumienie uruchomione. Czekam na pierwszą klatkę...")
    
    while True:
        try:
            frames = pipeline.wait_for_frames(10000)
        except RuntimeError:
            print("Kamera wciąż się nagrzewa, czekam dalej...")
            continue
            
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()
        
        if not color_frame or not depth_frame:
            continue
            
        color_image = np.asanyarray(color_frame.get_data())
        _, color_buffer = cv2.imencode('.jpg', color_image)
        socket.send_multipart([b"color", color_buffer.tobytes()])
        
        depth_image = np.asanyarray(depth_frame.get_data())
        socket.send_multipart([b"depth", depth_image.tobytes()])
        
finally:
    pipeline.stop()
