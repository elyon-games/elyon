import traceback
import json
import os
import sys
import pygame

import common.process as process
from common.config import getConfig, setConfigParameter
from common.random import generate_random_uuid
from common.args import getArgs
from common.utils import joinPath

pygame.init()
pygame.font.init()
pygame.mixer.init()

from client.lib.title import changeTitle
from client.lib.ping import ping
import common.path as path
import common.assets as assets
from client.style.constants import WHITE
from client.style.fonts import getFont
from client.lib.screen.controller import showScreen, updateScreen
from client.lib.storage.file import File
import hashlib

def stopAllProcesses():
    config = getConfig("client")
    pygame.quit()
    if config["launch"]["type"] == "local":
        for proces in process.get_all_processes().values():
            proces.stop()

def InitPygame():
    icon = pygame.image.load(assets.getAsset("/logo/round.ico"))
    pygame.display.set_icon(icon)
    changeTitle("Chargment...")
    window_width, window_height = 800, 600
    window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    return window, clock

def Main():
    try:
        config = getConfig("client")
        options = getArgs()
        global window, clock, ms_per_frame
        ms_per_frame = 10
        window, clock = InitPygame()

        client_data_path = path.get_path("client_data")
        client_data_servers_path = path.get_path("client_data_servers")

        commonStorage = File("common", client_data_path)
        computer_id: str = ""
        if "computer_id" not in commonStorage.getData():
            computer_id = generate_random_uuid()
            print(f"Computer ID : {computer_id}")
            commonStorage.addData("computer_id", computer_id)
            commonStorage.saveData()
        else:
            computer_id = commonStorage.getData()["computer_id"]
        setConfigParameter("client", "computer_id", computer_id)
        config = getConfig("client")

        changeTitle("Acceuil")

        pingData = ping()
        if pingData.get("version") != config["version"]:
            raise ValueError("La version du serveur ne correspond pas à celle du client.")
        
        serverKey = pingData.get("key")
        serverLocalID = hashlib.md5(f"{serverKey}{config['server']['host']}".encode('utf-8')).hexdigest()

        serverStorage = File(serverLocalID, client_data_servers_path)

        serverStorage.addData("token", "test")
        serverStorage.saveData()

        process.started_callback("client-main")

        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            window.fill((0, 0, 0))

            keys = pygame.key.get_pressed()

            # if keys[pygame.K_a]:
            #     showScreen(window, "auth")
            # elif keys[pygame.K_t]:
            #     showScreen(window, "test")

            updateScreen(window=window, events=events, keys=keys)

            fps = int(clock.get_fps())
            current_ms_per_frame = clock.get_time()
            if abs(current_ms_per_frame - ms_per_frame) >= 5:
                ms_per_frame = current_ms_per_frame

            computer_id_text = getFont("hud_info").render(f"CLIENT : {computer_id.split('-')[0]}", True, WHITE)
            window.blit(computer_id_text, (window.get_width() - computer_id_text.get_width() - 10, 10))

            fps_text = getFont("hud_info").render(f"FPS : {fps}", True, WHITE)
            ms_text = getFont("hud_info").render(f"MSPF : {ms_per_frame}", True, WHITE)
            window.blit(fps_text, (window.get_width() - fps_text.get_width() - 10, 25))
            window.blit(ms_text, (window.get_width() - ms_text.get_width() - 10, 40))

            pygame.display.flip()
            clock.tick(100)

        stopAllProcesses()

    except Exception as exc:
        import tkinter as tk
        from tkinter import messagebox

        def show_error_message(message, detail):
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Erreur", message, detail=detail)
            root.destroy()

        error_message = f"Une erreur s'est produite : {exc}"
        error_detail = traceback.format_exc()
        show_error_message(error_message, error_detail)
        stopAllProcesses()