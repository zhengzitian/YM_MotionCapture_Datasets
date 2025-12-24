import os
import torch
import argparse
import numpy as np
import sys
sys.path.append(os.getcwd())

from smpl_sim.smpllib.smpl_parser import SMPL_Parser
import joblib
from matplotlib import pyplot as plt
from pathlib import Path
import imageio


def load_motion_npz(npz_path):
    """
    兼容：
    1) 纯数值 npz
    2) 含字符串 / metadata 的 npz（AMASS / PHC 风格）
    """
    try:
        data = np.load(npz_path)
    except ValueError:
        # 包含 string / object，需要允许 pickle
        data = np.load(npz_path, allow_pickle=True)

    motion = {}
    for k in data.files:
        v = data[k]
        # 只保留数值类型（float / int）
        if isinstance(v, np.ndarray) and v.dtype.kind in {"f", "i"}:
            motion[k] = v

    return motion, data


def visualize_npz(npz_file, output_video="animation1.mp4", fps=30):
    # ========= 加载 npz（自动兼容） =========
    try:
        motion, raw = load_motion_npz(npz_file)
    except Exception as e:
        print(f"Error loading {npz_file}: {e}")
        return

    print("Keys in NPZ:", raw.files)

    # ========= 必要字段检查 =========
    if "poses" not in motion or "trans" not in motion:
        raise KeyError("npz 文件中必须包含 'poses' 和 'trans'")

    smpl_pose = motion["poses"]      # (T, 72)
    smpl_trans = motion["trans"]     # (T, 3)

    # ========= 可选 metadata =========
    gender = raw["gender"].item() if "gender" in raw.files else "neutral"
    fps = int(raw["mocap_framerate"]) if "mocap_framerate" in raw.files else fps

    # ========= SMPL 初始化 =========
    smpl_parser = SMPL_Parser(
        model_path="data/smpl",
        gender=gender
    )

    shape_new, _ = joblib.load("data/y1/shape_optimized_v1.pkl")

    # ========= SMPL 前向 =========
    verts, joints = smpl_parser.get_joints_verts(
        torch.from_numpy(smpl_pose).float(),
        shape_new,
        torch.from_numpy(smpl_trans).float()
    )

    j3d_joints = joints.detach().cpu().numpy()  # (T, J, 3)

    # ========= 可视化 =========
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
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
        c="b",
        s=10
    )

    frames = []
    for t in range(len(j3d_joints)):
        scat._offsets3d = (
            j3d_joints[t, :, 0],
            j3d_joints[t, :, 1],
            j3d_joints[t, :, 2],
        )
        fig.canvas.draw()

        frame = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        frame = frame.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        frame = np.rot90(frame, k=1)
        frames.append(frame)

    imageio.mimsave(output_video, frames, fps=fps)
    print(f"Animation saved to {output_video}")

    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Visualize SMPL motion from npz (robust version)"
    )
    parser.add_argument(
        "--npz_path", "-n",
        type=str,
        required=True,
        help="Path to npz file, e.g. dbsj/ATLstop/63.npz"
    )
    parser.add_argument(
        "--output_video", "-o",
        type=str,
        default="animation1.mp4",
        help="Output video path"
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=30,
        help="Frames per second"
    )

    args = parser.parse_args()

    visualize_npz(args.npz_path, args.output_video, args.fps)

    # 示例：
    # python visualize_npz.py -n dbsj/ATLstop/63.npz -o atlstop_63.mp4
