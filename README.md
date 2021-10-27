# Atlantic_Hurricane_Simulations
This repository includes the source code and postprocessing codes using Git version control to simulate Atlantic Hurricanes


In this study, the extensively used software WRF are employed to study the impact of surface roughness on the simulation accuracy both in wind intensity and Hurricane tracks.
We studied the sensitivity of momentum roughness and analyzed the results including wind intensity, Hurricane tracks, wind profiles, time series for roughness at Hurricane center
and eyewall, wind speed v.s. radius, wind speed v.s. slp(sea-level pressure), etc.



section1_default_comparison_for_strong_hurricanes: In this section, we choosed different PBL schemes and surface fluxes options. In one case, we explicitly consider the ocean
wave effect by coupling WRF and SWAN using the COAWST system. We compared diifferent cases using the default momentum roughness. 

section2_change_pars_for_strong_hurricanes: In this section, we studies how the momentum roughness affect the strong Hurricane simulations. Here, we define the the strong HUrricane 
based on critical wond speed 50 m/s.

section3_change_pars_for_weak_hurricanes: In this section, we stuudied how the momentum roughness affect the strong Hurricane simulations.

Post_processing_for_observation_data: The observation data is obtained from dropsonde.


