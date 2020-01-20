"""
This is a simple window-application made in Python 3.7 with Arcade 2.3.5 library. Application is a simple quiz about
guessing correct characters from WH40k setting. User clicks on the portraits trying to select only characters aligned
to the chosen fraction. As long as his choices are correct, he can continue picking characters. When he makes a mistake,
quiz is restarted.
"""
import arcade


SCREEN_W, SCREEN_H = 0, 0


def get_screen_size():
    from ctypes import windll
    user32 = windll.user32
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


class CharacterPortrait(arcade.Sprite):

    def __init__(self, image: str, x: int, y: int, is_correct: bool):
        super().__init__(image, x, y)
        self.is_correct = is_correct

    def is_cursor_above(self, x, y):
        raise NotImplementedError


class Quiz(arcade.Window):

    def __init__(self, screen_width, screen_height, window_title):
        super().__init__(screen_width, screen_height, window_title)
        self.characters_portraits = None
        self.restart_quiz()

    def restart_quiz(self):
        self.characters_portraits = self.get_random_characters_portraits()

    @staticmethod
    def get_random_characters_portraits(rows: int = 3, columns: int = 6) -> arcade.SpriteList:
        """
        TODO: return x randomly ordered characters images and assign them to buttons
        :return: list
        """
        row_offset = SCREEN_W // columns
        col_offset = SCREEN_H // rows
        images_path = "/images/"

        characters, correct_choices, incorrect_choices = [], set(), set()
        correct = False
        with open("config.txt", "r") as file:
            for line in file.readlines():
                if line.startswith("#"):
                    if line.startswith("# CORRECT"):
                        correct = True
                    continue
                if line == "\n":
                    continue
                if correct:
                    correct_choices.add(line)
                else:
                    incorrect_choices.add(line)
                characters.append(line)

        portraits = arcade.SpriteList()
        if characters:
            for i in range(rows):
                for j in range(columns):
                    name = characters.pop()
                    image = images_path + name
                    correct = name in correct_choices
                    portraits.append(CharacterPortrait(image, i*row_offset, j*col_offset, correct))
        return portraits

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        # TODO: check if mouse points at any character-portrait image [ ] if so, highlight it []
        pass

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        raise NotImplementedError

    def on_correct_choice(self):
        # TODO: select character [ ] and allo player to continue selecting [ ]
        raise NotImplementedError

    def on_wrong_choice(self):
        # TODO: display error image [ ] and restart game [ ]
        raise NotImplementedError

    def on_update(self, delta_time: float):
        self.characters_portraits.update()

    def on_draw(self):
        arcade.start_render()
        self.characters_portraits.draw()


if __name__ == '__main__':
    TITLE = "WH40k Quiz"
    SCREEN_W, SCREEN_H = get_screen_size()
    quiz = Quiz(SCREEN_W, SCREEN_H, TITLE)
    arcade.run()

