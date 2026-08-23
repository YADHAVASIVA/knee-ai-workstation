# X-Ray Image Preprocessing Audit

**Dataset Subfolder Selected:** `kneeKL224`

## Image Properties
- **Original dimensions:** 224x224
- **Grayscale:** Yes (1-channel 'L' mode)
- **Anatomical crop:** Pre-cropped to the knee joint
- **Intensity range:** 8-bit [0, 255]

## Model Input Strategy (DenseNet121)
**Chosen Approach: OPTION A**
Convert the 1-channel grayscale image into a 3-channel RGB image by identically duplicating the grayscale values across all three channels. 

**Justification:**
DenseNet121's `ImageNet` pretrained weights expect a 3-channel input. By copying the grayscale channel 3 times, the existing pretrained spatial filters (which look for edges, textures, etc., across RGB) will respond identically as if they were observing a purely desaturated color image. This reliably preserves the initial learned representations without requiring surgical modifications to the network architecture. We will then apply standard ImageNet normalization (`mean=[0.485, 0.456, 0.406]`, `std=[0.229, 0.224, 0.225]`).

## Final Augmentation & Preprocessing (Train)
1. Convert to RGB (3 identical channels)
2. Random Horizontal Flip (since laterality is often standardized, this helps generalizability)
3. Random Rotation (-10 to +10 degrees)
4. Convert to Tensor
5. ImageNet Normalization

## Final Preprocessing (Validation/Test)
1. Convert to RGB (3 identical channels)
2. Convert to Tensor
3. ImageNet Normalization
