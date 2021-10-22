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
  slp_high = 944.46
  slp_low = 934.92  
  region = "Eye"
  accepted_time_file = "./wrfout_d01_2005-08-28_15:10:00"

  outputFolder = "Output/Extracted_csv_variables7.1"
  system("mkdir -p " + outputFolder)

; We generate plots, but what kind do we prefer?
  type = "pdf" ;"X11","pdf","ps","ncgm"

  ; LOAD FILES
  DATADir = "./"
  FILES = systemfunc (" ls -1 " + DATADir + "wrfout_d0* ")
  numFILES = dimsizes(FILES)

  a = addfile(FILES(0)+".nc","r")
  dims = dimsizes(a->P(0,:,:,:))
  nlev  = dims(0)
  nlat  = dims(1)
  nlon  = dims(2)

  ncl_sp_tm_avg_ur    = new((/nlev/),float)
  ncl_sp_tm_avg_uth   = new((/nlev/),float)
  ncl_sp_tm_avg_uz    = new((/nlev/),float)
  ncl_sp_tm_avg_urur  = new((/nlev/),float)
  ncl_sp_tm_avg_uruth = new((/nlev/),float)
  ncl_sp_tm_avg_uruz  = new((/nlev/),float)
  ncl_sp_tm_avg_uthuth= new((/nlev/),float)
  ncl_sp_tm_avg_uthuz = new((/nlev/),float)
  ncl_sp_tm_avg_uzuz  = new((/nlev/),float)
  ncl_sp_tm_avg_mrr   = new((/nlev/),float)
  ncl_sp_tm_avg_mrth  = new((/nlev/),float)
  ncl_sp_tm_avg_mrz   = new((/nlev/),float)
  ncl_sp_tm_avg_mthth = new((/nlev/),float)
  ncl_sp_tm_avg_mthz  = new((/nlev/),float)
  ncl_sp_tm_avg_mzz   = new((/nlev/),float)
  ncl_sp_avg_z        = new((/nlev/),float)
  ncl_sp_avg_r        = new((/nlev/),float)
  ncl_sp_avg_Trr   = new((/nlev/),float)
  ncl_sp_avg_Trth  = new((/nlev/),float)
  ncl_sp_avg_Trz   = new((/nlev/),float)
  ncl_sp_avg_Tthth = new((/nlev/),float)
  ncl_sp_avg_Tthz  = new((/nlev/),float)
  ncl_sp_avg_Tzz   = new((/nlev/),float)
  ncl_sp_tm_avg_tke   = new((/nlev/),float)
  ncl_sp_tm_avg_tke2   = new((/nlev/),float) ; Calculater from 1/2*tr(Rij)
  ;ncl_min_r        = new((/nlev/),float)
  ;ncl_max_r        = new((/nlev/),float)
  ncl_sp_avg_spd      = new((/nlev/),float)
  ;ncl_min_spd_in_r      = new((/nlev/),float)
  ;ncl_max_spd_in_r      = new((/nlev/),float)
  ;ncl_max_spd           = new((/nlev/),float)

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

        tm_avg_u1 = wrf_user_getvar(a,"TM_AVG_U1",itime)       ; 3D U at mass points interpolated in ncl 
        tm_avg_u2 = wrf_user_getvar(a,"TM_AVG_U2",itime)       ; 3D V at mass points interpolated in ncl 
        tm_avg_u3 = wrf_user_getvar(a,"TM_AVG_U3",itime)       ; 3D W at mass points interpolated in ncl 
        tm_avg_u1u1 = wrf_user_getvar(a,"TM_AVG_U1U1",itime)   ; 3D UU at mass points interpolated in ncl 
        tm_avg_u1u2 = wrf_user_getvar(a,"TM_AVG_U1U2",itime)   ; 3D UV at mass points interpolated in ncl 
        tm_avg_u1u3 = wrf_user_getvar(a,"TM_AVG_U1U3",itime)   ; 3D UW at mass points interpolated in ncl 
        tm_avg_u2u2 = wrf_user_getvar(a,"TM_AVG_U2U2",itime)   ; 3D VV at mass points interpolated in ncl 
        tm_avg_u2u3 = wrf_user_getvar(a,"TM_AVG_U2U3",itime)   ; 3D VW at mass points interpolated in ncl 
        tm_avg_u3u3 = wrf_user_getvar(a,"TM_AVG_U3U3",itime)   ; 3D WW at mass points interpolated in ncl 
        tm_avg_m11  = wrf_user_getvar(a,"TM_AVG_M11",itime)    ; 3D M11 at mass points  
        tm_avg_m12  = wrf_user_getvar(a,"TM_AVG_M12",itime)    ; 3D M12 at mass points  
        tm_avg_m13  = wrf_user_getvar(a,"TM_AVG_M13",itime)    ; 3D M13 at mass points  
        tm_avg_m22  = wrf_user_getvar(a,"TM_AVG_M22",itime)    ; 3D M22 at mass points  
        tm_avg_m23  = wrf_user_getvar(a,"TM_AVG_M23",itime)    ; 3D M23 at mass points  
        tm_avg_m33  = wrf_user_getvar(a,"TM_AVG_M33",itime)    ; 3D M33 at mass points  
        tm_avg_tke  = wrf_user_getvar(a,"TM_AVG_TKE",itime)    ; 3D TKE at mass points  

        slp     = wrf_user_getvar(a,"slp",itime)    ; 2D pressure at sea level
        ;U       = wrf_user_getvar(a,"U",itime)      ; 3D U at mass points from file 2
        ;V       = wrf_user_getvar(a,"V",itime)      ; 3D V at mass points from file 2
        ;SPEED   = (tm_avg_u1*tm_avg_u1 + tm_avg_u2*tm_avg_u2)^(0.5) ; m/sec
        ;SPEED@description = "Wind Speed"
        ;SPEED@units = "m/s"
        ;SPEED@lat2d = wrf_user_getvar(a,"XLAT",itime)   ; latitude/longitude
        ;SPEED@lon2d = wrf_user_getvar(a,"XLONG",itime)  ; required for plotting

        LAT     = wrf_user_getvar(a, "XLAT",itime)
        LONG    = wrf_user_getvar(a, "XLONG",itime)

        ; Find the eye:
        P1D      = ndtooned(slp) ; Convert 2D to 1D
        dsizes_P = dimsizes(slp)
        indices  = ind_resolve(minind(P1D),dsizes_P)
        ilat = indices(0,0)
        jlon = indices(0,1)
        eye_LAT  = LAT(ilat,jlon)
        eye_LONG = LONG(ilat,jlon)
        eye_slp = min(slp)

        dims = dimsizes(a->m11(itime,:,:,:))
        nlev  = dims(0)
        nlat  = dims(1)
        nlon  = dims(2)

        ; Reset data
        do k=0,nlev-1
          ncl_sp_tm_avg_ur(k)  = 0.0
          ncl_sp_tm_avg_uth(k) = 0.0
          ncl_sp_tm_avg_uz(k)  = 0.0
          ncl_sp_tm_avg_urur(k)  = 0.0
          ncl_sp_tm_avg_uruth(k) = 0.0
          ncl_sp_tm_avg_uruz(k)  = 0.0
          ncl_sp_tm_avg_uthuth(k) = 0.0
          ncl_sp_tm_avg_uthuz(k)  = 0.0
          ncl_sp_tm_avg_uzuz(k) = 0.0
          ncl_sp_tm_avg_mrr(k)  = 0.0
          ncl_sp_tm_avg_mrth(k) = 0.0
          ncl_sp_tm_avg_mrz(k)  = 0.0
          ncl_sp_tm_avg_mthth(k)= 0.0
          ncl_sp_tm_avg_mthz(k) = 0.0
          ncl_sp_tm_avg_mzz(k)  = 0.0
          ncl_sp_avg_z(k)      = 0.0
          ncl_sp_avg_r(k)      = 0.0
          ncl_sp_avg_spd(k)    = 0.0
          ncl_sp_avg_Trr(k)    = 0.0
          ncl_sp_avg_Trth(k)   = 0.0
          ncl_sp_avg_Trz(k)    = 0.0
          ncl_sp_avg_Tthth(k)  = 0.0
          ncl_sp_avg_Tthz(k)   = 0.0
          ncl_sp_avg_Tzz(k)    = 0.0
          ncl_sp_tm_avg_tke(k)    = 0.0
          ncl_sp_tm_avg_tke2(k)   = 0.0
        end do 

        ; Summing and averaging data
        counter = 0.0
        do i=0,nlat-1
          do j=0,nlon-1
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
                u = tm_avg_u1(k,i,j)
                v = tm_avg_u2(k,i,j)
                w = tm_avg_u3(k,i,j)
                uu = tm_avg_u1u1(k,i,j)
                uv = tm_avg_u1u2(k,i,j)
                uw = tm_avg_u1u3(k,i,j)
                vv = tm_avg_u2u2(k,i,j)
                vw = tm_avg_u2u3(k,i,j)
                ww = tm_avg_u3u3(k,i,j)
                m11 = tm_avg_m11(k,i,j)
                m12 = tm_avg_m12(k,i,j)
                m13 = tm_avg_m13(k,i,j)
                m22 = tm_avg_m22(k,i,j)
                m23 = tm_avg_m23(k,i,j)
                m33 = tm_avg_m33(k,i,j)
                tke = tm_avg_tke(k,i,j)

                spd     = (u*u + v*v)^(0.5) ; m/sec
                ; Convert to Polar
                ;-----------------
                ; ur - radial velocity:  
                ur  =  u*cos(th) + v*sin(th)
                ; uth - azimuthal velocity:
                uth = -u*sin(th) + v*cos(th)
                ; uz - elevation velocity
                uz = w

                ; ur.ur & mrr
                urur = uu*cos(th)*cos(th) + 2.0*uv*cos(th)*sin(th) + vv*sin(th)*sin(th)
                mrr = m11*cos(th)*cos(th) + 2.0*m12*cos(th)*sin(th) + m22*sin(th)*sin(th)
                ; ur.uth & mrth
                uruth = -uu*sin(th)*cos(th) - uv*sin(th)*sin(th) + uv*cos(th)*cos(th) + vv*sin(th)*cos(th) 
                mrth = -m11*sin(th)*cos(th) - m12*sin(th)*sin(th) + m12*cos(th)*cos(th) + m22*sin(th)*cos(th) 
                ; ur.uz & mrz
                uruz = uw*cos(th) + vw*sin(th) 
                mrz = m13*cos(th) + m23*sin(th) 
                ; uth.uth & mthth
                uthuth = uu*sin(th)*sin(th) - 2*uv*sin(th)*cos(th) + vv*cos(th)*cos(th)
                mthth = m11*sin(th)*sin(th) - 2*m12*sin(th)*cos(th) + m22*cos(th)*cos(th)
                ; uth.uz = -uw*sin(th) + vw*cos(th)
                uthuz = -uw*sin(th) + vw*cos(th)
                mthz = -m13*sin(th) + m23*cos(th)
                ; uz.uz = ww
                uzuz = ww 
                mzz  = m33

                ; Summing up Polar velocity
                ;--------------------------
                ncl_sp_tm_avg_ur(k)     = ncl_sp_tm_avg_ur(k)  + ur
                ncl_sp_tm_avg_uth(k)    = ncl_sp_tm_avg_uth(k) + uth
                ncl_sp_tm_avg_uz(k)     = ncl_sp_tm_avg_uz(k)  + uz

                ncl_sp_tm_avg_urur(k)   = ncl_sp_tm_avg_urur(k)   + urur
                ncl_sp_tm_avg_uruth(k)  = ncl_sp_tm_avg_uruth(k)  + uruth
                ncl_sp_tm_avg_uruz(k)   = ncl_sp_tm_avg_uruz(k)   + uruz
                ncl_sp_tm_avg_uthuth(k) = ncl_sp_tm_avg_uthuth(k) + uthuth
                ncl_sp_tm_avg_uthuz(k)  = ncl_sp_tm_avg_uthuz(k)  + uthuz
                ncl_sp_tm_avg_uzuz(k)   = ncl_sp_tm_avg_uzuz(k)   + uzuz

                ncl_sp_tm_avg_mrr(k)   = ncl_sp_tm_avg_mrr(k)   + mrr
                ncl_sp_tm_avg_mrth(k)  = ncl_sp_tm_avg_mrth(k)  + mrth
                ncl_sp_tm_avg_mrz(k)   = ncl_sp_tm_avg_mrz(k)   + mrz
                ncl_sp_tm_avg_mthth(k) = ncl_sp_tm_avg_mthth(k) + mthth
                ncl_sp_tm_avg_mthz(k)  = ncl_sp_tm_avg_mthz(k)  + mthz
                ncl_sp_tm_avg_mzz(k)   = ncl_sp_tm_avg_mzz(k)   + mzz

                ncl_sp_avg_z(k)   = ncl_sp_avg_z(k) + z(k,i,j)
                ncl_sp_avg_r(k)   = ncl_sp_avg_r(k) + radius
                ncl_sp_avg_spd(k) = ncl_sp_avg_spd(k) +  spd

                ncl_sp_avg_Trr(k)    = ncl_sp_avg_Trr(k)    + urur   - ur*ur
                ncl_sp_avg_Trth(k)   = ncl_sp_avg_Trth(k)   + uruth  - ur*uth
                ncl_sp_avg_Trz(k)    = ncl_sp_avg_Trz(k)    + uruz   - ur*uz
                ncl_sp_avg_Tthth(k)  = ncl_sp_avg_Tthth(k)  + uthuth - uth*uth
                ncl_sp_avg_Tthz(k)   = ncl_sp_avg_Tthz(k)   + uthuz  - uth*uz
                ncl_sp_avg_Tzz(k)    = ncl_sp_avg_Tzz(k)    + uzuz   - uz*uz

                ncl_sp_tm_avg_tke(k) = ncl_sp_tm_avg_tke(k) + tke
                ncl_sp_tm_avg_tke2(k) = ncl_sp_tm_avg_tke2(k) + 0.5*((urur - ur*ur)^2 + (uthuth - uth*uth)^2 + (uzuz - uz*uz)^2)
              end do
            end if
          end do
        end do

        ; Averaging Polar velocity and Saving it
        ;----------------------------------------
        filename = outputFolder+"/Vel_data_"+region+"_t"+times(itime)+"_slph"+slp_high+"_slpl"+slp_low+".csv"
        header = "This ASCII file contains velocity data taken from wrf and then converted to polar with slp range "+slp_low+" to "+slp_high 
        write_table(filename, "w", [/header/], "%s")    ; Use "w" to create file
        alist = [/"index,z,ncl_sp_tm_avg_ur,ncl_sp_tm_avg_uth,ncl_sp_tm_avg_uz,ncl_sp_tm_avg_urur,ncl_sp_tm_avg_uruth,ncl_sp_tm_avg_uruz,ncl_sp_tm_avg_uthuth,ncl_sp_tm_avg_uthuz,ncl_sp_tm_avg_uzuz,ncl_sp_tm_avg_mrr,ncl_sp_tm_avg_mrth,ncl_sp_tm_avg_mrz,ncl_sp_tm_avg_mthth,ncl_sp_tm_avg_mthz,ncl_sp_tm_avg_mzz,ncl_sp_avg_r,ncl_sp_avg_spd,ncl_sp_avg_Trr,ncl_sp_avg_Trth,ncl_sp_avg_Trz,ncl_sp_avg_Tthth,ncl_sp_avg_Tthz,ncl_sp_avg_Tzz,ncl_sp_tm_avg_tke,ncl_sp_tm_avg_tke2,End"/]
        write_table(filename, "a", alist, "%s") 

        do k=0,nlev-1
          ncl_sp_avg_z(k)        = ncl_sp_avg_z(k)/counter
          ncl_sp_avg_r(k)        = ncl_sp_avg_r(k)/counter
          ncl_sp_avg_spd(k)      = ncl_sp_avg_spd(k)/counter

          ncl_sp_tm_avg_ur(k)     = ncl_sp_tm_avg_ur(k)/counter
          ncl_sp_tm_avg_uth(k)    = ncl_sp_tm_avg_uth(k)/counter
          ncl_sp_tm_avg_uz(k)     = ncl_sp_tm_avg_uz(k)/counter 

          ncl_sp_tm_avg_urur(k)   = ncl_sp_tm_avg_urur(k)/counter
          ncl_sp_tm_avg_uruth(k)  = ncl_sp_tm_avg_uruth(k)/counter
          ncl_sp_tm_avg_uruz(k)   = ncl_sp_tm_avg_uruz(k)/counter
          ncl_sp_tm_avg_uthuth(k) = ncl_sp_tm_avg_uthuth(k)/counter
          ncl_sp_tm_avg_uthuz(k)  = ncl_sp_tm_avg_uthuz(k)/counter
          ncl_sp_tm_avg_uzuz(k)   = ncl_sp_tm_avg_uzuz(k)/counter

          ncl_sp_tm_avg_mrr(k)   = ncl_sp_tm_avg_mrr(k)/counter
          ncl_sp_tm_avg_mrth(k)  = ncl_sp_tm_avg_mrth(k)/counter
          ncl_sp_tm_avg_mrz(k)   = ncl_sp_tm_avg_mrz(k)/counter
          ncl_sp_tm_avg_mthth(k) = ncl_sp_tm_avg_mthth(k)/counter
          ncl_sp_tm_avg_mthz(k)  = ncl_sp_tm_avg_mthz(k)/counter
          ncl_sp_tm_avg_mzz(k)   = ncl_sp_tm_avg_mzz(k)/counter

          ncl_sp_avg_Trr(k)    = ncl_sp_avg_Trr(k)  /counter
          ncl_sp_avg_Trth(k)   = ncl_sp_avg_Trth(k) /counter
          ncl_sp_avg_Trz(k)    = ncl_sp_avg_Trz(k)  /counter
          ncl_sp_avg_Tthth(k)  = ncl_sp_avg_Tthth(k)/counter
          ncl_sp_avg_Tthz(k)   = ncl_sp_avg_Tthz(k) /counter
          ncl_sp_avg_Tzz(k)    = ncl_sp_avg_Tzz(k)  /counter

          ncl_sp_tm_avg_tke(k) = ncl_sp_tm_avg_tke(k) / counter
          ncl_sp_tm_avg_tke2(k) = ncl_sp_tm_avg_tke2(k) / counter
          ; Write the data
          mlist = [/k,ncl_sp_avg_z(k),ncl_sp_tm_avg_ur(k),ncl_sp_tm_avg_uth(k),ncl_sp_tm_avg_uz(k),ncl_sp_tm_avg_urur(k),ncl_sp_tm_avg_uruth(k),ncl_sp_tm_avg_uruz(k),ncl_sp_tm_avg_uthuth(k),ncl_sp_tm_avg_uthuz(k),ncl_sp_tm_avg_uzuz(k),ncl_sp_tm_avg_mrr(k),ncl_sp_tm_avg_mrth(k),ncl_sp_tm_avg_mrz(k),ncl_sp_tm_avg_mthth(k),ncl_sp_tm_avg_mthz(k),ncl_sp_tm_avg_mzz(k),ncl_sp_avg_r(k),ncl_sp_avg_spd(k),ncl_sp_avg_Trr(k),ncl_sp_avg_Trth(k),ncl_sp_avg_Trz(k),ncl_sp_avg_Tthth(k),ncl_sp_avg_Tthz(k),ncl_sp_avg_Tzz(k),ncl_sp_tm_avg_tke(k),ncl_sp_tm_avg_tke2(k),0/]

          write_table(filename, "a", mlist, "%d,%.8e,%.8e,%.8e,%.8e,%.8e,%.8e,%.8e,%.8e,%.8e,%.8e,%.8e,%.8e,%.8e,%.8e,%.8e,%.8e,%.8e,%.8e,%.8e,%.8e,%.8e,%.8e,%.8e,%.8e,%.8e,%.8e,%d") 

        end do
        counter = 0.0
        ;print("Done with time " + times(itime))
    end do
    print("Done with File " + FILES(numF))
  end do

end



