"""
This is a simple window-application made in Python 3.7 with Arcade 2.3.5 library.
Application is a simple quiz about guessing correct characters from WH40k setting.
User clicks on the portraits trying to select only characters aligned to the
chosen fraction. As long as his choices are correct, he can continue picking
characters. When he makes a mistake, quiz is restarted.
"""
import os
import random
import arcade


SCREEN_W, SCREEN_H = 0, 0
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
TITLE = "WH40k Quiz"
EXCELLENT = 'EXCELLENT!'
INCORRECT = "INCORRECT!"
draw_rect_outl = arcade.draw_lrtb_rectangle_outline
draw_rect_fill = arcade.draw_lrtb_rectangle_filled
draw_text = arcade.draw_text


def get_screen_size() -> tuple:
    from ctypes import windll
    user32 = windll.user32
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


class SelectionsSpriteLists(arcade.SpriteList):
    """
    Reason for this wrapper is additional method allowing displaying green
    rectangle around 'selected' sprites.
    """

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
        draw_rect_outl(left, right, top, bottom, GREEN)


class Button:
    # TODO: implement restart-button [x]

    def __init__(self, x, y, width, height, text=None, text_color=BLACK,
                 function=None, outline_color=WHITE, fill_color=WHITE):
        self.text = text
        self.text_color = text_color
        self.function = function
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = (
            x - (width // 2), x + (width // 2),
            y + (height // 2), y - (height // 2)
        )  # (left, right, top, bottom)
        self.outline_color = outline_color
        self.fill_color = fill_color
        self.is_highlighted = False

    def draw(self):
        rect = self.rect
        if self.outline_color is not None:
            draw_rect_outl(rect[0], rect[1], rect[2], rect[3], self.outline_color)

        if self.fill_color is not None:
            draw_rect_fill(rect[0]-1, rect[1]+1, rect[2]-1, rect[3]+1, self.fill_color)

        if self.is_highlighted:
            draw_rect_outl(rect[0]-5, rect[1]+5, rect[2]+5, rect[3]-5, self.outline_color)

        if self.text is not None:
            x, y = (rect[0] + rect[1]) // 2, (rect[2] + rect[3]) // 2
            draw_text(self.text, x, y, self.text_color, font_size=20, bold=True, anchor_x='center', anchor_y='center')

    def is_cursor_above(self, x, y):
        rect = self.rect
        return rect[0] <= x <= rect[1] and rect[3] <= y <= rect[2]

    def on_click(self):
        if self.function is not None:
            self.function()


class Quiz(arcade.Window):

    def __init__(self, screen_width, screen_height, window_title):
        super().__init__(screen_width, screen_height, window_title)
        self.characters_portraits = None
        self.pointed_portrait = None
        self.communicate = None
        self.correct_guesses = 0
        self.win_guesses_count = 0
        self.reset_button = Button(screen_width // 2, screen_height // 2, 200, 50, 'RESTART', function=self.restart_quiz)
        self.restart_quiz()

    def restart_quiz(self):
        self.characters_portraits = self.get_random_characters_portraits()
        self.reset_button.is_highlighted = False
        self.communicate = ''
        self.correct_guesses = 0

    def get_random_characters_portraits(self, rows: int = 3, columns: int = 6) -> SelectionsSpriteLists:
        """
        Search in 'correct' and 'incorrect' folders for image files to be loaded
        and used as choice-options in the quiz and randomly displace them in the
        choices-list.
        TODO: return x randomly ordered characters images and assign them to buttons [x]
        :return: SelectionSpriteList
        """
        col_offset = (SCREEN_W - 100) / (columns + 1)
        row_offset = SCREEN_H / (rows + 1)
        this_folder = os.getcwd()  # os.path.dirname(__file__)  # os.path.abspath()
        correct_dir = this_folder + '/images/portraits/correct/'
        incorrect_dir = this_folder + '/images/portraits/incorrect/'

        characters, correct_choices, incorrect_choices = [], set(), set()

        for file in os.listdir(correct_dir):
            characters.append(file)
            correct_choices.add(file)
        self.win_guesses_count = len(correct_choices)

        for file in os.listdir(incorrect_dir):
            characters.append(file)
            incorrect_choices.add(file)

        portraits = SelectionsSpriteLists()
        if characters:
            random.shuffle(characters)  # each game would mix portraits in random order
            for i in range(rows):
                for j in range(columns):
                    if not characters:
                        return portraits
                    name = characters.pop()
                    correct = name in correct_choices
                    image = correct_dir + name if correct else incorrect_dir + name
                    x, y = (j + 1) * row_offset, (i + 1) * col_offset
                    portraits.append(CharacterPortrait(image, x, y, correct))
        return portraits

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        # TODO: check if mouse points at any character-portrait image [x] if so, highlight it [x]
        if self.characters_portraits is not None:
            self.pointed_portrait = None
            for portrait in self.characters_portraits:
                if portrait.is_cursor_above(x, y):
                    self.pointed_portrait = portrait
                    break
        elif not self.reset_button.is_highlighted:
            if self.reset_button.is_cursor_above(x, y):
                self.reset_button.is_highlighted = True
        elif not self.reset_button.is_cursor_above(x, y):
            self.reset_button.is_highlighted = False

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if self.characters_portraits is not None:
            if self.pointed_portrait is not None:
                if self.pointed_portrait.is_correct:
                    if not self.pointed_portrait.selected:
                        self.on_correct_choice()
                else:
                    self.on_wrong_choice()
        elif self.reset_button.is_highlighted:
            self.reset_button.on_click()

    def on_correct_choice(self):
        # TODO: select character [x] and allow player to continue selecting [x]
        self.correct_guesses += 1
        self.pointed_portrait.selected = True
        if self.correct_guesses == self.win_guesses_count:
            self.on_quiz_completed()

    def on_wrong_choice(self):
        # TODO: display error image [x] and button to restart game [x]
        self.characters_portraits = None
        self.communicate = INCORRECT

    def on_update(self, delta_time: float):
        if self.characters_portraits is not None:
            self.characters_portraits.update()

    def on_draw(self):
        arcade.start_render()
        if self.characters_portraits is not None:
            self.characters_portraits.draw()
            self.characters_portraits.draw_selections()  # show already clicked items

            if self.pointed_portrait is not None:
                self.highlight_pointed_portrait()  # highlight pointed item
        else:
            self.draw_communicate()
            self.reset_button.draw()

    def draw_communicate(self):
        color = RED if self.communicate == INCORRECT else GREEN
        draw_text(self.communicate, (SCREEN_W // 2), (SCREEN_H // 3) * 2, color, 30, bold=True, anchor_x='center')

    def highlight_pointed_portrait(self):
        left = self.pointed_portrait.left - 5
        right = self.pointed_portrait.right + 5
        top = self.pointed_portrait.top + 5
        bottom = self.pointed_portrait.bottom - 5
        draw_rect_outl(left, right, top, bottom, WHITE)

    def on_quiz_completed(self):
        self.characters_portraits = None
        self.communicate = EXCELLENT


if __name__ == '__main__':
    SCREEN_W, SCREEN_H = get_screen_size()
    quiz = Quiz(SCREEN_W, SCREEN_H, TITLE)
    arcade.run()
