import cv2
import numpy as np
from lib import util


class ImageBaseHandler:
    PROJECT_ROOT = util.get_proyect_root_path()
    STANDARD_WATERMARK_IMG_PATH = PROJECT_ROOT + "/templates/watermarks/standard.png"
    RESULT_WATERMARK_IMG_PATH = PROJECT_ROOT + "/templates/watermarks/result.png"
    DIFFERENCES_WATERMARK_IMG_PATH = PROJECT_ROOT + "/templates/watermarks//differences.png"

    rectangle_thickness = 2
    rectangle_color = (0, 0, 255)
    threshold = 0.99

    def __init__(self, target_img_path, full_img_path, result_img_path, threshold=None,
                 window_size=None):
        # Target Image
        self.target_img_path = target_img_path
        self.target_img = None

        # Screenshot Image
        self.full_img_path = full_img_path
        self.full_img = None

        # Result image
        self.result_img_path = result_img_path
        self.result_img = None

        self.img_occurrences = []
        self.occurrences = None
        self.threshold = threshold if threshold is not None else self.threshold
        self.standard_minus_current_difference = None
        self.matching_img_y_cord = None
        self.matching_img_x_cord = None
        self.target_img_height = None
        self.target_img_width = None

        self.window_size = window_size

    def set_result_img_path(self, result_img_path):
        self.result_img_path = result_img_path

    def set_threshold(self, threshold):
        self.threshold = threshold

    def get_threshold(self):
        return self.threshold

    def set_windows_size(self, windows_size):
        self.window_size = windows_size

    def set_target_image_path(self, target_path):
        self.target_img_path = target_path

    def set_full_image_path(self, full_image_path):
        self.full_img_path = full_image_path

    def find_img_on_screen(self, full_img_path=None, target_img_path=None, draw_rectangle=False):
        """
        Find target image in another image.
        :param target_img_path: Path to target image to be found in screenshot image
        :param full_img_path: Path to full image
        :param draw_rectangle: If a rectangle should be drawn in the full image showing the matching result.
        :return:
        """

        if target_img_path is None:
            if self.target_img_path is None:
                raise Exception("You must specify a target path.")
        else:
            self.target_img_path = target_img_path

        if full_img_path is None:
            if self.full_img_path is None:
                raise Exception("You must specify a screenshot path.")
        else:
            self.full_img_path = full_img_path

        self.target_img = self.get_image(image_path=self.target_img_path)
        self.full_img = self.get_image(image_path=self.full_img_path)

        # Looking for a target image in full image
        self.result_img = self.find_matching(target_img=self.target_img,
                                             full_image=self.full_img,
                                             method=cv2.TM_CCOEFF_NORMED)

        if self.is_image_found(result=self.result_img):
            if draw_rectangle:
                self.draw_rectangle_on_image(full_image=self.full_img,
                                             target_img=self.target_img)
            return True
        else:
            return False

    def find_matching(self, target_img, full_image, method):

        result = cv2.matchTemplate(image=target_img, templ=full_image, method=method)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        top_left = max_loc

        self.target_img_height, self.target_img_width = target_img.shape[:-1]

        self.matching_img_y_cord = top_left[1] + int(self.target_img_height / 2)
        self.matching_img_x_cord = top_left[0] + int(self.target_img_width / 2)

        return result

    @staticmethod
    def get_template_matching_method(method):

        if method is None:
            return "TM_CCOEFF_NORMED", cv2.TM_CCOEFF_NORMED
        else:
            method = method.upper()

        if method == "TM_CCOEFF_NORMED":
            return "TM_CCOEFF_NORMED", cv2.TM_CCOEFF_NORMED
        elif method == "TM_CCOEFF":
            return method, cv2.TM_CCOEFF
        elif method == "TM_CCORR":
            return method,cv2.TM_CCORR
        elif method == "TM_CCORR_NORMED":
            return method, cv2.TM_CCORR_NORMED
        elif method == "TM_SQDIFF":
            return method, cv2.TM_SQDIFF
        elif method == "TM_SQDIFF_NORMED":
            return method, cv2.TM_SQDIFF_NORMED
        else:
            raise Exception(
                4 * "<" + "[ERROR]" + 4 * ">" +
                "\n" +
                "Template Matching Method does not exist or is not supported: " +
                "\n" +
                method +
                "\n")

    @staticmethod
    def get_image(image_path, flags=None) -> np.ndarray:
        result_img = cv2.imread(image_path)
        if result_img is None:
            raise Exception(
                4 * "<" + "[ERROR]" + 4 * ">" +
                "\n" +
                "Image is invalid or does not exist: " +
                image_path +
                "\n")

        return result_img

    def draw_rectangle_on_image(self, full_image: np.ndarray, target_img: np.ndarray):
        h, w = target_img.shape[:-1]
        self.img_occurrences = []

        for pt in zip(*self.occurrences[::-1]):
            x = pt[0] + int(w / 2)
            y = pt[1] + int(h / 2)

            self.img_occurrences.append((x, y))

            cv2.rectangle(img=full_image, pt1=pt, pt2=(pt[0] + w, pt[1] + h),
                          color=self.rectangle_color, thickness=self.rectangle_thickness)

            cv2.circle(img=full_image, center=(x, y), radius=1, color=(255, 0, 255), thickness=self.rectangle_thickness)

        cv2.imwrite(self.result_img_path, full_image)

    def is_image_found(self, result: np.ndarray, threshold=None) -> bool:
        if threshold is None:
            threshold = self.threshold

        self.occurrences = np.where(result >= threshold)

        return False if self.occurrences[0].shape[0] == 0 else True

    def compare_images(self):
        self.target_img = self.get_image(self.target_img_path)
        self.full_img = self.get_image(self.full_img_path)

        # Differences found
        self.standard_minus_current_difference = cv2.absdiff(self.target_img, self.full_img)

        # Creates the images comparison collage

        diff_compare = cv2.absdiff(self.target_img, self.full_img)

        standard = cv2.copyMakeBorder(self.target_img, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=[255, 0, 0])

        standard = self.apply_watermark(image=standard, watermark_img_path=self.STANDARD_WATERMARK_IMG_PATH)

        screenshot = cv2.copyMakeBorder(self.full_img, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=[255, 0, 0])

        screenshot = self.apply_watermark(image=screenshot, watermark_img_path=self.RESULT_WATERMARK_IMG_PATH)

        differences = cv2.copyMakeBorder(diff_compare, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=[255, 0, 0])

        differences = self.apply_watermark(image=differences, watermark_img_path=self.DIFFERENCES_WATERMARK_IMG_PATH)

        temp4 = np.hstack((standard, screenshot))

        diff_compare = np.hstack((temp4, differences))

        cv2.imwrite(filename=self.result_img_path, img=diff_compare)

        return self.standard_minus_current_difference

    def is_difference_found(self, standard_img_path=None, full_img_path=None):
        self.standard_minus_current_difference = self.compare_images()

        if self.standard_minus_current_difference is None:
            raise Exception(
                4 * "<" + "[ERROR]" + 4 * ">" +
                "\n" +
                "standard_minus_current_difference variable cannot be None"
                + "\n")

        b, g, r = cv2.split(self.standard_minus_current_difference)

        if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
            return False
        else:
            return True

    @staticmethod
    def apply_watermark(image, watermark_img_path, position=(10, 10)):
        # Coordinates where to put the watermark
        cx, cy = position

        # Reading the image
        (h, w) = image.shape[:2]
        image = np.dstack([image, np.ones((h, w), dtype="uint8") * 255])

        # Reading the watermark
        watermark_img = cv2.imread(watermark_img_path, cv2.IMREAD_UNCHANGED)
        (wH, wW) = watermark_img.shape[:2]
        (B, G, R, A) = cv2.split(watermark_img)
        B = cv2.bitwise_and(B, B, mask=A)
        G = cv2.bitwise_and(G, G, mask=A)
        R = cv2.bitwise_and(R, R, mask=A)
        watermark = cv2.merge([B, G, R, A])

        # Creating the image's overlay with the watermark
        overlay = np.zeros((h, w, 4), dtype="uint8")
        overlay[cy:wH + cy, cx:wW + cx] = watermark

        # Applying the overlay
        output = image.copy()
        return cv2.addWeighted(overlay, 0.4, output, 1.0, 0, output)

# ##### Metodo 3: Recorta la diferencia y con ese recorte crea otra imagen
#
# try:
#     copy2 = cv2.compare(standard, current, cv2.CMP_EQ)
#     cv2.imwrite('./screenshots/baseline/diff_compare.png', copy2)
# except Exception as e:
#     print(e)
