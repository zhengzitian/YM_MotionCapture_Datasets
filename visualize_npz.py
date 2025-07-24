import os
import torch
import argparse
import numpy as np
import sys
sys.path.append(os.getcwd())
from smpl_sim.smpllib.smpl_parser import (
    SMPL_Parser,
)

import joblib
from smpl_sim.utils.pytorch3d_transforms import axis_angle_to_matrix
from smpl_sim.smpllib.smpl_joint_names import SMPL_MUJOCO_NAMES, SMPL_BONE_ORDER_NAMES, SMPLH_BONE_ORDER_NAMES, SMPLH_MUJOCO_NAMES
from matplotlib import pyplot as plt
from pathlib import Path
import imageio


def visualize_npz(npz_file, output_video="animation1.mp4", fps=30):
    # 加载 .npz 文件
    try:
        data = np.load(npz_file)
    except Exception as e:
        print(f"Error loading {npz_file}: {e}")
        return  


    print("Key names in NPZ files:", data.files)  
    smpl_pose = data["poses"]  # (T, 72)
    smpl_trans = data["trans"]  # (T, 3)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    smpl_parser_n = SMPL_Parser(model_path="data/smpl", gender="neutral")
    shape_new, _ = joblib.load("data/y1/shape_optimized_v1.pkl")  # shape_new = np.zeros(10)

    
    verts, joints = smpl_parser_n.get_joints_verts(torch.from_numpy(smpl_pose), shape_new, torch.from_numpy(smpl_trans))
    j3d_joints = joints.detach().numpy()
    idx = 0

    
    fig=plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.view_init(90, 0)  
    ax.set_xticks([])  
    ax.set_yticks([])  
    ax.set_zticks([])  

    ax.set_xlim(-1, 2)
    ax.set_ylim(-1, 2)
    ax.set_zlim(-1, 2)
    ax.grid(True)  

    

    scat = ax.scatter(
        j3d_joints[0, :, 0],
        j3d_joints[0, :, 1],
        j3d_joints[0, :, 2],
        c='b')

    frames = []
    for frame in range(len(j3d_joints)):
        scat._offsets3d = (
            j3d_joints[frame, :, 0],
            j3d_joints[frame, :, 1],
            j3d_joints[frame, :, 2])
        fig.canvas.draw()
        frame_image = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        frame_image = frame_image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        frame_image_rotated = np.rot90(frame_image, k=1)  
        frames.append(frame_image_rotated)


    imageio.mimsave(output_video, frames, fps=fps)
    print(f"Animation saved to {output_video}")
    plt.close(fig)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize SMPL/SMPL-X from .npz")

    parser.add_argument("--npz_path", "-n", type=str, default="ym_datasets_version1/ALF/34.npz", help="Input .npz file path under 'ym_datasets_version1/',e.g., 'ym_datasets_version1/ALF/34.npz'")
    parser.add_argument("--output_video", "-o", type=str, default="animation1.mp4", help="Output video path")
    parser.add_argument("--fps", type=int, default=30, help="Frames per second")
    args = parser.parse_args()
    
    base_dir = Path("./ym_datasets_version1")
    npz_path = base_dir / args.npz_path

    visualize_npz(args.npz_path, args.output_video, args.fps)


    #python visualize_npz.py -n ./ym_datasets_version1/ATLstop/63.npz