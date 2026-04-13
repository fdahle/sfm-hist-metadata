"""Estimate the height"""

# Library imports
import copy
import pandas as pd
from typing import Optional, Union

# Constants
MIN_NR_OF_IMAGES = 3
MAX_STD = None


def estimate_height(image_id: str,
                    use_estimated: bool = False, return_data: bool = False,
                    height_data: Optional[pd.DataFrame] = None,
                    ) -> Union[None, tuple[None, None], float,
                               tuple[float, Optional[pd.DataFrame]]]:
    """
    Estimates the height for a given image based on images with similar properties.
    Args:
        image_id (str): The ID of the image for which the height is to be estimated.
        use_estimated (bool): Flag to include estimated heights in the analysis.
        return_data (bool): Flag to return the original height data.
        height_data (pd.DataFrame): DataFrame with columns 'image_id', 'height', and
            'height_estimated' for images with similar properties.
    Returns:
        float: A float values containing the estimated height.
            This return type is provided when `return_data` is False.
        Tuple[float, pd.DataFrame]: A tuple containing the estimated height and the
            original subset data `pd.DataFrame` if `return_data` is True.
        None: Returns None if conditions like minimum number of images or maximum standard deviation are not met.
    """

    if height_data is None:
        raise ValueError(
            "height_data must be provided as a DataFrame with columns "
            "'image_id', 'height', and 'height_estimated'."
        )

    # create a copy for the return
    orig_height_data = copy.deepcopy(height_data)

    # remove the image_id from the image we want to extract information from
    height_data = height_data[height_data['image_id'] != image_id]

    # remove estimated if we don't want to use them
    if use_estimated is False:
        height_data = height_data.loc[height_data['height_estimated'] == False]  # noqa

    # check if we still have data
    if height_data.shape[0] == 0:
        return None

    # count the number of non Nan values
    height_count = height_data.loc[pd.notnull(height_data[f'height'])].shape[0]

    # check if there is a minimum number of images
    if MIN_NR_OF_IMAGES is not None:

        # check if the number of images is below the minimum
        if height_count < MIN_NR_OF_IMAGES:
            return None

    # get the std value of height
    std = height_data['height'].std()

    # check if there is a maximum standard deviation
    if MAX_STD is not None:

        # check if the standard deviation is above the maximum
        if std > MAX_STD:
            return None

    # get the median value
    median_val = height_data['height'].median()

    # round the mean value
    height = int(median_val)

    return (height, orig_height_data) if return_data else height
