from get_dicom_headers import DicomSiemensScan

# OLD software version (syngo MR XA30)
data_102 = "data/sub-102_ses-MRI1_voi-ACC_acq-pres_svs.dcm"
participant102 = DicomSiemensScan(data_102)

# NEW software version (syngo MR E11)
data_217 = "data/sub-217_ses-MRI1_voi-ACC_acq-pres_svs.dcm"
participant217 = DicomSiemensScan(data_217)
data_223 = "data/sub-223_ses-MRI2_voi-ACC_acq-pres_svs.dcm"
participant223 = DicomSiemensScan(data_223)

targetFolder="sidecar_files"

participant102.save_json(targetFolder)
participant217.save_json(targetFolder)
participant223.save_json(targetFolder)
