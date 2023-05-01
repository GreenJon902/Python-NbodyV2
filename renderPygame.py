import pygame
import nbody
import glob
import cv2 as cv
import os
# os.environ["SDL_VIDEODRIVER"] = "dummy"
from tqdm import tqdm


def pygame_setup():
    global win, center_x, center_y
    pygame.init()

    WIDTH = 1920
    HEIGHT = 1080

    win = pygame.display.set_mode((WIDTH, HEIGHT))

    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h

    center_x = screen_width // 2
    center_y = screen_height // 2
    # print(center_x, center_y)


def render(poses, dist):
    with tqdm(total=len(poses)) as pb:
        for bodies in range(poses.shape[0]):
            win.fill((0, 0, 0))
            x = poses[bodies, :, 0]
            y = poses[bodies, :, 1]
            z = poses[bodies, :, 2]
            radius = poses[bodies, :, 3]
            for n in range(len(x)):
                x1 = int(x[n])
                y1 = int(y[n])
                z1 = int(z[n])
                radius1 = int(radius[n]) * nbody.Nbody.SCALE
                # print(x1, y1, z1, radius1)

                if z1 == 0:
                    z1 = z1 + 1

                rendered_x = int(x1 + (x1 / z1))
                rendered_y = int(y1 + (y1 / z1))
                dynamic_radius = 1  # int(radius1 / z1)
                if dynamic_radius == 0:
                    dynamic_radius = 1
                #print(f"Render X: {rendered_x}, Rendered Y: {rendered_y}, Rendered Radius: {dynamic_radius}")
                try:
                    pygame.draw.circle(win, (255, 255, 255), (int(center_x - rendered_x), int(center_y - rendered_y)),
                                       dynamic_radius, 0)
                    #print("On Screen")
                except TypeError:
                    #print("Not On screen")
                    pass

            pygame.image.save(win, f'run/image0{bodies}.jpg')
            pb.update(1)
            pygame.display.flip()


def img2vid(FPS, vid_id, cycles):
    filenames = sorted(glob.glob("run/*.jpg"), key=os.path.getmtime)

    images = [cv.imread(img) for img in filenames]
    img_amount = len(images)

    video_name = f"{vid_id}_{cycles}_{nbody.Nbody.TIMESTEP}.mp4"
    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    video = cv.VideoWriter(video_name, fourcc, FPS, (960, 720))

    print("Creating Video From Frames")
    with tqdm(total=img_amount) as pb:
        for img in images:
            video.write(img)
            pb.update(1)
    cv.destroyAllWindows()
    video.release()
