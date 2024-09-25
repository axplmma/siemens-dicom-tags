from pydicom import dcmread
from dicom_parser import Header
from dicom_parser.utils.siemens.csa.header import CsaHeader

class dicom_siemens_scan:

    def __init__(self, dicom_path):
        self.dicom_path = dicom_path
        self.dicom_data = dcmread(self.dicom_path, stop_before_pixels=True)
    
    @property
    def software_version(self):
        """
        Find the software version of the Siemens DICOM file.
        The available software versions for LEV files are 'syngo MR XA30' and 'syngo MR E11'.
        The "old" version is 'syngo MR XA30' and the "new" version is 'syngo MR E11'.
        """
        return self.dicom_data.get((0x018, 0x1020)).value
    
    @property
    def public_tags(self):
        """
        Extract the public tags from the Siemens DICOM file.
        i.e. access the information not stored in private or CSA headers
        """
        return dcmread(self.dicom_path)
    
    @property
    def private_tags(self):
        """
        Extract the private tags hidden in the Siemens DICOM file.
        i.e. either 'private' or 'CSA' headers
        """
        if self.software_version == "syngo MR E11":
            image = Header(self.dicom_data)
            raw_csa = image.get((0x029, 0x1110))
            return CsaHeader(raw_csa).read()
        elif self.software_version == "syngo MR XA30":
            print(f"The software version is {self.software_version}. This script is only compatible with syngo MR E11. Sorry")
            print("Here is the best I can do:")
            image = Header(self.dicom_data)
            # keys = image.keys()
            # print(keys)
            raw_csa = image.get((0x0021, 0x1026))
            # (0x0021, 0x1071)
            # (0x0021, 0x1026)
            # (0x0021, 0x1019)
            return raw_csa
        else: 
            print("The software version is not compatible with this script. Please check the software version.")
            return None