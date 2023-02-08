import glob
import os
from pathlib import Path

import numpy as np
from plyfile import PlyData




class MyDataset:
    def __init__(self, data_dir: Path, *_, **__):
        # Config stuff
        self.sequence_id = os.path.basename(data_dir)
        self.sequence_dir = os.path.realpath(data_dir)
        self.velodyne_dir = os.path.realpath(data_dir)
        #self.velodyne_dir = os.path.join(self.sequence_dir, "frames/")
        self.scan_files = sorted(glob.glob(self.velodyne_dir + "/*.bin"))
        self.gt_poses = self.load_gt_poses(os.path.join(self.sequence_dir, "gt_traj_lidar.txt"))

        print(self.velodyne_dir, len(self.scan_files))

    def __len__(self):
        return len(self.scan_files)

    def __getitem__(self, idx):
        return self.read_point_cloud(self.scan_files[idx])

    def read_point_cloud(self, file_path: str):

        timestamps = int(os.path.basename(file_path).split(".")[0])
        points = np.fromfile(file_path, dtype=np.float32)
        points = points.reshape((-1, 3))#.transpose()

        # print(file_path, points.shape)
        # print(points[0:10, :])
        # plydata = PlyData.read(file_path)
        # x = np.asarray(plydata.elements[0].data["x"]).reshape(-1, 1)
        # y = np.asarray(plydata.elements[0].data["y"]).reshape(-1, 1)
        # z = np.asarray(plydata.elements[0].data["z"]).reshape(-1, 1)
        # points = np.concatenate([x, y, z], axis=1)
        # timestamps = np.asarray(plydata.elements[0].data["timestamp"])
        # timestamps = timestamps / np.max(timestamps)
        return points, timestamps


    def load_gt_poses(self, file_path):
        gt_poses = []
        for xyz in np.loadtxt(file_path):
            #T = np.eye(4)
            #T[:3, 3] = xyz
            T = xyz.reshape(4, 4)
            gt_poses.append(T)
        return gt_poses

    def apply_calibration(self, poses):
        """ParisLucoDataset only has a x, y, z trajectory, so we must will em all"""
        new_poses = []
        for pose in poses:
            T = pose.copy()
            T[:3, :3] = np.eye(3)
            new_poses.append(T)
        return new_poses
