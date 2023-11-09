import time
import struct
class IP_Addr:
    def __init__(self, ip_address):
        self.ip = ip_address.split(".") # i.e. ['127', '0', '0', '12']
        for i in range(4):
            self.ip[i] = int(self.ip[i])
        
    def toHex(self):
        hex = '{:02x}'.format(self.ip[0]) + '{:02x}'.format(self.ip[1]) + '{:02x}'.format(self.ip[2]) + '{:02x}'.format(self.ip[3])
        return hex
    
    def stringify(ip):
        ip_string = str(int(ip[0:2], 16)) + "." + \
                    str(int(ip[2:4], 16)) + "." + \
                    str(int(ip[4:6], 16)) + "." + \
                    str(int(ip[6:8], 16))
        return ip_string

class Packet:
    def __init__(self, packet_flag_type, username, data):
        self.protocol_version = "0.2.0" # 5
        self.timestamp = time.time()    # 18
        self.packet_flag_type = packet_flag_type
        self.username = username
        self.data_length = len(data)
        self.data = data

    def toBytes(self):
        # Converts data into a bytestring format for transmission between client and server  line 30 #self.dest_ip.toHex() + \
        byteString =  str(self.protocol_version).encode('utf-8') + \
                      str(self.timestamp).encode('utf-8') + \
                      str(self.packet_flag_type).encode('utf-8') + \
                      str(self.username).encode('utf-8') + \
                      str(self.data_length).encode('utf-8') + \
                      str(self.data).encode('utf-8')
        
        return byteString
    
    def fromBytes(byteString):
        # Extract components based on the specified format
        hexString = byteString.decode('utf-8')

    # Extract components based on the specified format
        protocol_version = hexString[0:5]
        print(f'Protocol Version: {protocol_version}')
        timestamp = float(hexString[5:21])
        print(f'Timestamp: {timestamp}')
        packet_flag_type = hexString[21:25]
        print(f'Packet Flag Type: {packet_flag_type}')
        username = bytes.fromhex(hexString[25:27]).decode('utf-8', 'replace')
        print(f'Username: {username}')
        data_length = int(hexString[27:29], 16)
        print(f'Data Length: {data_length}')
        data = bytes.fromhex(hexString[29:-1]).decode('utf-8', 'replace')
        print(f'Data: {data}')

        
        
        
        
        
        

        return protocol_version, timestamp, packet_flag_type, username, data_length, data

