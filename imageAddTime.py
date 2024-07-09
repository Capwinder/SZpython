import cv2
import os
import datetime


def image_func(init_path, target_path):
    if not os.path.exists(target_path):
        os.makedirs(target_path, exist_ok=True)

    if not os.listdir(init_path):
        print('您提供的文件夹为空')
    else:
        for imageName in os.listdir(init_path):
            if imageName.lower().endswith(('.jpg', '.png', '.jpeg', '.bmp', '.gif')):
                full_path = os.path.join(init_path, imageName)
                image = cv2.imread(full_path)

                if image is not None:
                    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(now_time)
                    height, width = image.shape[:2]
                    x = width - 460
                    y = height - 65

                    font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
                    font_scale = 1
                    color = (255, 255, 255)
                    thickness = 2

                    cv2.putText(image, now_time, (x, y), font, font_scale, color, thickness, cv2.LINE_AA)

                    edited_image_name = imageName.split('.')[0] + ' edited.' + imageName.split('.')[1]
                    full_output_path = os.path.join(output_folder, edited_image_name)

                    cv2.imwrite(full_output_path, image)
                    print(f'图像处理完毕：{full_output_path}')

                else:
                    print(f'图像读取失败：{full_path}')

        print('结束')


if __name__ == "__main__":
    image_folder = "C:/Users/Capwinder/Pictures/opencvImage/"
    output_folder = 'C:/Users/Capwinder/Pictures/outputfolder/'
    image_func(image_folder, output_folder)
