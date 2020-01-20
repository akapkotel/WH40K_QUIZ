"""
This is a simple window-application made in Python 3.7 with Arcade 2.3.5 library. Application is a simple quiz about
guessing correct characters from WH40k setting. User clicks on the portraits trying to select only characters aligned
to the chosen fraction. As long as his choices are correct, he can continue picking characters. When he makes a mistake,
quiz is restarted.
"""
import os
import random
import arcade


SCREEN_W, SCREEN_H = 0, 0
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


def get_screen_size():
    from ctypes import windll
    user32 = windll.user32
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


class SelectionsSpriteLists(arcade.SpriteList):

    def draw_selections(self):
        for sprite in self.sprite_list:
            if sprite.selected:
                sprite.draw_selection()


class CharacterPortrait(arcade.Sprite):

    def __init__(self, image: str, x: int, y: int, is_correct: bool):
        super().__init__(image)
        self.set_position(x, y)
        self.is_correct = is_correct
        self.selected = False

    def is_cursor_above(self, x, y):
        return self.left <= x <= self.right and self.bottom <= y <= self.top

    def draw_selection(self):
        left = self.left - 5
        right = self.right + 5
        top = self.top + 5
        bottom = self.bottom - 5
        arcade.draw_lrtb_rectangle_outline(left, right, top, bottom, GREEN)


class Quiz(arcade.Window):

    def __init__(self, screen_width, screen_height, window_title):
        super().__init__(screen_width, screen_height, window_title)
        self.characters_portraits = None
        self.pointed_portrait = None
        self.correct_guesses = 0
        self.win_guesses_count = 0
        self.restart_quiz()

    def restart_quiz(self):
        self.characters_portraits = self.get_random_characters_portraits()

    def get_random_characters_portraits(self, rows: int = 3, columns: int = 6) -> arcade.SpriteList:
        """
        TODO: return x randomly ordered characters images and assign them to buttons
        :return: list
        """
        col_offset = (SCREEN_W - 100) / (columns + 1)
        row_offset = SCREEN_H / (rows + 1)
        this_folder = os.path.dirname(os.path.abspath(__file__))

        images_path = this_folder + '/images/portraits/'

        characters, correct_choices, incorrect_choices = [], set(), set()
        correct = False
        with open("config.txt", "r") as file:
            for line in file.readlines():
                if line.startswith("#") or line.startswith("INCORRECT") or line == "\n":
                    continue
                if line == "CORRECT IMAGES:\n":
                    correct = True
                    continue
                if not correct:
                    incorrect_choices.add(line.rstrip('\n'))
                else:
                    correct_choices.add(line.rstrip('\n'))
                characters.append(line.rstrip('\n'))
        self.win_guesses_count = len(correct_choices)

        portraits = SelectionsSpriteLists()
        if characters:
            random.shuffle(characters)  # each game would mix portraits in random order
            for i in range(rows):
                for j in range(columns):
                    name = characters.pop()
                    image = images_path + name
                    correct = name in correct_choices
                    portraits.append(CharacterPortrait(image, (j+1) * row_offset, (i+1) * col_offset, correct))
        return portraits

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        # TODO: check if mouse points at any character-portrait image [ ] if so, highlight it []
        if self.characters_portraits:
            self.pointed_portrait = None
            for portrait in self.characters_portraits:
                if portrait.is_cursor_above(x, y):
                    self.pointed_portrait = portrait
                    break

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if self.pointed_portrait is not None:
            if self.pointed_portrait.is_correct:
                if not self.pointed_portrait.selected:
                    self.on_correct_choice()
            else:
                self.on_wrong_choice()

    def on_correct_choice(self):
        # TODO: select character [ ] and allow player to continue selecting [ ]
        self.correct_guesses += 1
        self.pointed_portrait.selected = True
        if self.correct_guesses == self.win_guesses_count:
            raise NotImplementedError

    def on_wrong_choice(self):
        # TODO: display error image [ ] and button to restart game [ ]
        self.restart_quiz()

    def on_update(self, delta_time: float):
        self.characters_portraits.update()

    def on_draw(self):
        arcade.start_render()
        self.characters_portraits.draw()
        self.characters_portraits.draw_selections()

        if self.pointed_portrait is not None:
            self.draw_portrait_highlight()

    def draw_portrait_highlight(self):
        left = self.pointed_portrait.left - 5
        right = self.pointed_portrait.right + 5
        top = self.pointed_portrait.top + 5
        bottom = self.pointed_portrait.bottom - 5
        arcade.draw_lrtb_rectangle_outline(left, right, top, bottom, WHITE)


if __name__ == '__main__':
    TITLE = "WH40k Quiz"
    SCREEN_W, SCREEN_H = get_screen_size()
    quiz = Quiz(SCREEN_W, SCREEN_H, TITLE)
    arcade.run()

