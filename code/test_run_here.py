from get_dicom_headers import dicom_siemens_scan

# OLD software version (syngo MR XA30)
data_102 = "data/sub-102_ses-MRI1_voi-ACC_acq-pres_svs.dcm"
participant102 = dicom_siemens_scan(data_102)

# NEW software version (syngo MR E11)
data_217 = "data/sub-217_ses-MRI1_voi-ACC_acq-pres_svs.dcm"
participant217 = dicom_siemens_scan(data_217)
data_223 = "data/sub-223_ses-MRI2_voi-ACC_acq-pres_svs.dcm"
participant223 = dicom_siemens_scan(data_223)

