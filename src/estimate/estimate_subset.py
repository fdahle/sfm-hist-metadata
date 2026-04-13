"""Estimates the subset values for a given image"""

# Library imports
import copy
import pandas as pd
from typing import Optional, Union

# Constants
MIN_NR_OF_IMAGES = 3
MAX_STD = None


def estimate_subset(image_id: str,
                    key: str,
                    use_estimated: bool = False,
                    return_data: bool = False,
                    subset_data: Optional[pd.DataFrame] = None,
                    ) -> Union[None, tuple[None, None], tuple[int, int],
                               tuple[tuple[int, int], Optional[pd.DataFrame]]]:
    """
    Estimates the subset values for a given image based on images with similar properties.
    Args:
        image_id (str): The ID of the image for which the subset is to be estimated.
        key (str): Key specifying the subset direction ('n', 'e', 's', 'w').
        use_estimated (bool): Flag to include estimated subsets in the analysis.
        return_data (bool): Flag to return the original subset data along with the estimated coordinates.
        subset_data (pd.DataFrame): DataFrame with columns 'image_id', subset_N_x/y/estimated columns
            for images with similar properties.
    Returns:
        Tuple[int, int]: A tuple containing the estimated x and y coordinates (x_val, y_val).
            This return type is provided when `return_data` is False.
        Tuple[Tuple[int, int], pd.DataFrame]: A tuple containing the estimated coordinates as a tuple of
            integers (x_val, y_val), and the original subset data `pd.DataFrame` if `return_data` is True.
        None: Returns None if conditions like minimum number of images or maximum standard deviation are not met.
    """

    if subset_data is None:
        raise ValueError(
            "subset_data must be provided as a DataFrame with columns "
            "'image_id', subset_N_x, subset_N_y, subset_N_estimated (for N in n/e/s/w)."
        )

    # create a copy for the return
    orig_subset_data = copy.deepcopy(subset_data)

    # remove the image_id from the image we want to extract information from
    subset_data = subset_data[subset_data['image_id'] != image_id]

    # remove estimated if we don't want to use them
    if use_estimated is False:
        subset_data = subset_data.loc[subset_data[f'subset_{key}_estimated'] == False]  # noqa

    # check if we still have data
    if subset_data.shape[0] == 0:
        return None

    # count the number of non Nan values (x and y should be similar)
    x_count = subset_data.loc[pd.notnull(subset_data[f'subset_{key}_x'])].shape[0]
    y_count = subset_data.loc[pd.notnull(subset_data[f'subset_{key}_y'])].shape[0]

    # check if the counts are similar (should usually always be the case)
    if x_count != y_count:
        return (None, None) if return_data else None

    # check if there is a minimum number of images
    if MIN_NR_OF_IMAGES is not None:

        # check if the number of images is below the minimum
        if x_count < MIN_NR_OF_IMAGES or y_count < MIN_NR_OF_IMAGES:
            return (None, None) if return_data else None

    # get the std values
    x_std = subset_data[f'subset_{key}_x'].std()
    y_std = subset_data[f'subset_{key}_y'].std()

    # check if there is a maximum standard deviation
    if MAX_STD is not None:

        # check if the standard deviation is above the maximum
        if x_std > MAX_STD or y_std > MAX_STD:
            return (None, None) if return_data else None

    # get the mean values
    x_val = subset_data[f'subset_{key}_x'].mean()
    y_val = subset_data[f'subset_{key}_y'].mean()

    # convert to integer
    x_val = int(x_val)
    y_val = int(y_val)

    # save coords as tuple
    coords = (x_val, y_val)

    return (coords, orig_subset_data) if return_data else coords
