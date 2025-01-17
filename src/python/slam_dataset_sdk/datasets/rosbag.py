# MIT License
#
# Copyright (c) 2022 Ignacio Vizzo, Tiziano Guadagnino, Benedikt Mersch, Cyrill
# Stachniss.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import importlib
import os
from pathlib import Path
import sys

import numpy as np
import yaml

class RosbagDataset:
    def __init__(self, data_dir: Path, *_, **kwargs):
        try:
            import rosbag
        except ModuleNotFoundError:
            print('python rosbag is not installed, run "sudo apt install python3-rosbag"')
            sys.exit(1)

        self.pc2 = importlib.import_module("sensor_msgs.point_cloud2")
        self.sequence_id = os.path.basename(data_dir).split(".")[0]

        # bagfile
        if data_dir[-1]=='/':
            data_dir = data_dir[:-1]
        self.bagfile = data_dir
        print(f"Opening {self.bagfile}")
        self.bag = rosbag.Bag(data_dir, mode="r")
        #topic = "sensor_msgs/PointCloud2"
        #topic = "/ouster/points"
        topic = kwargs.get("topic", "")
        self.topic = topic
        self.check_for_topics()

        # Get an iterable
        self.n_scans = self.bag.get_message_count(topic_filters=topic)
        self.msgs = self.bag.read_messages(topics=[topic])

        self.gt_poses = np.zeros((self.n_scans, 4, 4))
        print(self.n_scans, "scans in the bagfile")
        
        # Visualization Options
        self.use_global_visualizer = True

    def __del__(self):
        self.bag.close()

    def __len__(self):
        return self.n_scans

    def __getitem__(self, idx):
        return self.read_point_cloud(self.bagfile, self.topic, idx)

    def read_point_cloud(self, bagfile: Path, topic: str, idx: int):
        # TODO: implemnt [idx], expose field_names
        _, msg, _ = next(self.msgs)
        print("read msg", msg.header.stamp)
        points = np.array(list(self.pc2.read_points(msg, field_names=["x", "y", "z"])))

        t_field = None
        for field in msg.fields:
            if field.name == "t" or field.name == "timestamp":
                t_field = field.name
        timestamps = np.ones(points.shape[0])
        if t_field:
            timestamps = np.array(list(self.pc2.read_points(msg, field_names=t_field)))
            timestamps = timestamps / np.max(timestamps)
        return points.astype(np.float64)#, timestamps

    def check_for_topics(self):
        print("Checking for topics...")
        if self.topic:
            return
        print("No topic provided")
        print("Please provide one of the following topics with the --topic flag")
        info_dict = yaml.safe_load(self.bag._get_yaml_info())
        info_dict.keys()
        print("PointCloud2 topics available:")
        for topic in info_dict["topics"]:
            if topic["type"] == "sensor_msgs/PointCloud2":
                for k, v in topic.items():
                    print(k.ljust(20), v)
        exit(1)
