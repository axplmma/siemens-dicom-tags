# siemens-dicom-tags

This code is used for extracting tags from Siemens DICOM files. The code is written in Python and uses the pydicom library.

It's used for Siemens "syngo MR E11" and "syngo MR XA30" software versions. I noticed the software update affected how private or CSA tags are accessed, and I am working a script that will work for both versions.

Currently only the older, "syngo MR E11" software version is supported. I am working on adding support for the newer "syngo MR XA30" software version.

## Files

The `get_dicom_headers.py` file contains the main scripts. The `test_run_here.py` file is used to test the script by accessing the example data- two MRS scans, one made with the old and the other with the new version. 

# Resources

- [Information about CSA header](https://nipy.org/nibabel/dicom/siemens_csa.html) from nibabel website
- [pydicom](https://pydicom.github.io/pydicom/stable/) documentation
- [dicom_parser](https://dicom-parser.readthedocs.io/en/latest/) documentation