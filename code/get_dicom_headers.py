import os
import json
from pydicom import dcmread
from dicom_parser.utils.siemens.csa.header import CsaHeader

class dicom_siemens_scan:

    def __init__(self, dicom_path):
        self.dicom_path = dicom_path
        self.filename = os.path.basename(self.dicom_path).split('.')[0]
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
            raw_csa = self.dicom_data.get((0x029, 0x1110)).value
            raw_tags = CsaHeader(raw_csa).read()
            tags_as_dict = {key: val['value'] for key, val in raw_tags.items()}
            return tags_as_dict
        elif self.software_version == "syngo MR XA30":
            print(f"The software version is {self.software_version}. This script is only compatible with syngo MR E11. Sorry")
            return None
        else: 
            print("The software version is not compatible with this script. Please check the software version.")
            return None
    
    @classmethod
    def convert_to_serializable(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
        raise TimeoutError(f'Object of type {obj.__class__.__name__} is not JSON serializable!')
    
    
    def save_json(self):
        """
        Save available metadata into json format.
        Currently works for private tags and syngo MR E11 only 
        """
        # define json filename
        filename = os.path.basename(self.dicom_path).split('.')[0]
        # print(self.filename)
        json_filename = 'sidecar_files/{}.json'.format(filename)
        if self.software_version == "syngo MR E11":
            # Save the simplified metadata as a JSON file
            with open(json_filename, 'w') as f:
                json.dump(self.public_tags, f, indent=4, default=self.convert_to_serializable)
        else:
            print("I don't know how to save this data to json yet :(")
