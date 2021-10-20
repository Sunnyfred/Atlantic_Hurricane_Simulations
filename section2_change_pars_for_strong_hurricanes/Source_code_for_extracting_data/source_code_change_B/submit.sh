#!/bin/bash
#SBATCH -J 8kmfixA
#BATCH -N 1 -n 2
#SBATCH -t 5:00:00
#SBATCH -A Momen

module add python/3.8
cd /project/momen/meng/COAWST/results/WRF_VS_WRFSWAN_2/postprocessing_WRFONLY/0_Paper_figures/section2_change_pars_for_strong_winds/source_code_change_B

python3 1_Calculate_z0_time_series_at_eye.py
python3 1_Calculate_z0_time_series_at_eyewall.py

python3 1_Calculate_wind_intensity_time_series.py
python3 1_Calculate_wind_track.py
