import glob
import os
from pathlib import Path

import numpy as np
from plyfile import PlyData
import re

from slam_dataset_sdk.tools.oxford_sdk.interpolate_poses import interpolate_vo_poses, interpolate_ins_poses
from slam_dataset_sdk.tools.oxford_sdk.transform import build_se3_transform
from slam_dataset_sdk.tools.oxford_sdk.velodyne import load_velodyne_raw, load_velodyne_binary, velodyne_raw_to_pointcloud

class OxfordRobotCarDataset:
    def __init__(self, data_dir: Path, *_, **__):
        # Config stuff
        self.sequence_id = os.path.basename(data_dir)
        self.sequence_dir = os.path.realpath(data_dir)
        self.velodyne_dir = os.path.realpath(data_dir)
        #self.velodyne_dir = os.path.join(self.sequence_dir, "frames/")
        self.scan_files = sorted(glob.glob(self.velodyne_dir + "/*.bin"))
        #self.gt_poses = self.load_gt_poses(os.path.join(self.sequence_dir, "gt_traj_lidar.txt"))

        print(self.velodyne_dir, len(self.scan_files))

        self.lidar = re.search('(lms_front|lms_rear|ldmrs|velodyne_left|velodyne_right)', self.velodyne_dir).group(0)
        timestamps_path = os.path.join( self.velodyne_dir, os.pardir, self.lidar  + '.timestamps')

        self.timestamps = []
        with open(timestamps_path) as timestamps_file:
            for line in timestamps_file:
                timestamp = int(line.split(' ')[0])
                #if start_time <= timestamp <= end_time:
                self.timestamps.append(timestamp)
        if len(self.timestamps) == 0:
            raise ValueError("No LIDAR data in the given time bracket.")
        

        curr_file_path = os.path.dirname(os.path.realpath(__file__))

        #self.extrinsics_dir = os.path.join( curr_file_path, os.pardir, 'tools','oxford_sdk','extrinsics')
        
        self.extrinsics_dir = os.path.join(self.velodyne_dir, os.pardir, 'extrinsics')
        #print(self.extrinsics_dir)

        with open(os.path.join(self.extrinsics_dir, self.lidar  + '.txt')) as extrinsics_file:
            extrinsics = next(extrinsics_file)
        self.G_posesource_laser = build_se3_transform([float(x) for x in extrinsics.split(' ')])

        poses_file = os.path.join(self.velodyne_dir, os.pardir, 'vo/vo.csv')


        poses_type = re.search('(vo|ins|rtk)\.csv', poses_file).group(1)
        origin_time = self.timestamps[0]

        if poses_type in ['ins', 'rtk']:
            with open(os.path.join(self.extrinsics_dir, 'ins.txt')) as extrinsics_file:
                extrinsics = next(extrinsics_file)
                self.G_posesource_laser = np.linalg.solve(build_se3_transform([float(x) for x in extrinsics.split(' ')]),
                                                    self.G_posesource_laser)

            gt_poses = interpolate_ins_poses(poses_file, self.timestamps, origin_time, use_rtk=(poses_type == 'rtk'))
        else:
            # sensor is VO, which is located at the main vehicle frame
            gt_poses = interpolate_vo_poses(poses_file, self.timestamps, origin_time)

        #self.gt_poses = [np.eye(4)]
        self.gt_poses = []
        print(len(gt_poses))
        for i in range(0, len(gt_poses)):
            self.gt_poses.append(np.dot(gt_poses[i], self.G_posesource_laser))


        #pointcloud = np.array([[0], [0], [0], [0]])
        if self.lidar  == 'ldmrs':
            self.reflectance = None
        else:
            self.reflectance = np.empty((0))
        

        

    def __len__(self):
        return len(self.timestamps)

    def __getitem__(self, idx):
        return self.read_point_cloud(idx)

    def read_point_cloud(self, idx: int):
    
        timestamp = self.timestamps[idx]

        scan_path = os.path.join(self.velodyne_dir, str(timestamp) + '.bin')
        if "velodyne" not in self.lidar:
            if not os.path.isfile(scan_path):
                print("No scan file found for timestamp: {}".format(timestamp))
                return None, timestamp

            scan_file = open(scan_path)
            scan = np.fromfile(scan_file, np.double)
            scan_file.close()

            scan = scan.reshape((len(scan) // 3, 3)).transpose()

            if self.lidar != 'ldmrs':
                # LMS scans are tuples of (x, y, reflectance)
                self.reflectance = np.concatenate((self.reflectance, np.ravel(scan[2, :])))
                scan[2, :] = np.zeros((1, scan.shape[1]))
        else:
            if os.path.isfile(scan_path):
                ptcld = load_velodyne_binary(scan_path)
            else:
                scan_path = os.path.join(self.velodyne_dir, str(timestamp) + '.png')
                if not os.path.isfile(scan_path):
                    print("No scan file found for timestamp: {}".format(timestamp))
                    return None, timestamp
                ranges, intensities, angles, approximate_timestamps = load_velodyne_raw(scan_path)
                ptcld = velodyne_raw_to_pointcloud(ranges, intensities, angles)

            self.reflectance = np.concatenate((self.reflectance, ptcld[3]))
            scan = ptcld[:3]

        points = scan.transpose()
        #points = points[[1, 0, 2]].transpose()
        return points, timestamp


