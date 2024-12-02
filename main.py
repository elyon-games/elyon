import sys
import os

def start()-> None:
    if "--server" in sys.argv :
        import server.main
        server.main.Main()
    else :
        import client.main
        client.main.Main()


if __name__=="__main__":
    start()