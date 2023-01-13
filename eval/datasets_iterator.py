
import os

import kiss_icp
import matplotlib.pyplot as plt
import numpy as np
from evo.tools import plot
from kiss_icp.config import load_config
from kiss_icp.datasets import dataset_factory
from kiss_icp.pipeline import OdometryPipeline
from rich import print

from kiss_icp_eval import get_sequence

dataset_name_to_subdir_map = {
    "paris_luco": "ParisLuco",
    "kitti": "kitti-odometry/dataset",
    "mulran": "MulRan",
    "newer_college": ""
 
}
def get_dataset_subdir(dataset_name, sequence):
    sub_dir = dataset_name_to_subdir_map[dataset_name]
    if dataset_name == "paris_luco":
        sub_dir = os.path.join(sub_dir, f"{sequence:02d}")
    return sub_dir


def dataset_itr(root_path, dataset_name, sequence):    
    dataset_root = os.path.join(root_path, get_dataset_subdir(dataset_name, sequence))
    cfg_file = os.path.join(os.path.dirname(kiss_icp.__file__), "config/default.yaml")
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
        yield raw_frame_timestamp[0], raw_frame_timestamp[1], gt_pose


# data_root = "/run/user/1000/gvfs/smb-share:server=10.84.164.159,share=datasets" #os.environ.get("DATASETS")
# paris_luco_root = os.path.join(data_root, "ParisLuco/00")
# cfg_file = os.path.join(os.path.dirname(kiss_icp.__file__), "config/default.yaml")

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