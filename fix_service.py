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

fix_file('backend/app/ai/segmentation/service.py', [
    (re.compile(r"def run_segmentation\(self, image_id: str\) -> SegmentationResult:\n        processed_path = "), """def run_segmentation(self, image_id: str) -> SegmentationResult:
        import json
        meta_path = os.path.join(settings.UPLOAD_DIR, f"{image_id}_meta.json")
        modality = "UNKNOWN"
        if os.path.exists(meta_path):
            with open(meta_path, "r") as f:
                meta = json.load(f)
                modality = meta.get("modality", "UNKNOWN")
                
        processed_path = """),
    (re.compile(r"mask_array = self\.model\.predict\(img_array\)"), "mask_array = self.model.predict(img_array, modality)"),
    (re.compile(r"\"medial_meniscus\": StructureResult\(\n                    detected=SegmentationClass\.MEDIAL_MENISCUS in unique_labels,\n                    confidence=None\n                \)"), """"medial_meniscus": StructureResult(
                    detected=SegmentationClass.MEDIAL_MENISCUS in unique_labels if modality == "MRI" else False,
                    confidence=None
                )""")
])
