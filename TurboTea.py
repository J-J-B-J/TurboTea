from OLED import *
from machine import Pin, Timer, PWM
from _thread import start_new_thread
from time import sleep, ticks_ms, sleep_ms


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

    TEAPOT_IMAGE = [
        # A list of (x, y) coordinates that represent a teapot image
        (5, 0), (10, 0),
        (4, 1), (5, 1), (9, 1), (10, 1),
        (3, 2), (4, 2), (8, 2), (9, 2),
        (3, 3), (4, 3), (8, 3), (9, 3),
        (4, 4), (5, 4), (9, 4), (10, 4),
        (5, 5), (6, 5), (10, 5), (11, 5),
        (5, 6), (6, 6), (7, 6), (10, 6), (11, 6), (12, 6),
        (6, 7), (7, 7), (8, 7), (11, 7), (12, 7), (13, 7),
        (6, 8), (7, 8), (8, 8), (11, 8), (12, 8), (13, 8),
        (5, 9), (6, 9), (7, 9), (10, 9), (11, 9), (12, 9),
        # ROW 10 IS EMPTY
        (0, 11), (1, 11), (2, 11), (3, 11), (4, 11), (5, 11), (6, 11), (7, 11),
        (8, 11), (9, 11), (10, 11), (11, 11), (12, 11), (13, 11), (14, 11),
        (15, 11), (16, 11), (17, 11),
        (0, 12), (17, 12),
        (0, 13), (17, 13), (18, 13), (19, 13), (20, 13),
        (0, 14), (17, 14), (18, 14), (19, 14), (20, 14), (21, 14),
        (0, 15), (17, 15), (18, 15), (19, 15), (20, 15), (21, 15),
        (0, 16), (17, 16), (18, 16), (20, 16), (21, 16),
        (0, 17), (17, 17), (18, 17), (20, 17), (21, 17),
        (0, 18), (17, 18), (18, 18), (20, 18), (21, 18),
        (0, 19), (17, 19), (18, 19), (20, 19), (21, 19),
        (0, 20), (17, 20), (18, 20), (19, 20), (20, 20),
        (0, 21), (17, 21), (18, 21), (19, 21), (20, 21),
        (0, 22), (17, 22),
        (0, 23), (17, 23),
        (1, 24), (16, 24),
        (1, 25), (2, 25), (15, 25), (16, 25),
        (2, 26), (3, 26), (14, 26), (15, 26),
        (3, 27), (4, 27), (5, 27), (6, 27), (7, 27), (8, 27), (9, 27),
        (10, 27), (11, 27), (12, 27), (13, 27), (14, 27),
    ]

    def __init__(self):
        self.oled = Oled()
        self.key0_rising = Pin(14, Pin.IN, Pin.PULL_UP)
        self.key0_falling = self.key0 = Pin(15, Pin.IN, Pin.PULL_UP)
        self.key1_rising = Pin(16, Pin.IN, Pin.PULL_UP)
        self.key1_falling = self.key1 = Pin(17, Pin.IN, Pin.PULL_UP)
        self.speaker = PWM(Pin(0))

        self.mode = "Home"
        self.selection_home = 0
        self.selection_insert = 1
        self.status = "Tuning"
        self.ignore_next_key_releases = 0

        self.dunk_time: float = 2
        self.cool_time: float = 10
        self.start_time: float = 0  # Time that the tea was started.
        self.rise_teabag_timer = Timer()
        self.update_display_timer = Timer()
        self.beep_start_time = 0

        self.draw_home_screen()
        self.oled.show()

        # Enable interrupts
        self.key0_rising.irq(lambda _: self.key_released(0), Pin.IRQ_RISING)
        self.key1_rising.irq(lambda _: self.key_released(1), Pin.IRQ_RISING)
        self.key0_falling.irq(lambda _: self.key_pressed(0), Pin.IRQ_FALLING)
        self.key1_falling.irq(lambda _: self.key_pressed(1), Pin.IRQ_FALLING)

        # Start a new process to tune the servo motor
        start_new_thread(self.tune_servo, tuple())

    def tune_servo(self):
        """Tune the servo motor (move the peg to the corrct height)"""
        sleep(2)  # TODO: Tune servo motor to correct height

        self.status = "Ready"
        if self.mode == "Wait":
            self.mode = "Insert"
            self.selection_insert = 1
            self.draw_insert_teabag_screen()
        else:
            self.draw_menu_bar()
        self.oled.show()

    def lower_teabag(self, *_):
        """Lower the teabag into the pot"""
        print("Lowering teabag")  # TODO: lower teabag

    def raise_teabag(self, *_):
        """Raise the teabag from the pot"""
        print("Raising teabag")  # TODO: raise teabag

    def make_tea(self):
        """Make the tea"""
        if self.dunk_time:
            self.lower_teabag()

            self.rise_teabag_timer.init(
                mode=Timer.ONE_SHOT,
                period=int(self.dunk_time * 60_000),
                callback=self.raise_teabag
            )

    def tea_done_sound(self):
        """Play a sound for the tea finishing"""
        while True:
            self.speaker.freq(262)
            if self.mode != "Finished":
                return
            self.speaker.duty_u16(60000)
            for frequency in [294, 330, 392]:
                sleep_ms(150)
                if self.mode != "Finished":
                    self.speaker.duty_u16(0)
                    return
                self.speaker.freq(frequency)
            sleep_ms(200)
            self.speaker.duty_u16(0)
            sleep_ms(5000)

    def beep_sound_start(self):
        """Start a sound for pressing a button"""
        self.beep_start_time = ticks_ms()
        self.speaker.freq(500)
        self.speaker.duty_u16(1000)

    def beep_sound_end(self):
        """End a sound for pressing a button"""
        while ticks_ms() - 50 < self.beep_start_time:
            pass
        self.speaker.duty_u16(0)

    def error_sound(self):
        """Play a sound for an error"""
        if not self.speaker.duty_u16():
            self.speaker.freq(500)
            self.speaker.duty_u16(1000)
        while ticks_ms() - 100 < self.beep_start_time:
            pass
        self.speaker.freq(400)
        sleep_ms(100)
        self.speaker.duty_u16(0)

    def update_time(self, *_):
        if (ticks_ms() / 1000 >= 60 * (self.dunk_time + self.cool_time) +
                self.start_time):
            self.update_display_timer.deinit()
            self.mode = "Finished"
            start_new_thread(self.tea_done_sound, tuple())
            self.draw_finish_screen()
            self.oled.show()
            return
        if self.mode != "Making":  # Cancelled
            self.update_display_timer.deinit()
            return

        self.draw_make_screen()
        self.oled.show()

    def get_dunk_str(self) -> str:
        if float(int(self.dunk_time)) == self.dunk_time:
            return str(int(self.dunk_time))
        else:
            return str(self.dunk_time)

    def get_cool_str(self) -> str:
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
        self.oled.ellipse(x + 13, y + 13, 13, 13, colour, False, 15)
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
            f"{self.get_dunk_str()}m",
            60 - (4 * len(self.get_dunk_str())),
            54,
            dunk_colour
        )  # Dunk value

        # Draw the cool button
        self.oled.text("Cool", 91, 14, cool_colour)  # Cool text
        self.draw_cool_logo(94, 24, cool_colour)  # Cool logo
        self.oled.text(
            f"{str(self.get_cool_str())}m",
            103 - (4 * len(str(self.get_cool_str()))),
            54,
            cool_colour
        )  # Cool value

    def draw_adjust_screen(self, highlight_arrow=0):
        """Draw the adjust screen"""
        # Draw the background
        self.oled.fill(0)

        # Draw the menu bar
        self.draw_menu_bar()

        # Draw the arrows
        width = 1
        for row in range(11):
            if highlight_arrow == 1 or row == 0 or row == 10:
                for column in range(12 - width, 13 + width):
                    self.oled.pixel(column, 21 + row, 1)
            else:
                self.oled.pixel(12 - width, 21 + row, 1)
                self.oled.pixel(12 + width, 21 + row, 1)
            if row % 3 != 0:
                width += 1
        width -= 1
        for row in range(11):
            if highlight_arrow == 2 or row == 0 or row == 10:
                for column in range(12 - width, 13 + width):
                    self.oled.pixel(column, 42 + row, 1)
            else:
                self.oled.pixel(12 - width, 42 + row, 1)
                self.oled.pixel(12 + width, 42 + row, 1)
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
                f"{str(self.get_dunk_str())} min" +
                ('s' if self.dunk_time != 1 else ''),
                45 - (4 * len(str(self.get_dunk_str()))),
                29,
                1
            )

            self.draw_image(98, 34, self.TEABAG_IMAGE, 1)
        else:  # Cool selected
            # Draw the heading
            self.oled.text("Cool", 48, 13, 1)

            # Draw the time text
            self.oled.text(
                f"{str(self.get_cool_str())} min" +
                ('s' if self.cool_time != 1 else ''),
                45 - (4 * len(str(self.get_cool_str()))),
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
        self.oled.rect(0, 52, 64, 12, 1 - self.selection_insert, True)
        self.oled.text("Cancel", 8, 54, self.selection_insert)

        # Draw the OK button
        self.oled.rect(64, 52, 64, 12, self.selection_insert, True)
        self.oled.text("OK", 88, 54, 1 - self.selection_insert)

    def draw_make_screen(self):
        # Draw the background
        self.oled.fill(0)

        # Draw the menu bar
        self.draw_menu_bar()

        # Draw the time text
        total_time = (self.dunk_time + self.cool_time) * 60
        time_so_far = int(ticks_ms() / 1000) - self.start_time
        time_remaining = total_time - time_so_far
        mins_remaining = str(int(time_remaining // 60))
        secs_remaining = str(int(time_remaining % 60))
        if time_remaining % 60 < 10:
            secs_remaining = "0" + secs_remaining
        time_text = f"{mins_remaining}:{secs_remaining}"
        self.oled.text(time_text, 64 - (4 * len(time_text)), 21, 1)

        # Draw the progress bar
        self.oled.rect(6, 33, 116, 8, 1, False)
        try:
            self.oled.rect(6, 33, int(116 * (time_so_far / total_time)), 8, 1,
                           True)
        except ZeroDivisionError:
            self.oled.rect(6, 33, 116, 8, 1, True)

        # Draw the cancel button
        self.oled.rect(32, 52, 64, 12, 1, True)  # Rectangle
        self.oled.text("Cancel", 40, 54, 0)  # Cancel text

    def draw_finish_screen(self):
        # Draw the background
        self.oled.fill(0)

        # Draw the menu bar
        self.draw_menu_bar()

        # Draw the finished text
        self.oled.text("Finished", 32, 28, 1)

        # Draw the teapot image
        self.draw_image(103, 25, self.TEAPOT_IMAGE, 1)

        # Draw the OK button
        self.oled.rect(32, 52, 64, 12, 1, True)  # Rectangle
        self.oled.text("OK", 56, 54, 0)  # OK text

    def key_pressed(self, key: int):
        """Update the display when one of the buttons is pressed"""
        if (not self.key0.value()) and (not self.key1.value()) and \
                self.mode != "Adjust":
            # Holding down two buttons
            self.ignore_next_key_releases += 1
            return

        if (key == 0 and self.key0.value()) or (
                key == 1 and self.key1.value()):
            # Key has been released already. Performing the action now would be
            # too unresponsive
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
                    self.ignore_next_key_releases += 1
                    self.mode = "Adjust"
                    self.draw_adjust_screen()
            self.beep_sound_start()
            self.oled.show()
            self.beep_sound_end()

        elif self.mode == "Adjust":
            if key == 0:
                other_key: Pin = self.key1
            else:
                other_key: Pin = self.key0
            if other_key.value():  # Highlight
                if key == 0:
                    self.draw_adjust_screen(1)
                else:
                    self.draw_adjust_screen(2)
            else:  # Exit
                self.mode = "Home"
                self.draw_home_screen()
                self.ignore_next_key_releases = 2
            self.beep_sound_start()
            self.oled.show()
            self.beep_sound_end()

        elif self.mode == "Wait" or self.mode == "Finished":
            if key == 1:  # Cancel (Wait) or OK (Finished)
                self.mode = "Home"
                self.draw_home_screen()
                self.beep_sound_start()
                self.oled.show()
                self.beep_sound_end()

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
                    self.start_time = ticks_ms() / 1000
                    self.draw_make_screen()
                    self.make_tea()
                    self.update_display_timer.init(period=1000,
                                                   callback=self.update_time)
            self.beep_sound_start()
            self.oled.show()
            self.beep_sound_end()

        elif self.mode == "Making":
            if key == 1:  # Cancel
                self.rise_teabag_timer.deinit()
                self.raise_teabag()
                self.mode = "Home"
                sleep(0.01)
                self.draw_home_screen()
                self.beep_sound_start()
                self.oled.show()
                self.beep_sound_end()

    def key_released(self, key: int):
        """Update the display when one of the buttons is released"""
        if self.ignore_next_key_releases:
            self.ignore_next_key_releases -= 1
            return

        if (key == 0 and (not self.key0.value())) or (
                key == 1 and (not self.key1.value())):
            # Key has been released already. Performing the action now would be
            # too unresponsive
            return

        if self.mode == "Home":
            pass

        elif self.mode == "Adjust":
            if key == 0:
                other_key: Pin = self.key1
            else:
                other_key: Pin = self.key0
            if other_key.value():  # Adjust
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
                        self.error_sound()
                else:  # Down
                    if current_value > 10:  # 11 to 99
                        change = -1
                    elif current_value > 0:  # 0.5 to 10
                        change = -0.5
                    else:  # 0-
                        self.error_sound()
                if self.selection_home == 1:  # Dunk adjust
                    self.dunk_time += change
                else:  # Cool adjust
                    self.cool_time += change
                self.draw_adjust_screen()
                self.oled.show()

        elif self.mode == "Wait" or self.mode == "Finished":
            pass

        elif self.mode == "Insert":
            pass

        elif self.mode == "Making":
            pass


if __name__ == "__main__":
    TurboTea()
