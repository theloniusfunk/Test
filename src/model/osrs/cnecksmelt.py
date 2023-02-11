import time
import random
import pyautogui as pag
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

import utilities.api.item_ids as ids
import utilities.imagesearch as imsearch
import utilities.ocr as ocr
import utilities.color as clr
import utilities.random_util as rd
from model.osrs.osrs_bot import OSRSBot
from model.runelite_bot import BotStatus
from utilities.api.morg_http_client import MorgHTTPSocket
from utilities.api.status_socket import StatusSocket
from utilities.geometry import RuneLiteObject


class OSRSNecksmelt(OSRSBot):
    def __init__(self):
        bot_title = "cNecksmelt"
        description = "This bot smelts necks. Position your character near the banks at Edgeville and press Play."
        super().__init__(bot_title=bot_title, description=description)
        self.running_time = 1
        self.take_breaks = False

    def create_options(self):
        self.options_builder.add_slider_option("running_time", "How long to run (minutes)?", 1, 500)
        self.options_builder.add_checkbox_option("take_breaks", "Take breaks?", [" "])

    def save_options(self, options: dict):
        for option in options:
            if option == "running_time":
                self.running_time = options[option]
            elif option == "take_breaks":
                self.take_breaks = options[option] != []
            else:
                self.log_msg(f"Unknown option: {option}")
                print("Developer: ensure that the option keys are correct, and that options are being unpacked correctly.")
                self.options_set = False
                return
        self.log_msg(f"Running time: {self.running_time} minutes.")
        self.log_msg(f"Bot will{' ' if self.take_breaks else ' not '}take breaks.")
        self.log_msg("Options set successfully.")
        self.options_set = True

    def main_loop(self):
        # Setup API
        api_m = MorgHTTPSocket()
        api_s = StatusSocket()

        keyboard = KeyboardController()
        mouse = MouseController()

        # Main loop
        start_time = time.time()
        end_time = self.running_time * 60

        gate = 0; 

        while time.time() - start_time < end_time:
            
            # Clicks on Furnace
            while api_s.get_inv_item_indices(ids.GOLD_BAR):
                if rd.random_chance(probability=0.79):
                    self.__move_mouse_to_furnace()
                    time.sleep(random.uniform(0.132, 0.344))
                    pag.keyDown("ctrl")
                    time.sleep(random.uniform(0.132, 0.344))
                    self.mouse.click()
                    time.sleep(random.uniform(0.135, 0.333))
                    pag.keyUp("ctrl")
                else:
                    self.__move_mouse_to_furnace()
                    self.mouse.click()
                    #running to furnace
                while not api_m.get_is_player_idle():
                    time.sleep(random.uniform(0.5, 0.75))
                    print("not idle - running")
                print("idle - at furnace")
                pag.press("space")
                gate = 0;
                while not api_m.get_is_player_idle():
                    time.sleep(random.uniform(0.5, 0.75))
                    print("not idle - smelting")
                print("idle")
                            
            if gate == 0:
                print("Go to Bank")
                self.take_break(max_seconds=2)
                cyan_tile = self.get_nearest_tag(clr.CYAN)
                self.mouse.move_to(cyan_tile.random_point())
                self.mouse.click()
                    #running to bank
                while not api_m.get_is_player_idle():
                    time.sleep(random.uniform(0.5, 0.75))
                    print("not idle - running")
                print("idle - at bank")

                #if api_s.get_inv_item_indices(ids.RUBY_NECKLACE):
                
            if imsearch.search_img_in_rect(imsearch.BOT_IMAGES.joinpath("bank", "DepositAll.png"), self.win.game_view, 0.05):
                print("deposit all")
                self.__DepositAll()
                time.sleep(random.uniform(0.11, 0.25))
                self.__move_mouse_to_item1()
                self.mouse.click()
                time.sleep(random.uniform(0.198, 0.31))
                self.__move_mouse_to_item2()
                self.mouse.click()
                time.sleep(random.uniform(0.13, 0.312))
                    
            """if DepositAll:= imsearch.search_img_in_rect(imsearch.BOT_IMAGES.joinpath("bank", "DepositAll.png"), self.win.game_view, 0.05):
                    if api_s.get_inv_item_indices(ids.RUBY_NECKLACE):
                        print("deposit all")
                        self.mouse.move_to(DepositAll.random_point())
                        self.mouse.click()
                        self.take_break(max_seconds=1)

                        #Fill inventory with gold bars
                        #self.get_item_from_bank("Gold bar")
                        self.__move_mouse_to_item1()
                        self.mouse.click()
                        time.sleep(random.uniform(0.198, 0.452))

                        #Fill inventory with sapphires
                        #self.get_item_from_bank("Sapphire")
                        self.__move_mouse_to_item2()
                        self.mouse.click()
                        time.sleep(random.uniform(0.13, 0.312))"""
                                
            # Escape key out of bank menu
            if gate == 0:
                pag.press("esc")
                print("escape")
                gate = 1;
            time.sleep(random.uniform(0.21, 0.31))

            self.update_progress((time.time() - start_time) / end_time)

        self.update_progress(1)
        self.__logout("Finished.")

    def __move_mouse_to_furnace(self):
        furnace = self.get_all_tagged_in_rect(self.win.game_view, clr.YELLOW)
        self.mouse.move_to(furnace[0].random_point())
        if not self.mouseover_text(contains=["Smelt"] + ["Furnace"], color=[clr.OFF_WHITE, clr.OFF_CYAN]):
            self.mouse.move_to(furnace[0].random_point())
        return True
    def __DepositAll(self):
        DepositAll = imsearch.search_img_in_rect(imsearch.BOT_IMAGES.joinpath("bank", "DepositAll.png"), self.win.game_view, 0.05)
        self.mouse.move_to(DepositAll.random_point())
        self.mouse.click()
        return True
    def __move_mouse_to_item1(self):
        iron_ore = self.get_all_tagged_in_rect(self.win.game_view, clr.GREEN)
        self.mouse.move_to(iron_ore[0].random_point())
        return True
    def __move_mouse_to_item2(self):
        iron_ore = self.get_all_tagged_in_rect(self.win.game_view, clr.RED)
        self.mouse.move_to(iron_ore[0].random_point())
        return True