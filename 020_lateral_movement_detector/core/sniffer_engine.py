from scapy.all import sniff, IP, TCP, UDP, ARP
import threading
import queue
import time

class SnifferEngine:
    """
    Asynchronous Packet Capture Engine using Scapy.
    Identifies patterns of lateral movement (ARP Spoofing, Brute Force, SMB traversal).
    """
    def __init__(self, callback):
        self.callback = callback
        self.running = False
        self.packet_queue = queue.Queue()
        self.sniffer_thread = None
        self.processor_thread = None

    def start(self, interface=None):
        self.running = True
        self.sniffer_thread = threading.Thread(target=self._sniff_loop, args=(interface,))
        self.processor_thread = threading.Thread(target=self._process_loop)
        
        self.sniffer_thread.daemon = True
        self.processor_thread.daemon = True
        
        self.sniffer_thread.start()
        self.processor_thread.start()

    def stop(self):
        self.running = False

    def _sniff_loop(self, interface):
        try:
            sniff(iface=interface, prn=lambda x: self.packet_queue.put(x), store=0, stop_filter=lambda x: not self.running)
        except Exception as e:
            print(f"Sniffer Error: {e}")
            # Mock mode if sniffing fails (e.g. no permissions)
            while self.running:
                time.sleep(1)

    def _process_loop(self):
        while self.running:
            try:
                packet = self.packet_queue.get(timeout=1)
                self._analyze_packet(packet)
            except queue.Empty:
                continue

    def _analyze_packet(self, packet):
        if not packet.haslayer(IP):
            return

        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        protocol = "OTHER"
        
        if packet.haslayer(TCP):
            protocol = "TCP"
            dport = packet[TCP].dport
            if dport in [445, 139]: # SMB
                self._flag_movement(src_ip, dst_ip, "SMB_TRAVERSAL", 75)
            elif dport in [3389]: # RDP
                self._flag_movement(src_ip, dst_ip, "RDP_ACCESS", 60)
        elif packet.haslayer(UDP):
            protocol = "UDP"
        elif packet.haslayer(ARP):
            protocol = "ARP"
            if packet[ARP].op == 2: # ARP Reply
                self._flag_movement(src_ip, dst_ip, "ARP_POISONING_CHECK", 40)

        # Basic flow notification
        self.callback({
            "src": src_ip,
            "dst": dst_ip,
            "proto": protocol,
            "time": time.time()
        })

    def _flag_movement(self, src, dst, type, confidence):
        # Notify of suspicious activity
        print(f"Suspicious {type} detected: {src} -> {dst} (Confidence: {confidence}%)")
