# siemens dicom tags

## Purpose
This code is used for extracting tags from Siemens DICOM files. I created it for use with my PhD project data; as the currently available python packages were not able to access most of the header data. I use [dcm2bids](https://github.com/UNFmontreal/Dcm2Bids) for creating sidecar files for all other data types, but since MRS is not yet icluded in the BIDS standard, the dcm2bids package does not create sidecar files for MRS data (hence my focus specifically on this type of data). I also tried using [spec2nii](https://github.com/wtclarke/spec2nii) which is capable of creating sidecar files for my MRS data, but they contain minimal information, as the script doesn't access private tags.
The sidecar files I got using 

## Siemens software version supported
In the middle of data collection the scanner had a software update, which affected how the dicom headers are written. As a result the two software versions has dicom headers that have to be accessed differently, The older version ("syngo MR E11") stores the data isn CSA tags, while the newer version ("syngo MR XA30") stores it in private tags.

Currently the script can access non-private tags from both versions of the software, but accessing private tags and exporting to json works only the older version. I am working on adding support for the newer "syngo MR XA30" software version. I have only tested the script on MRS data, and probably won't add support for other data types. 

## Libraries used
The code is written in Python and uses the [pydicom](https://github.com/pydicom/pydicom) and [dicom_parser](https://github.com/open-dicom/dicom_parser) libraries.

## Files

The `get_dicom_headers.py` file contains the main scripts. The `test_run_here.py` file is used to test the script by accessing the example data- two MRS scans, one made with the old and the other with the new version. 

## Resources

If you want to know more about the dicom headers, I found the following resources helpful:

- [Information about CSA header](https://nipy.org/nibabel/dicom/siemens_csa.html) from nibabel website
- [pydicom](https://pydicom.github.io/pydicom/stable/) documentation
- [dicom_parser](https://dicom-parser.readthedocs.io/en/latest/) documentation

## Improvements/ suggestions/ contributions
I don't plan on making this code usable for other file types beyond my PhD project. If any of it is useful to you, feel free to use it. If you're adding support for the types of data included here to your repository I would be happy to help.

## Meme

Here is a meme for your enjoyment:

<img align="left" src="https://www.explainxkcd.com/wiki/images/b/bf/fmri_billboard.png">