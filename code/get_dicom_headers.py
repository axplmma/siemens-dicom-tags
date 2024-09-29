import os
import ast
import json
from pydicom import dcmread
from  pydicom.valuerep import PersonName
from pydicom.multival import MultiValue
from dicom_parser.utils.siemens.csa.header import CsaHeader

class dicom_siemens_scan:
    """
    A class to represent siemens dicom metadata.

    Attributes
    ----------
    `dicom_path` : str
        Path to a dicom file 
    `filename` : str
        Name of the dicom file. Extracted from `dicom_path`, without extension. Used to name the corresponding json file.
    `dicom_data` : FileDataset
        The dicom headers extracted from the file provided with `dicom_path`

    Methods
    -------
    `software_version`
        Accesses the dicom tag `(0018, 1020)` - which contains the software version
    `public_tags`
        Read public (i.e. not CSA & not private) dicom tags
    `private_tags`
        Read CSA or private tags (depending on software version)
    `convert_to_serializable`
        Read dictionary output of dicom tags and decode if needed
    `save_json`
        Save all (private and public) tags as a json file. File has the same as the dicom file and is saved in the same directory. 
    """

    def __init__(self, dicom_path:str):
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
        raw_tags = dcmread(self.dicom_path)
        public_dict_tags:dict = {}
        for item in raw_tags:
            if "CSA" in item.name: continue
            if item.VR == "SQ":
                print("this is a sequence")
            else:
                public_dict_tags.update({item.name: item.value})
                # key, value = item.name, item.value
        return public_dict_tags
    
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
    
    @property 
    def all_tags(self):
        """
        "Public" and private/tags joined into one dictionary, to be exported as a single json file.
        """
        return {**self.public_tags, **self.private_tags}

    def convert_to_serializable(self, obj)->dict:
        """
        Fix dictionary format of headers to save them in a json file.
        """
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
        if isinstance(obj, MultiValue):
            return list(obj)  # Convert MultiValue to a list
        if isinstance(obj, PersonName):
            return str(obj)
        raise TimeoutError(f'Object of type {obj.__class__.__name__} is not JSON serializable!')
    
    def save_json(self)->None:
        """
        Save available metadata into json format.
        Currently works for syngo MR E11 only 
        """
        # define json filename
        filename = os.path.basename(self.dicom_path).split('.')[0]
        # print(self.filename)
        json_filename = 'sidecar_files/{}.json'.format(filename)
        if self.software_version == "syngo MR E11":
            # Save the simplified metadata as a JSON file
            with open(json_filename, 'w') as f:
                json.dump(self.all_tags, f, indent=4, default=self.convert_to_serializable)
        else:
            print("I don't know how to save this data to json yet :(")
