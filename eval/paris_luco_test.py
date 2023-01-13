
import os
from datasets_iterator import dataset_itr

import argparse

# data_root = "/run/user/1000/gvfs/smb-share:server=10.84.164.159,share=datasets" #os.environ.get("DATASETS")
# dataset_name = "paris_luco"
# dataset_name = "kitti"
# sequence = 0


parser = argparse.ArgumentParser(
                    prog = 'Dataset loader',
                    description = 'print dataset frames')

parser.add_argument('--dataset_name', type=str, default='paris_luco', help='dataset name')
parser.add_argument('--sequence', type=int, default=0, help='sequence number')
parser.add_argument('--data_root', type=str, default='/run/user/1000/gvfs/smb-share:server=10.84.164.159,share=datasets')

args = parser.parse_args()

for raw_frame, timestamp, gt_pose in dataset_itr(args.data_root, args.dataset_name, args.sequence):
    print(raw_frame.shape, timestamp, gt_pose) 