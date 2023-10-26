class IP_Addr:
    def __init__(self, ip_address):
        self.ip = ip_address.split(".") # i.e. ['127', '0', '0', '12']
        self.ip[0] = int(self.ip[0])
        self.ip[1] = int(self.ip[1])
        self.ip[2] = int(self.ip[2])
        self.ip[3] = int(self.ip[3])
        
    def toHex(self):
        hex = '{:02x}'.format(self.ip[0]) + '{:02x}'.format(self.ip[1]) + '{:02x}'.format(self.ip[2]) + '{:02x}'.format(self.ip[3])
        return hex
    
    def stringify(ip_to_convert):
        ip_string = str(int(ip_to_convert[0:2], 16)) + "." + str(int(ip_to_convert[2:4], 16)) + "." + str(int(ip_to_convert[4:6], 16)) + "." + str(int(ip_to_convert[6:8], 16))
        return ip_string

class Packet:
    def __init__(self, client_id, dest_ip, packet_id, data):
        self.client_id = client_id
        self.dest_ip = IP_Addr(dest_ip)
        self.packet_id = packet_id
        self.data_length = len(data)
        self.data = data
            
    def toBytes(self):
        byteString = '{:08x}'.format(self.client_id) + self.dest_ip.toHex() + '{:08x}'.format(self.packet_id) + '{:08x}'.format(self.data_length) + str(self.data) + "\n"
        return bytes(byteString, 'utf-8')

    def summary(packet):
        client_id = packet[0:8]
        ip = packet[8:16] # IP Address is 4 bytes, which is 8 hex digits
        packet_id = packet[16:24]
        data_length = int(packet[24:32],16)
        data = packet[32:(32 + data_length)]
        
        print()
        print("Packet " + str(int(packet_id,16)) + " from client " + str(int(client_id, 16)) + " from IP (" + IP_Addr.stringify(ip) + ") contains data:\n" + data)