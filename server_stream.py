import io
import socket
import struct
from PIL import Image
import cv2
import numpy as np

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

# Define the codec and create VideoWriter object
# fourcc = cv2.VideoWriter_fourcc(*'MJPG')
# out = cv2.VideoWriter('output.mpg',fourcc, 20.0, (640,480))

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
try:
    cv2.namedWindow('img')
    while True:
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)
        # Construct a numpy array from the stream
        data = np.fromstring(image_stream.getvalue(), dtype=np.uint8)
        # "Decode" the image from the array, preserving colour
        image = cv2.imdecode(data, 1)
        cv2.imshow('img', image)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
finally:
    cv2.destroyAllWindows()
    connection.close()
    server_socket.close()
