import cv2

GRAY_IMG = 1
COLOR_IMG = 2


def cut_dark(img, is_show=False):
    """
    去出图片的黑边
    :param img:
    :return:
    """

    # 灰度图
    if len(img.shape) == 2:
        print('灰度图')
        img_type = GRAY_IMG
        new_point = 255
    elif len(img.shape) == 3:
        print('彩色图')
        img_type = COLOR_IMG
        new_point = (255, 255, 255)
    else:
        print('非法图片格式，退出！')
        return

    (h, w) = img.shape[:2]
    img[:int(h / 30), :] = new_point
    img[:, :int(w / 30)] = new_point
    img[int(h / 30 * 29):, :] = new_point
    img[:, int(w / 30 * 29):] = new_point

    if is_show:
        cv2.imshow('img', img)
        cv2.waitKey(10000)
        cv2.destroyAllWindows()


def scan(file, threshold=80):
    """
    扫描图片成文档
    :param file: 图片文件
    :param threshold: 阈值
    :return:
    """

    img = cv2.imread(file)

    # result_b = img[:, :, 0] > threshold
    # result_g = img[:, :, 1] > threshold
    result_r = img[:, :, 2] > threshold
    # result = result_b & result_g & result_r
    new_img = result_r * 255

    cut_dark(new_img)

    cv2.imwrite(file, new_img)
