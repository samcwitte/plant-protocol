import time

class Packet:
    def __init__(self, packet_flag_type, username, data):
        self.protocol_version = "2.0.0" # 5
        self.timestamp = time.time_ns() // 1_000_000_000    # 18
        self.packet_flag_type = packet_flag_type
        self.username = username
        self.data = data

    def toBytes(self):
        # Converts data into a bytestring format for transmission between client and server  line 30 #self.dest_ip.toHex() + \
        byteString =  bytes((self.protocol_version).encode('utf-8')) + \
                      bytes(str(self.timestamp), 'utf-8') + \
                      bytes((self.packet_flag_type).encode('utf-8')) + \
                      bytes((self.username.ljust(16, '\x00').encode('utf-8'))) + \
                      bytes((self.data).encode('utf-8'))
        
        # print(str(byteString))
        return byteString
    
    def fromBytes(byteString):
        # Extract components based on the specified format
        hexString = byteString.decode('utf-8')
        # print(hexString)
        # 0.2.01699498899ICONtimmy
    # Extract components based on the specified format
        protocol_version = hexString[0:5]
        timestamp = float(hexString[5:15])
        packet_flag_type = hexString[15:19]
        username = hexString[19:35]
        data = hexString[35:]

        # print(f'Protocol Version: {protocol_version}')
        # print(f'Timestamp: {timestamp}')
        # print(f'ctime: {time.ctime(timestamp)}')
        # print(f'Packet Flag Type: {packet_flag_type}')
        # print(f'Username: {username}')
        # print(f'Data: {data}')
        return protocol_version, timestamp, packet_flag_type, username, data
