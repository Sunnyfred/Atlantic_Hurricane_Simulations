#!/bin/bash
#SBATCH -J 2kmfix
#BATCH -N 1 -n 2
#SBATCH -t 5:00:00
#SBATCH -A Momen

#SBATCH --mem=0

module add python/3.8
cd /project/momen/meng/COAWST/results/WRF_VS_WRFSWAN_2/postprocessing_WRFONLY/0_Paper_figures/section2_change_pars_for_strong_winds/source_code_change_Clz_isftcflx_1

###python3 1_Calculate_z0_time_series_at_eye.py
###python3 1_Calculate_z0_time_series_at_eyewall.py
###python3 1_Calculate_wind_intensity_time_series.py
###python3 1_Calculate_wind_track.py
###python3 1_Calculate_avg_speed_vs_radius.py
###python3 1_Calculate_velocity_pressure.py

###python3 1_Calculate_z0_time_series_at_eye_2km.py
###python3 1_Calculate_z0_time_series_at_eyewall_2km.py
###python3 1_Calculate_wind_intensity_time_series_2km.py
###python3 1_Calculate_wind_track_2km.py
###python3 1_Calculate_z0_time_series_at_eyewall_bandavg.py

###python3 1_Calculate_avg_speed_vs_radius_multiple_height.py
###python3 1_Calculate_ZNT_contour_8km.py
###python3 1_Calculate_avg_speed_vs_slp_multiple_height.py

python3 1_Calculate_wind_profiles_16km.py
python3 1_Calculate_wind_profiles_8km.py