"""
This is a simple window-application made in Python 3.7 with Arcade 2.3.5 library. Application is a simple quiz about
guessing correct characters from WH40k setting. User clicks on the portraits trying to select only characters aligned
to the chosen fraction. As long as his choices are correct, he can continue picking characters. When he makes a mistake,
quiz is restarted.
"""
import arcade


def get_screen_size():
    from ctypes import windll
    user32 = windll.user32
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


class Quiz(arcade.Window):

    def __init__(self, screen_width, screen_height, window_title):
        super().__init__(screen_width, screen_height, window_title)
        self.characters = []

        self.restart_quiz()

    def restart_quiz(self):
        self.characters = self.get_random_characters()

    def get_random_characters(self):
        """
        TODO: return x randomly ordered characters images and assign them to buttons
        :return: list
        """
        return []

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        raise NotImplementedError

    def on_correct_choice(self):
        # TODO: select character [ ] and allo player to continue selecting [ ]
        raise NotImplementedError

    def on_wrong_choice(self):
        # TODO: display error image [ ] and restart game [ ]
        raise NotImplementedError


if __name__ == '__main__':
    TITLE = "WH40k Quiz"
    SCREEN_W, SCREEN_H = get_screen_size()
    quiz = Quiz(SCREEN_W, SCREEN_H, TITLE)
    arcade.run()

