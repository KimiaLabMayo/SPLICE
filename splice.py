import cv2
import numpy as np
from PIL import Image


def splice(patches_np: np.ndarray, patches_xy: np.ndarray, thresh: int = 30):
    """
    Implementation of the method SPLICE

    Argements:
        patches_np: np.ndarray: The patches that have been read and converted to numpy
        patches_xy: np.ndarray: The coordinates of the patches
        thresh: int: The percentile for including or excluding patches (default 30)
    Returns:
        np.array(collage): The collage of the patches
    """
    # Resize, as smaller patches are better for color histogram comparison
    patches_color_size = []
    for patch in patches_np:
        patch_PIL = Image.fromarray(patch)
        patches_color_size.append(np.array(patch_PIL.resize((int(32), int(32)))))
    patches_color_size = np.array(patches_color_size)

    histograms = []
    for patch in patches_color_size:
        # Split the image into color channels
        red_channel, green_channel, blue_channel = cv2.split(patch)
        # Calculate the mean for each channel
        mean_red = np.mean(red_channel)
        mean_green = np.mean(green_channel)
        mean_blue = np.mean(blue_channel)
        # Calculate the standard deviation for each channel
        std_dev_red = np.std(red_channel)
        std_dev_green = np.std(green_channel)
        std_dev_blue = np.std(blue_channel)
        # Combine the computed features into a single feature vector
        histograms.append(
            [mean_red, mean_green, mean_blue, std_dev_red, std_dev_green, std_dev_blue]
        )
    histograms = np.array(histograms)

    # Here we store the calculated distances between patches. In every round, this list will be reset
    euc_dist = []
    # pointer is the index of the base patch
    pointer = 0
    # We start by storing the index of the base so that we initiate the comparison.
    # We will keep adding to this list until we get the final list
    included_patches = [pointer]
    # Here we store the indices of the excluded patches.
    # We will keep adding to this list until we get the final list.
    excluded_patches = []
    # here we store the index of the patches that we measure
    # the distance between them and the base patch (pointer)
    measured_patch_idx = []

    # Start including and excluding patches based on the sequential approach
    for index_1 in range(len(histograms)):
        euc_dist = []
        measured_patch_idx = []

        # we always start from the pointer so that
        # we can avoid the excluded patches in the previous rounds
        if index_1 == pointer:
            for index_2 in range(len(histograms)):
                # compare only with the remaining patches
                # that are not yet included (previous bases) or exluded
                if (index_2 not in excluded_patches) and (
                    index_2 not in included_patches
                ):
                    # calculate the euclidean distance between
                    # the base and the remaining patches (not included or exluded yet)
                    euc_dist.append(
                        np.linalg.norm(histograms[pointer] - histograms[index_2])
                    )
                    # keep tracking of the patch indices that we compared with
                    measured_patch_idx.append(index_2)

            # we need at least two remaining patches to find the median or percentile
            if len(euc_dist) > 1:
                # find the percentile
                perc_thresh = np.percentile(euc_dist, thresh)
                # exclude all the patches that are similar to the base patch
                excluded_idx = [
                    i for i in range(len(euc_dist)) if euc_dist[i] < perc_thresh
                ]
                # as excluded_idx has the indices of the current itiration,
                # we get the real index of the excluded patches from the measured_patch_idx
                for i in excluded_idx:
                    excluded_patches.append(measured_patch_idx[i])

                # here we find the patches that are dissimilar,
                # just to get the index of the next base (pointer)
                included_idx = [
                    i for i in range(len(euc_dist)) if euc_dist[i] > perc_thresh
                ]

                # > 0 because in rare cases, included_idx will have 0 patches
                # if the distance between the base and all remaining patches is the same.
                if len(included_idx) > 0:
                    # the pointer for the next itiration
                    # if the first patch is dissimilar to the current pointer
                    first_included = included_idx[0]
                    pointer = measured_patch_idx[first_included]
                    # the next base will be included so we add it to the final included_patches
                    included_patches.append(pointer)
                    # if the pointer of the next iteration is the last remaining patch
                    if len(included_idx) == 1:
                        break
                else:
                    break
            # include the last remaining patch that was not excluded before
            else:
                if measured_patch_idx:
                    pointer = measured_patch_idx[0]
                    included_patches.append(pointer)
                    break

    collage = []
    # get the coordinates of the collage using indices stored in included_patches
    for i in included_patches:
        collage.append(patches_xy[i])

    return np.array(collage)
