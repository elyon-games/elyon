from server.services.cmd.base import classCMD
from typing import Dict
import common.process as process
import os
import signal

comandes: Dict[str, classCMD] = {}

def initCMD():
    print("Start CLI")
    while process.get_process_running_status("server-cli"):
        command = input("\n")
        if command == "stop":
            print("Stopping server...")
            process.stop_all_processes()
            os.kill(os.getpid(), signal.SIGINT)
        else:
            print(f"Command Inconnu: {command}")
    print("Stop CLI")