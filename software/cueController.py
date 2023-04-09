import websocket
import threading
from threading import Thread
import serial

device = 'COM4'
global result
result = 0

try:
    global ser
    ser = serial.Serial(device, 9600)
except serial.SerialException:
    print("Couldn't connect to Arduino on %s" % device)
    exit(1)


class SerialWorker(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            serialBytes = str(ser.readline(3))
            first_byte = serialBytes[2]
            second_byte = serialBytes[3]

            print(serialBytes)

            if first_byte == "^":
                if second_byte == "E":
                    my_bytes = bytearray()
                    char = int(hex(ord(str(second_byte))), 16)
                    my_bytes.append(char)
                    result = my_bytes
                    ws.send(result)
                    my_bytes = bytearray()
                else:
                    char1 = int("0x5E", 16)

                    third_byte = serialBytes[4]
                    char2 = int(hex(ord(str(second_byte))), 16)
                    char3 = int(hex(ord(str(third_byte))), 16)

                    my_bytes = bytearray()

                    my_bytes.append(char1)
                    my_bytes.append(char2)
                    my_bytes.append(char3)

                    result = my_bytes
                    ws.send(result)
                    my_bytes = bytearray()

# Function to handle incoming messages


def on_message(ws, message):
    print(f'Received message: {message}')
    if message[0] == "^":
        ser.write(b'^')
        ser.write(str(message[1]).encode())
        ser.write(str(message[2]).encode())

# Function to handle WebSocket close event


def on_close(ws):
    print('WebSocket connection closed.')

# Function to send messages to the server^


def send_messages(ws):
    while True:
        message = input('> ')
        ws.send(message)
        if message == 'exit':
            break


# Create WebSocket connection
ws = websocket.WebSocketApp('ws://192.168.1.173:3000/',
                            on_message=on_message,
                            on_close=on_close)

# Start a separate thread for sending messages
send_thread = threading.Thread(target=send_messages, args=(ws,))
send_thread.start()

worker = SerialWorker()
worker.daemon = True
worker.start()

# Start the WebSocket connection and listen for incoming messages
ws.run_forever()
