/**********************************************************************
02_load_and_verify_data.do
Load analysis data and verify unit/time keys.
Replace placeholder globals with project-specific values.
**********************************************************************/

use "$data", clear

datasignature

* ---------- REQUIRED USER-PROVIDED MACROS ----------
* Replace placeholders before running.
global y              "DEPENDENT_VARIABLE"
global x              "FOCAL_X_OR_TREATMENT"
global controls       "c1 c2 c3"
global unit_id        "unit_id"
global time_id        "time_id"
global cluster_id     "unit_id"
global fe_time        "i.time_id"
global instrument_z   "z"
global treat          "treat"
global group_id       "group_id"

* Verify key if panel
cap isid $unit_id $time_id
if _rc {
    di as error "Unit-time key is not unique. Inspect duplicates before panel/DID/dynamic models."
    duplicates report $unit_id $time_id
}

cap xtset $unit_id $time_id
if _rc {
    di as error "xtset failed. Verify unit_id and time_id before panel models."
}
else {
    xtdescribe
    xtsum $y $x $controls
}

misstable summarize $y $x $controls $instrument_z $treat $unit_id $time_id $cluster_id
