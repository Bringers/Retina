import numpy as np
import random

def data_generator(num, pixels=256, objects=1, object_width=20, width=6, rand_width=6, speed_range=(1, 30),
                   label_delay=0, state_change=0.05, left=0.3, right=0.3, noise=0.00, loop_around=False):
    # Input
    # num           Number of images
    # pixels        Image resolution
    # objects       Number of moving objects
    # object_width  Length between object contours
    # width         Width of contours
    # rand_width    Random change in width (+|-)
    # speed_range   Random range of the speed for the object
    # label_delay   Adds a delay to answers to prevent labelling of jitter
    # state_change  Likelihood of changing movement
    # left          Likelihood of moving left
    # right         Likelihood of moving right (not moving = 1 - (left+right))
    # noise         Likelihood of a pixel being turned white
    # loop_around   Object appears on the other side when out of frame
    #
    # Output
    # data          Array of 1D images (pixelsx1). Use imshow(data) to view
    # labels        -1 means left movement, 0 no movement and 1 right movement

    data = np.zeros((num, pixels, 3))
    labels = {}
    labels["left"] = np.zeros(num)
    labels["right"] = np.zeros(num)

    for l in range(objects):
        # Init
        label_count = label_delay
        r = np.random.rand()
        if r < left:
            state = -1
        elif r < left + right:
            state = 1
        else:
            state = 0
        last_pos = random.randrange(0, pixels - 1)

        # Go through each time step
        for i in range(num):
            speed = random.randrange(speed_range[0], speed_range[1])

            # Randomly change state
            if state_change > np.random.rand():
                label_count = label_delay
                r = np.random.rand()
                if r < left:
                    state = -1
                elif r < left + right:
                    state = 1
                else:
                    state = 0

            label_count -= 1

            # Move object
            pos = last_pos + speed * state
            if loop_around:
                if pos > pixels - 1:
                    pos = 0
                elif last_pos < 0:
                    pos = pixels - 1
            else:
                if pos > pixels - 1:
                    state = -1
                    pos = last_pos + speed * state
                elif last_pos < 0:
                    state = 1
                    pos = last_pos + speed * state

            # Paint contours
            if state != 0:
                # Left contour
                width_now = width + round(rand_width * np.random.rand() * 2 - rand_width / 2)
                pos_offset = pos - int(object_width / 2)
                for j in range(width_now + 1):
                    if j % 2 == 0:
                        index = pos_offset - int(j / 2)
                    else:
                        index = pos_offset + int(j / 2 + 1)
                    if index >= 0 and index < pixels:
                        data[i][index].fill(1)

                # Right contour
                width_now = width + round(rand_width * np.random.rand() * 2 - rand_width / 2)
                pos_offset = pos + int(object_width / 2)
                for j in range(width_now + 1):
                    if j % 2 == 0:
                        index = pos_offset - int(j / 2)
                    else:
                        index = pos_offset + int(j / 2 + 1)
                    if index >= 0 and index < pixels:
                        data[i][index].fill(1)

            # Write labels
            last_pos = pos
            if label_count < 0:
                if state == -1:
                    labels["left"][i] += 1
                elif state == 1:
                    labels["right"][i] += 1

    if noise > 0:
        data = random_noise(data, noise)

    labels = labels["right"] - labels["left"]
    return data, labels


def random_noise(data, noise):
    for img in data:
        for i in range(int(2 * np.random.rand() * noise * len(img))):
            index = random.randrange(0, len(img))
            img[index].fill(1)

    return data