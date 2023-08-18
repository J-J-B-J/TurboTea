from OLED import *
from machine import Pin
from _thread import start_new_thread
from time import sleep


class TurboTea:
    """A class for a TurboTea"""
    TEABAG_IMAGE = [
        # A list of (x, y) coordinates that represent a teabag image
        (10, 0), (11, 0), (12, 0), (13, 0), (14, 0), (15, 0), (16, 0), (17, 0),
        (9, 1), (10, 1), (17, 1), (18, 1),
        (8, 2), (9, 2), (18, 2), (19, 2),
        (7, 3), (8, 3), (19, 3),
        (7, 4), (19, 4), (20, 4),
        (7, 5), (20, 5),
        (7, 6), (20, 6),
        (7, 7), (15, 7), (16, 7), (17, 7), (18, 7), (19, 7), (20, 7), (21, 7),
        (22, 7), (23, 7), (24, 7),
        (7, 8), (14, 8), (15, 8), (20, 8), (24, 8), (25, 8),
        (7, 9), (8, 9), (14, 9), (16, 9), (19, 9), (20, 9), (23, 9), (25, 9),
        (8, 10), (13, 10), (16, 10), (17, 10), (22, 10), (23, 10), (26, 10),
        (8, 11), (9, 11), (13, 11), (14, 11), (15, 11), (18, 11), (19, 11),
        (20, 11), (21, 11), (24, 11), (25, 11), (26, 11),
        (9, 12), (13, 12), (26, 12),
        (8, 13), (9, 13), (13, 13), (26, 13),
        (4, 14), (5, 14), (6, 14), (7, 14), (8, 14), (13, 14), (26, 14),
        (3, 15), (4, 15), (13, 15), (26, 15),
        (3, 16), (13, 16), (26, 16),
        (1, 17), (2, 17), (3, 17), (4, 17), (5, 17), (13, 17), (26, 17),
        (0, 18), (3, 18), (6, 18), (13, 18), (26, 18),
        (0, 19), (6, 19), (13, 19), (14, 19), (16, 19), (17, 19), (19, 19),
        (20, 19), (22, 19), (23, 19),
        (25, 19), (26, 19),
        (0, 20), (6, 20), (13, 20), (14, 20), (15, 20), (16, 20), (17, 20),
        (18, 20), (19, 20), (20, 20), (21, 20),
        (22, 20), (23, 20), (24, 20), (25, 20),
        (26, 20),
        (0, 21), (6, 21), (13, 21), (14, 21), (15, 21), (16, 21), (17, 21),
        (18, 21), (19, 21), (20, 21), (21, 21),
        (22, 21), (23, 21), (24, 21), (25, 21),
        (26, 21),
        (0, 22), (6, 22), (13, 22), (14, 22), (15, 22), (16, 22), (17, 22),
        (18, 22), (19, 22), (20, 22), (21, 22),
        (22, 22), (23, 22), (24, 22), (25, 22),
        (26, 22),
        (0, 23), (6, 23), (13, 23), (14, 23), (15, 23), (16, 23), (17, 23),
        (18, 23), (19, 23), (20, 23), (21, 23),
        (22, 23), (23, 23), (24, 23), (25, 23),
        (26, 23),
        (0, 24), (1, 24), (2, 24), (3, 24), (4, 24), (5, 24), (6, 24),
        (13, 24),
        (14, 24), (15, 24), (16, 24), (17, 24),
        (18, 24), (19, 24), (20, 24), (21, 24),
        (22, 24), (23, 24), (24, 24), (25, 24),
        (26, 24),
        (13, 25), (14, 25), (15, 25), (16, 25), (17, 25), (18, 25), (19, 25),
        (20, 25), (21, 25), (22, 25),
        (23, 25), (24, 25), (25, 25),
        (26, 25),
        (13, 26), (14, 26), (15, 26), (16, 26), (17, 26), (18, 26), (19, 26),
        (20, 26), (21, 26), (22, 26),
        (23, 26), (24, 26), (25, 26),
        (26, 26),
    ]

    def __init__(self):
        self.oled = Oled()
        self.key0 = Pin(15, Pin.IN, Pin.PULL_UP)
        self.key1 = Pin(17, Pin.IN, Pin.PULL_UP)

        self.mode = "Home"
        self.selection_home = 0
        self.selection_insert = 1
        self.status = "Tuning"
        self.ignore_next_key_release = False

        self.dunk_time: float = 2
        self.cool_time: float = 10

        self.draw_home_screen()
        self.oled.show()

        # Enable interrupts
        self.key0.irq(lambda _: self.key_pressed(0), Pin.IRQ_RISING)
        self.key1.irq(lambda _: self.key_pressed(1), Pin.IRQ_RISING)

        # Start a new process to tune the servo motor
        start_new_thread(self.tune_servo, tuple())

    def tune_servo(self):
        """Tune the servo motor (move the peg to the corrct height)"""
        sleep(10)  # TODO: Tune servo motor to correct height

        self.status = "Ready"
        if self.mode == "Wait":
            self.mode = "Insert"
            self.selection_insert = 1
            self.draw_insert_teabag_screen()
        else:
            self.draw_menu_bar()
        self.oled.show()

    def get_dunk_time(self) -> str:
        if float(int(self.dunk_time)) == self.dunk_time:
            return str(int(self.dunk_time))
        else:
            return str(self.dunk_time)

    def get_cool_time(self) -> str:
        if float(int(self.cool_time)) == self.cool_time:
            return str(int(self.cool_time))
        else:
            return str(self.cool_time)

    def draw_menu_bar(self):
        """Draw the menu bar for the TurboTea with the given status"""
        # Draw the rectangle
        self.oled.rect(0, 0, 128, 10, 1, True)

        # Draw the TurboTea text
        self.oled.text("TurboTea", 1, 1, 0)

        # Draw the status text
        self.oled.text(self.status, 127 - (8 * len(self.status)), 1, 0)

    def draw_cool_logo(self, x: int, y: int, colour: int):
        """Draw a cool icon with the top-left corner at the given
        coordinates"""
        self.oled.ellipse(x + 13, y + 13, 13, 13, colour)
        self.oled.vline(x + 12, y + 3, 11, colour)
        self.oled.line(x + 12, y + 14, x + 18, y + 9, colour)

    def draw_image(self, x: int, y: int, image: [(int, int)],
                   colour: int):
        """Draw an image with the top-left corner at the given coordinates"""
        for px_x, px_y in image:
            self.oled.pixel(x + px_x, y + px_y, colour)

    def draw_home_screen(self):
        """Draw the main screen"""
        # Draw the background
        self.oled.fill(0)

        # Draw the menu bar
        self.draw_menu_bar()

        if self.selection_home == 0:  # Run selected
            run_colour = 0
            dunk_colour = 1
            cool_colour = 1
            selected_x = 0
        elif self.selection_home == 1:  # Dunk selected
            run_colour = 1
            dunk_colour = 0
            cool_colour = 1
            selected_x = 43
        else:  # Cool selected
            run_colour = 1
            dunk_colour = 1
            cool_colour = 0
            selected_x = 86

        # Draw the selected rectangle
        self.oled.rect(selected_x, 11, 42, 53, 1, True)

        # Draw the run button
        self.oled.text("Run", 9, 14, run_colour)  # Run text
        # Run logo
        height = 12
        for column in range(19):
            for row in range(12 - height, 13 + height):
                self.oled.pixel(13 + column, 25 + row, run_colour)
            if column % 3 != 0:
                height -= 1

        # Draw the dunk button
        self.oled.text("Dunk", 48, 14, dunk_colour)  # Dunk text
        self.draw_image(50, 24, self.TEABAG_IMAGE, dunk_colour)  # Dunk logo
        self.oled.text(
            f"{self.get_dunk_time()}m",
            60 - (4 * len(self.get_dunk_time())),
            54,
            dunk_colour
        )  # Dunk value

        # Draw the cool button
        self.oled.text("Cool", 91, 14, cool_colour)  # Cool text
        self.draw_cool_logo(94, 25, cool_colour)  # Cool logo
        self.oled.text(
            f"{str(self.get_cool_time())}m",
            103 - (4 * len(str(self.get_cool_time()))),
            54,
            cool_colour
        )  # Cool value

    def draw_adjust_screen(self):
        """Draw the adjust screen"""
        # Draw the background
        self.oled.fill(0)

        # Draw the menu bar
        self.draw_menu_bar()

        # Draw the arrows
        width = 1
        for row in range(11):
            for column in range(12 - width, 13 + width):
                self.oled.pixel(column, 21 + row, 1)
            if row % 3 != 0:
                width += 1
        width -= 1
        for row in range(11):
            for column in range(12 - width, 13 + width):
                self.oled.pixel(column, 42 + row, 1)
            if row % 3 != 0:
                width -= 1

        # Draw the exit text
        self.oled.text("A+B: Save", 21, 54, 1)

        # Draw the title underline
        self.oled.hline(48, 21, 32, 1)

        if self.selection_home == 1:  # Dunk selected
            # Draw the heading
            self.oled.text("Dunk", 48, 13, 1)

            # Draw the time text
            self.oled.text(
                f"{str(self.get_dunk_time())} min{'s' if self.dunk_time != 1 else ''}",
                45-(4*len(str(self.get_dunk_time()))),
                29,
                1
            )

            self.draw_image(98, 34, self.TEABAG_IMAGE, 1)
        else:  # Cool selected
            # Draw the heading
            self.oled.text("Cool", 48, 13, 1)

            # Draw the time text
            self.oled.text(
                f"{str(self.get_cool_time())} min{'s' if self.cool_time != 1 else ''}",
                45-(4*len(str(self.get_cool_time()))),
                29,
                1
            )

            self.draw_cool_logo(98, 34, 1)

    def draw_wait_screen(self):
        # Draw the background
        self.oled.fill(0)

        # Draw the menu bar
        self.draw_menu_bar()

        # Draw the please wait text
        self.oled.text("Please wait", 20, 18, 1)
        self.oled.text("for tuning", 24, 27, 1)
        self.oled.text("to finish.", 24, 36, 1)

        # Draw the cancel button
        self.oled.rect(32, 52, 64, 12, 1, True)  # Rectangle
        self.oled.text("Cancel", 40, 54, 0)  # Cancel text

    def draw_insert_teabag_screen(self):
        # Draw the background
        self.oled.fill(0)

        # Draw the menu bar
        self.draw_menu_bar()

        # Draw the insert teabag text
        self.oled.text("Insert tea bag", 8, 24, 1)
        self.oled.text("then press OK", 12, 33, 1)

        # Draw the cancel button
        self.oled.rect(0, 52, 64, 12, 1-self.selection_insert, True)
        self.oled.text("Cancel", 8, 54, self.selection_insert)

        # Draw the OK button
        self.oled.rect(64, 52, 64, 12, self.selection_insert, True)
        self.oled.text("OK", 88, 54, 1-self.selection_insert)

    def key_pressed(self, key: int):
        """Update the display when one of the buttons is released"""
        if self.ignore_next_key_release:
            if key == 0 and self.key1.value():
                self.ignore_next_key_release = False
            elif key == 1 and self.key0.value():
                self.ignore_next_key_release = False
            return

        if self.mode == "Home":
            if key == 0:
                self.selection_home = (self.selection_home + 1) % 3
                self.draw_home_screen()
            else:
                if self.selection_home == 0:
                    if self.status == "Tuning":
                        self.mode = "Wait"
                        self.draw_wait_screen()
                    else:
                        self.mode = "Insert"
                        self.selection_insert = 1
                        self.draw_insert_teabag_screen()
                else:
                    self.mode = "Adjust"
                    self.draw_adjust_screen()
            self.oled.show()

        elif self.mode == "Adjust":
            if key == 0:
                other_key: Pin = self.key1
            else:
                other_key: Pin = self.key0
            if not other_key.value():  # Exit
                self.mode = "Home"
                self.draw_home_screen()
                self.oled.show()
                self.ignore_next_key_release = True
            else:  # Adjust
                change = 0
                if self.selection_home == 1:  # Dunk adjust
                    current_value = self.dunk_time
                else:  # Cool adjust
                    current_value = self.cool_time
                if key == 0:  # Up
                    if current_value < 10:  # Up to 10
                        change = 0.5
                    elif current_value < 99:  # 11 to 99
                        change = 1
                    else:  # 100+
                        # TODO: play error sound
                        pass
                else:  # Down
                    if current_value > 10:  # 11 to 99
                        change = -1
                    elif current_value > 0:  # 0.5 to 10
                        change = -0.5
                    else:  # 0-
                        # TODO: play error sound
                        pass
                if self.selection_home == 1:  # Dunk adjust
                    self.dunk_time += change
                else:  # Cool adjust
                    self.cool_time += change
                if change:
                    self.draw_adjust_screen()
                    self.oled.show()

        elif self.mode == "Wait":
            if key == 1:  # Cancel
                self.mode = "Home"
                self.draw_home_screen()
                self.oled.show()

        elif self.mode == "Insert":
            if key == 0:
                self.selection_insert = (self.selection_insert + 1) % 2
                self.draw_insert_teabag_screen()
            else:
                if self.selection_insert == 0:
                    self.mode = "Home"
                    self.draw_home_screen()
                else:
                    self.mode = "Making"
                    self.status = "Making"
                    self.draw_menu_bar()  # TODO: Show make screen
                    # TODO: Make tea
            self.oled.show()


if __name__ == "__main__":
    TurboTea()
