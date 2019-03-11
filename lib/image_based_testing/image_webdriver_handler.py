from lib.image_based_testing.image_base_handler import ImageBaseHandler


class ImageWebdriverHandler(ImageBaseHandler):

    def __init__(self, target_img_path=None, full_img_path=None, result_img_path=None, threshold=None, window_size=None):
        super(ImageWebdriverHandler, self).__init__(target_img_path=target_img_path,
                                                    full_img_path=full_img_path,
                                                    result_img_path=result_img_path,
                                                    threshold=threshold)
        self.matching_img_y_cord = None
        self.matching_img_x_cord = None
        self.window_size = window_size
        self.standard_minus_current_difference = None

    def get_image_occurrence_coordinates(self, target_image_path, full_image_path, window_size):
        if not self.find_img_on_screen(target_img_path=target_image_path, full_img_path=full_image_path, draw_rectangle=False):
            raise Exception(
                        4 * "<" + "[ERROR]" + 4 * ">" +
                        "\n" +
                        "NO IMAGE Occurrence Found."
                        + "\n")
        else:
            return self.get_web_element_coordinates(window_size)

    def get_web_element_coordinates(self, window_size):
        self.window_size = window_size
        h, w = self.target_img.shape[:-1]

        size_diff_factor = self.full_img.shape[1] / self.window_size['width']

        for pt in zip(*self.occurrences[::-1]):
            # WebDriver X Coordinate
            self.matching_img_x_cord = int(pt[0] / size_diff_factor) + int(w / size_diff_factor / 2)

            # WebDriver Y Coordinate
            self.matching_img_y_cord = int(pt[1] / size_diff_factor) + int(h / size_diff_factor / 2)

            return [self.matching_img_x_cord, self.matching_img_y_cord]
