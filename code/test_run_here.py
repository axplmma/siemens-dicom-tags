from get_dicom_headers import dicom_siemens_scan

data_new = "data/sub-223_ses-MRI1_voi-ACC_acq-pres_svs.dcm"
data_old = "data/sub-102_ses-MRI1_voi-ACC_acq-pres_svs.dcm"

participant223 = dicom_siemens_scan(data_new)
participant102 = dicom_siemens_scan(data_old)

# print(participant102.software_version)
# print(participant102.public_tags)
# print(participant102.private_tags)

# print(participant223.software_version)
print(participant223.public_tags)
print(participant223.private_tags)