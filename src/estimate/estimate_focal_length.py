"""Estimates the focal length for a given image"""

# Library imports
import copy
import pandas as pd
from typing import Optional, Union

# Constants
MIN_NR_OF_IMAGES = 3
MAX_STD = 0.005


def estimate_focal_length(image_id: str,
                          use_estimated: bool = False, return_data: bool = False,
                          focal_length_data: Optional[pd.DataFrame] = None,
                          ) -> Union[None, tuple[None, None], float,
                                     tuple[float, Optional[pd.DataFrame]]]:
    """
    Estimates the focal length for a given image based on images with similar properties.
    Args:
        image_id (str): The ID of the image for which the focal length is to be estimated.
        use_estimated (bool): Flag to include estimated focal lengths in the analysis.
        return_data (bool): Flag to return the original focal length data.
        focal_length_data (pd.DataFrame): DataFrame with columns 'image_id', 'focal_length',
            and 'focal_length_estimated' for images with similar properties.
    Returns:
        float: A float values containing the estimated focal length.
            This return type is provided when `return_data` is False.
        Tuple[float, pd.DataFrame]: A tuple containing the estimated focal length and the
            original subset data `pd.DataFrame` if `return_data` is True.
        None: Returns None if conditions like minimum number of images or maximum standard deviation are not met.
    """

    if focal_length_data is None:
        raise ValueError(
            "focal_length_data must be provided as a DataFrame with columns "
            "'image_id', 'focal_length', and 'focal_length_estimated'."
        )

    # create a copy for the return
    orig_focal_length_data = copy.deepcopy(focal_length_data)

    # remove the image_id from the image we want to extract information from
    focal_length_data = focal_length_data[focal_length_data['image_id'] != image_id]

    # remove estimated if we don't want to use them
    if use_estimated is False:
        focal_length_data = focal_length_data.loc[focal_length_data['focal_length_estimated'] == False]  # noqa

    # check if we still have data
    if focal_length_data.shape[0] == 0:
        return None

    # count the number of non Nan values
    focal_length_count = focal_length_data.loc[pd.notnull(focal_length_data[f'focal_length'])].shape[0]

    # check if there is a minimum number of images
    if MIN_NR_OF_IMAGES is not None:

        # check if the number of images is below the minimum
        if focal_length_count < MIN_NR_OF_IMAGES:
            return None

    # get the std value of focal length
    std = focal_length_data['focal_length'].std()

    # check if the standard deviation is below the maximum
    if MAX_STD is not None:

        # check if the standard deviation is below the maximum
        if std > MAX_STD:
            return None

    # get the median value
    median_focal_length = focal_length_data['focal_length'].median()

    # round the focal length
    focal_length = round(median_focal_length, 3)

    return (focal_length, orig_focal_length_data) if return_data else focal_length
