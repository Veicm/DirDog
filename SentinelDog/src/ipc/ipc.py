from multiprocessing.connection import Client
import time


def connect_to_host(ip="localhost",port=6000):
    while True:
        time.sleep(3)
        try:
            print(f"[+] Trying to connect!")
            address = (ip, port)
            conn = Client(address, authkey=b"secret password")

            print("[+] Connection succesfull!")
            return conn
        except:
            print("[!] Error: Connecetion failed!")

def send_data(conn,data):
    conn.send(data)