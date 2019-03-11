import pyscreenshot as image_grab
from pymouse import PyMouse
from pykeyboard import PyKeyboard
from lib.image_based_testing.image_base_handler import ImageBaseHandler


class ImageDesktopHandler(ImageBaseHandler):

    def __init__(self, full_img_path=None, target_img_path=None, result_img_path=None, threshold=None):
        super(ImageDesktopHandler, self).__init__(target_img_path=target_img_path,
                                                  full_img_path=full_img_path,
                                                  result_img_path=result_img_path,
                                                  threshold=threshold)
        self.img = None
        self.mouse = PyMouse()
        self.keyboard = PyKeyboard()

    def grab_screen(self, path):
        """
        Takes a full screenshot of the visible desktop.
        :param path: Output path.
        :return: None
        """
        self.full_img_path = path
        self.img = image_grab.grab()
        self.img.save(self.full_img_path)

    def click(self, button="left"):
        # Check if screen size
        self.__check_and_fix_screen_size()

        if button.lower() == "left":
            button = 1
        elif button.lower() == "right":
            button = 2
        elif button.lower() == "middle":
            button = 3

        self.mouse.click(int(self.matching_img_x_cord), int(self.matching_img_y_cord), button=button, n=1)

    def __check_and_fix_screen_size(self):
        x_dim, y_dim = self.mouse.screen_size()
        x_ratio = self.img.width / x_dim
        y_ratio = self.img.height / y_dim

        if x_ratio > 1:
            self.matching_img_x_cord = self.matching_img_x_cord / x_ratio
        if y_ratio > 1:
            self.matching_img_y_cord = self.matching_img_y_cord / y_ratio
