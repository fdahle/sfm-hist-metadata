"""Estimate the cam id"""

# Library imports
import copy
import pandas as pd
from typing import Optional, Union

# Constants
MIN_NR_OF_IMAGES = 3
MAX_STD = 0.005


def estimate_cam_id(image_id: str,
                    use_estimated: bool = False, return_data: bool = False,
                    cam_id_data: Optional[pd.DataFrame] = None,
                    ) -> Union[None, tuple[None, None], float,
                               tuple[str, Optional[pd.DataFrame]]]:
    """
    Estimates the cam id for a given image based on images with similar properties.
    Args:
        image_id (str): The ID of the image for which the cam id is to be estimated.
        use_estimated (bool): Flag to include estimated cam ids in the analysis.
        return_data (bool): Flag to return the original cam id data.
        cam_id_data (pd.DataFrame): DataFrame with columns 'image_id', 'cam_id', and
            'cam_id_estimated' for images with similar properties.
    Returns:
        float: A string containing the estimated cam id.
            This return type is provided when `return_data` is False.
        Tuple[float, pd.DataFrame]: A tuple containing the estimated cam id and the
            original subset data `pd.DataFrame` if `return_data` is True.
        None: Returns None if conditions like minimum number of images or maximum standard
            deviation are not met.
    """

    if cam_id_data is None:
        raise ValueError(
            "cam_id_data must be provided as a DataFrame with columns "
            "'image_id', 'cam_id', and 'cam_id_estimated'."
        )

    # create a copy for the return
    orig_cam_id_data = copy.deepcopy(cam_id_data)

    # remove the image_id from the image we want to extract information from
    cam_id_data = cam_id_data[cam_id_data['image_id'] != image_id]

    # remove estimated if we don't want to use them
    if use_estimated is False:
        cam_id_data = cam_id_data.loc[cam_id_data['cam_id_estimated'] == False]  # noqa

    # check if we still have data
    if cam_id_data.shape[0] == 0:
        return None

    # count the number of non Nan values
    cam_id_count = cam_id_data.loc[pd.notnull(cam_id_data[f'cam_id'])].shape[0]

    # check if there is a minimum number of images
    if MIN_NR_OF_IMAGES is not None:

        # check if the number of images is below the minimum
        if cam_id_count < MIN_NR_OF_IMAGES:
            return None

    # get most common cam id
    cam_id = cam_id_data['cam_id'].mode().iloc[0]

    return cam_id if not return_data else (cam_id, orig_cam_id_data)
