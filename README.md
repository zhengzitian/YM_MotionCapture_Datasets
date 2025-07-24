# YM_MotionCapture_Datasets

<p align="center">
  <strong>200 motion data samples, including dancing, walking, and more.</strong> 
</p>


<div align="center">

| <div align="center"> Retarget </div> | <div align="center">  Sim2Sim </div> |  <div align="center"> Physical </div> |
|--- | --- | --- |
| [<img src="gif/retarget.gif" height="280" style="width: auto; height: auto;">]() | [<img src="gif/sim.gif" height="280" style="width: auto; height: auto;">]() | [<img src="gif/real.gif" height="280" style="width: auto; height: auto;">]() |

</div>

#### ⚙️ File Description
Data saved in SMPL format, with the file in NPZ format, can be used with the PHC project.
- `--data`: The retargeted data for the "YunMu" E-model robot is as shown in the example.
- `--robots`: The URDF file containing the YunMu E-model robot.
- `--ym_datasets_version1`: containing motion capture data.
- `--visualize_npz.py`: npz data visualization.

### visualization
Run the following command to start check datasets:
```bash
python visualize_npz.py -n ./ym_datasets_version1/ATLstop/63.npz
```
Run this command to view motion number 63 in the ATLstop dance action set.
