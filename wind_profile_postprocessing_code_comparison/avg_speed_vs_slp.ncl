;   Script display location of model domains
;   Only works for ARW domains
;   Only works for NCL versions 6.2 or later
;   Reads namelist file directly

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/wrf/WRF_contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/wrf/WRFUserARW.ncl"

begin
  pi  = 3.14159265359
  slp_high = 982.410234 
  slp_low = 962.956566  
  region = "Eye"
  accepted_time_file = "/project/momen/meng/COAWST/results/WRF_VS_WRFSWAN_2/Katrina/8km/WRFONLY_NoTurb_8km_isftcflx_2_changeClz_1p0000/wrfout_d01_2005-08-29_18:00:00"

  outputFolder = "/project/momen/meng/COAWST/results/WRF_VS_WRFSWAN_2/Katrina/Extracted_csv_variables"
  system("mkdir -p " + outputFolder)

; We generate plots, but what kind do we prefer?
  type = "pdf" ;"X11","pdf","ps","ncgm"

  ; LOAD FILES
  DATADir = "/project/momen/meng/COAWST/results/WRF_VS_WRFSWAN_2/Katrina/8km/WRFONLY_NoTurb_8km_isftcflx_2_changeClz_1p0000/"
  FILES = systemfunc(" ls " + DATADir + "wrfout_d0* ")
  numFILES = dimsizes(FILES)


  a = addfile(FILES(0)+".nc","r")
  dims = dimsizes(a->P(0,:,:,:))
  nlev  = dims(0)
  nlat  = dims(1)
  nlon  = dims(2)


  ncl_sp_tm_avg_ur    = new((/nlev/),float)
  ncl_sp_tm_avg_uth   = new((/nlev/),float)
  ncl_sp_avg_z        = new((/nlev/),float)


  ; File Loop
  do numF=0,numFILES-1

    a = addfile(FILES(numF)+".nc","r")
    if FILES(numF) .ne. accepted_time_file then
      continue
    end if

    times = wrf_user_getvar(a,"times",-1)   ; get all times in the file
    ntimes = dimsizes(times)                ; number of times in the file
    Times_wrf_2 = wrf_times_c(a->Times,2)   ; converting time data to double

    ; Time Loop
    do itime=0,ntimes-1 
        print("Working on " + times(itime))
                                         
        z = wrf_user_getvar(a,"z",itime)  ; 3D z at mass points 


        slp     = wrf_user_getvar(a,"slp",itime)    ; 2D pressure at sea level


        LAT     = wrf_user_getvar(a, "XLAT",itime)
        LONG    = wrf_user_getvar(a, "XLONG",itime)

        u = wrf_user_getvar(a,"U",itime)                    
        v = wrf_user_getvar(a,"V",itime)     

        ; Find the eye:
        P1D      = ndtooned(slp) ; Convert 2D to 1D
        dsizes_P = dimsizes(slp)
        indices  = ind_resolve(minind(P1D),dsizes_P)
        ilat = indices(0,0)
        jlon = indices(0,1)
        eye_LAT  = LAT(ilat,jlon)
        eye_LONG = LONG(ilat,jlon)
        eye_slp = min(slp)

        ;dims = dimsizes(a->m11(itime,:,:,:))
        ;nlev  = dims(0)
        ;nlat  = dims(1)
        ;nlon  = dims(2)


        ; Reset data
        do k=0,nlev-1
          ncl_sp_tm_avg_ur(k)  = 0.0
          ncl_sp_tm_avg_uth(k) = 0.0
          ncl_sp_avg_z(k)      = 0.0
        end do 
        print(eye_slp)
        ; Summing and averaging data
        counter = 0.0
        do i=0,nlat-1
          do j=0,nlon-1
            ;print(i)
            ;print(j)
            ;print(slp(i,j))
            ;print(slp(i,j) .le. slp_high)
            if ((slp(i,j) .le. slp_high) .and. (slp(i,j) .ge. slp_low)) then ; 
           
              counter = counter + 1.0

              ; Find r & theta
              ;----------------
              radius = gc_latlon(eye_LAT,eye_LONG, LAT(i,j),LONG(i,j), 20,3) ; return the distance in meters
              y_lat = gc_latlon(eye_LAT,eye_LONG, LAT(i,j),eye_LONG, 20,3) ; return the distance in meters
              x_lon = gc_latlon(eye_LAT,eye_LONG, eye_LAT,LONG(i,j), 20,3) ; return the distance in meters
              th = 0.0 ; theta

              if (x_lon .eq. 0.0)  then
                if ( LAT(i,j) .ge. eye_LAT) then
                  th = pi/2.0
                else 
                  th = -pi/2.0
                end if
              else
                th = atan(y_lat/x_lon)

                if ( (LONG(i,j) .le. eye_LONG) .and. (LAT(i,j) .ge. eye_LAT) ) then ; 2nd Quadrant
                  th = pi - th
                else if ( (LONG(i,j) .le. eye_LONG) .and. (LAT(i,j) .le. eye_LAT) ) then ; 3rd Quadrant
                  th = th + pi
                else if ( (LONG(i,j) .ge. eye_LONG) .and. (LAT(i,j) .le. eye_LAT) ) then ; 4th Quadrant
                  th = -th
                end if 
                end if
                end if
              end if

              do k=0,nlev-1

                ;spd     = (u*u + v*v)^(0.5) ; m/sec
                ; Convert to Polar
                ;-----------------
                ; ur - radial velocity:  
                ur  =  u(k,i,j)*cos(th) + v(k,i,j)*sin(th)
                ; uth - azimuthal velocity:
                uth = -u(k,i,j)*sin(th) + v(k,i,j)*cos(th)


                ; Summing up Polar velocity
                ;--------------------------
                ncl_sp_tm_avg_ur(k)     = ncl_sp_tm_avg_ur(k)  + ur
                ncl_sp_tm_avg_uth(k)    = ncl_sp_tm_avg_uth(k) + uth
                ncl_sp_avg_z(k)   = ncl_sp_avg_z(k) + z(k,i,j)


              end do
            end if
          end do
        end do
        print("counter: "+counter)

        ; Averaging Polar velocity and Saving it
        ;----------------------------------------
        filename = outputFolder+"/Vel_data_"+region+"_t"+times(itime)+"_slph"+slp_high+"_slpl"+slp_low+".csv"
        ;header = "This ASCII file contains velocity data taken from wrf and then converted to polar with slp range "+slp_low+" to "+slp_high 
        ;write_table(filename, "w", [/header/], "%s")    ; Use "w" to create file
        alist = [/"z,ncl_sp_tm_avg_ur,ncl_sp_tm_avg_uth"/]
        write_table(filename, "a", alist, "%s") 

        do k=0,nlev-1

          ncl_sp_avg_z(k)        = ncl_sp_avg_z(k)/counter
          ncl_sp_tm_avg_ur(k)     = ncl_sp_tm_avg_ur(k)/counter
          ncl_sp_tm_avg_uth(k)    = ncl_sp_tm_avg_uth(k)/counter


          ; Write the data
          mlist = [/z(k,0,0),ncl_sp_tm_avg_ur(k),ncl_sp_tm_avg_uth(k)/]

          write_table(filename, "a", mlist, "%.8e,%.8e,%.8e") 

        end do
        counter = 0.0
    end do
    print("Done with File " + FILES(numF))
  end do

end



