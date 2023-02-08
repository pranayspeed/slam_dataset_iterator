
import os

import slam_dataset_sdk
import matplotlib.pyplot as plt
import numpy as np
#from evo.tools import plot
#from slam_dataset_sdk.config import load_config
from slam_dataset_sdk.datasets import dataset_factory
from slam_dataset_sdk.pipeline import OdometryPipeline
from rich import print

#from kiss_icp_eval import get_sequence
from dataclasses import dataclass
from typing import Callable, Dict
#from typing import List


from slam_dataset_sdk.tools.progress_bar import get_progress_bar

def get_sequence(kiss_pipeline: Callable, results: Dict, **kwargs):
    # Create pipeline object
    pipeline: OdometryPipeline = kiss_pipeline(kwargs.pop("sequence"))

    # New entry to the results dictionary
    results.setdefault("dataset_name", pipeline.dataset_name)

    # Run pipeline
    print(f"Now evaluating sequence {pipeline.dataset_sequence}")
    #first_idx = pipeline.get_first_idx()
    #last_idx = pipeline.get_last_idx()
    #for idx in get_progress_bar(pipeline._first, pipeline._last):
    #    yield pipeline._next(idx) , pipeline.gt_poses[idx]
    for idx in range(pipeline._first, pipeline._last):
        yield pipeline._next(idx) , pipeline.gt_poses[idx]


dataset_name_to_subdir_map = {
    "oxford": "velodyne_left",
    "mydataset":"",
    "paris_luco": "ParisLuco",
    "kitti": "kitti-odometry/dataset",
    "mulran": "MulRan",
    "newer_college": "",
    "rosbag": "",
    "rosbag2": "",
    
}
def get_dataset_subdir(dataset_name, sequence):
    sub_dir = dataset_name_to_subdir_map[dataset_name]
    if dataset_name == "paris_luco":
        sub_dir = os.path.join(sub_dir, f"{sequence:02d}")
    return sub_dir


def dataset_itr(root_path, dataset_name, sequence):    
    dataset_root = os.path.join(root_path, get_dataset_subdir(dataset_name, sequence))
    cfg_file = os.path.join(os.path.dirname(slam_dataset_sdk.__file__), "config/default.yaml")
    def dataset_sequence_pipeline(sequence: int):
        return OdometryPipeline(
            dataset = dataset_factory(
                dataloader=dataset_name,
                data_dir=dataset_root,
                config=cfg_file,
                sequence=sequence,
            ),
            config=cfg_file,
        )

    results = {}
    for raw_frame_timestamp, gt_pose in get_sequence(dataset_sequence_pipeline, sequence=sequence, results=results):
        data = {
            "raw_frame": raw_frame_timestamp[0],
            "timestamp": raw_frame_timestamp[1],
            "gt_pose": gt_pose
        }
        yield data


def get_supported_datasets():
    return dataset_name_to_subdir_map.keys()

# data_root = "/run/user/1000/gvfs/smb-share:server=10.84.164.159,share=datasets" #os.environ.get("DATASETS")
# paris_luco_root = os.path.join(data_root, "ParisLuco/00")
# cfg_file = os.path.join(os.path.dirname(slam_dataset_sdk.__file__), "config/default.yaml")

# print(f"Reading datasets from : {data_root}")
# print(f"Configuration:")
# print(load_config(cfg_file))


# from kiss_icp_eval import run_sequence, get_sequence


# def paris_luco_sequence(sequence: int):
#     return OdometryPipeline(
#         dataset=dataset_factory(
#             dataloader="paris_luco",
#             data_dir=paris_luco_root,
#             config=cfg_file,
#             sequence=sequence,
#         ),
#         config=cfg_file,
#     )


# results = {}
# for sequence in range(0, 1):
#     for raw_frame, timestamp in get_sequence(paris_luco_sequence, sequence=sequence, results=results):
#         print(raw_frame.shape)