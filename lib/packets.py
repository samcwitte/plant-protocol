import time
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
    def __init__(self, packet_flag_type, data):
        self.protocol_version = "0.2.0"
        self.timestamp = time.time()
        self.packet_flag_type = packet_flag_type
        self.client_id = int(data['client_id'])
        self.data_length = len(data)
        self.data = data
            
    def toBytes(self):
        # Converts data into a bytestring format for transmission between client and server
        byteString = self.dest_ip.toHex() + \
                     '{:08x}'.format(self.packet_id) + \
                     '{:08x}'.format(self.data_length) + \
                     str(self.data) + "\n"
        return bytes(byteString, 'utf-8')