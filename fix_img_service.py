import os
import re

def fix_file(filepath, replacements):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    for old, new in replacements:
        if isinstance(old, re.Pattern):
            content = old.sub(new, content)
        else:
            content = content.replace(old, new)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_file('backend/app/services/image_service.py', [
    (re.compile(r"dicom_res = DicomService\.parse_dicom\(content\)\n                  d_meta = dicom_res\[\"metadata\"\]\n                  metadata_dict\.update\(d_meta\)"), """dicom_res = DicomService.parse_dicom(content)
                  d_meta = dicom_res["metadata"]
                  
                  # Modality mapping
                  raw_modality = d_meta.get("modality", "")
                  if raw_modality in ["CR", "DX", "XA", "RF"]:
                      d_meta["modality"] = "X-RAY"
                  elif raw_modality in ["MR"]:
                      d_meta["modality"] = "MRI"
                  elif raw_modality in ["CT"]:
                      d_meta["modality"] = "CT"
                  else:
                      d_meta["modality"] = "UNKNOWN"
                      
                  metadata_dict.update(d_meta)"""),
    (re.compile(r"\"format\": \"DICOM\" if is_dicom else \"IMAGE\",\n              \"status\": \"uploaded\","), """"format": "DICOM" if is_dicom else "IMAGE",
              "modality": "UNKNOWN",
              "status": "uploaded",""")
])
