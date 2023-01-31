
import os
import slam_dataset_sdk
from slam_dataset_sdk.datasets_iterator import dataset_itr, get_supported_datasets

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
parser.add_argument('--data_root', type=str, default='/run/user/1000/gvfs/smb-share:server=10.84.162.67,share=datasets')

parser.add_argument('--list_dataset', type=bool, default=False, help='supported dataset names list')


args = parser.parse_args()

spported_datasets = get_supported_datasets() 
if args.dataset_name not in spported_datasets:
    print("Error : Unsupported dataset name")
if args.list_dataset or args.dataset_name not in spported_datasets:
    print("Supported datasets:")
    print(spported_datasets)
    print("Usage: python3 paris_luco_test.py --dataset_name <supported_dataset_name> --sequence <seq_number> --data_root <dataset_root_dir>")
    print("output for dataset_itr: dict{raw_frame, timestamp, gt_pose}")
    exit(0)


# for raw_frame, timestamp, gt_pose in dataset_itr(args.data_root, args.dataset_name, args.sequence):
#     print(raw_frame, timestamp, gt_pose) 

for data in dataset_itr(args.data_root, args.dataset_name, args.sequence):
    print(data['raw_frame'].shape, data['timestamp'], data['gt_pose'])
