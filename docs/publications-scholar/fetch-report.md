# Google Scholar 论文采集报告

- 作者：檀韬（Tao Tan）
- Google Scholar ID：`lLg3WRkAAAAJ`
- 数据获取时间：2026-11-22T09:41:13Z
- 采集轮次：`20261122T094058.988533Z-a52546c2`
- 原始条目数：416
- 去重后论文数：416
- CSV 审核行数：416
- 疑似重复记录数：8
- 与上次完整快照比较：0 篇旧记录

## 分页完整性

共获取 5 页；每页最多 100 条。采集在下一页不存在且末页不足 100 条时结束。SerpApi 文档说明单次最多返回 100 条，`start` 为结果偏移量。

| start | API 条数 | 数据获取时间 |
|---:|---:|---|
| 0 | 100 | 2026-11-22T09:41:07Z |
| 100 | 100 | 2026-11-22T09:41:08Z |
| 200 | 100 | 2026-11-22T09:41:10Z |
| 300 | 100 | 2026-11-22T09:41:12Z |
| 400 | 16 | 2026-11-22T09:41:13Z |

## 各年份论文数量

| 年份 | 篇数 |
|---|---:|
| 2006 | 1 |
| 2009 | 1 |
| 2011 | 1 |
| 2012 | 2 |
| 2013 | 5 |
| 2014 | 4 |
| 2015 | 4 |
| 2016 | 4 |
| 2017 | 5 |
| 2018 | 14 |
| 2019 | 18 |
| 2020 | 14 |
| 2021 | 10 |
| 2022 | 13 |
| 2023 | 51 |
| 2024 | 71 |
| 2025 | 102 |
| 2026 | 83 |
| （缺失） | 13 |

## 字段缺失情况

统计口径为去重后的 416 条论文；缺失字段保持为空，没有推测或补造。

| 字段 | 缺失数 / 论文总数 |
|---|---:|
| `title` | 0 / 416 |
| `authors` | 0 / 416 |
| `year` | 13 / 416 |
| `publication` | 16 / 416 |
| `citation_count` | 106 / 416 |
| `link` | 0 / 416 |
| `citation_id` | 0 / 416 |

## 重复记录供人工核验

按 `citation_id` 去重；相同标题和年份但不同 `citation_id` 的记录仍保留，并标记为疑似重复。CSV 包含所有原始论文条目，JSON 的 `publications` 为去重结果，`duplicate_records` 保留重复条目。

| 原因 | 标题 | 年份 | citation_id | 对照 citation_id |
|---|---|---:|---|---|
| possible_title_year_duplicate | Generative Artificial Intelligence in Medical Imaging: Foundations, Progress, and Clinical Translation | 2025 | lLg3WRkAAAAJ:EPG8bYD4jVwC | lLg3WRkAAAAJ:qe6vwMD2xtsC |
| possible_title_year_duplicate | VLA: Prior-Guided Vision-Language-Action Models via World Knowledge Variation | 2026 | lLg3WRkAAAAJ:MIg0yeAD4ggC | lLg3WRkAAAAJ:SxCCDk4iOpsC |
| possible_title_year_duplicate | BioVFM-21M: Benchmarking and Scaling Self-supervised Vision Foundation Models for Biomedical Image Analysis | 2025 | lLg3WRkAAAAJ:Xl6nMSl579sC | lLg3WRkAAAAJ:w1MjKQ0l0TYC |
| possible_title_year_duplicate | Multimodality image processing techniques for training image data generation and usage thereof for developing mono-modality image inferencing models | 2025 | lLg3WRkAAAAJ:r_AWSJRzSzQC | lLg3WRkAAAAJ:wvYxNZNCP7wC |
| possible_title_year_duplicate | Multi-layer image registration | 2024 | lLg3WRkAAAAJ:6ZxmRoH8BuwC | lLg3WRkAAAAJ:-mN3Mh-tlDkC |
| possible_title_year_duplicate | Combining machine and deep transfer learning for mediastinal lymph node evaluation in patients with lung cancer. | 2024 | lLg3WRkAAAAJ:JP7YXuLIOvAC | lLg3WRkAAAAJ:jgBuDB5drN8C |
| possible_title_year_duplicate | Is There a Difference between Paper and Electronic Chinese Signatures? | 2023 | lLg3WRkAAAAJ:ZzlSgRqYykMC | lLg3WRkAAAAJ:OcBU2YAGkTUC |
| possible_title_year_duplicate | Comprehensive deep learning-based framework for automatic organs-at-risk segmentation in head-and-neck and pelvis for MR-guided radiation therapy planning | 2023 | lLg3WRkAAAAJ:yFnVuubrUp4C | lLg3WRkAAAAJ:yqoGN6RLRZoC |

## 与前一完整快照比较

### 新增论文（416）

| 标题 | 年份 | citation_id |
|---|---:|---|
| Stand-alone artificial intelligence for breast cancer detection in mammography: comparison with 101 radiologists | 2019 | lLg3WRkAAAAJ:XiSMed-E-HIC |
| Fusionmamba: Dynamic feature enhancement for multimodal image fusion with mamba | 2024 | lLg3WRkAAAAJ:2tRrZ1ZAMYUC |
| Denoising of 3D magnetic resonance images with multi-channel residual learning of convolutional neural network | 2018 | lLg3WRkAAAAJ:1sJd4Hv_s6UC |
| Deep learning methods for lung cancer segmentation in whole-slide histopathology images—the acdc@ lunghp challenge 2019 | 2020 | lLg3WRkAAAAJ:HE397vMXCloC |
| HTC-Net: A hybrid CNN-transformer framework for medical image segmentation | 2024 | lLg3WRkAAAAJ:KbBQZpvPDL4C |
| Epileptic seizure detection in EEG signals using sparse multiscale radial basis function networks and the Fisher vector approach | 2019 | lLg3WRkAAAAJ:UxriW0iASnsC |
| An explainable longitudinal multi-modal fusion model for predicting neoadjuvant therapy response in women with breast cancer | 2024 | lLg3WRkAAAAJ:PYBJJbyH-FwC |
| Computer-aided detection of cancer in automated 3-D breast ultrasound | 2013 | lLg3WRkAAAAJ:j3f4tGmQtD8C |
| Deep learning approach to semantic segmentation in 3d point cloud intra-oral scans of teeth | 2019 | lLg3WRkAAAAJ:SP6oXDckpogC |
| Computer-aided lesion diagnosis in automated 3-D breast ultrasound using coronal spiculation | 2012 | lLg3WRkAAAAJ:e5wmG9Sq2KIC |
| TransMRSR: transformer-based self-distilled generative prior for brain MRI super-resolution | 2023 | lLg3WRkAAAAJ:IRz6iEL74y4C |
| Predicting breast cancer types on and beyond molecular level in a multi-modal fashion | 2023 | lLg3WRkAAAAJ:8d8msizDQcsC |
| Automated Detection of Cerebral Microbleeds in Patients with Traumatic Brain Injury | 2016 | lLg3WRkAAAAJ:bFI3QPDXJZMC |
| Dedicated computer-aided detection software for automated 3D breast ultrasound; an efficient tool for the radiologist in supplemental screening of women with dense breasts | 2018 | lLg3WRkAAAAJ:b0M2c_1WBrUC |
| Optimize Transfer Learning for Lung Diseases in Bronchoscopy Using a New Concept: Sequential Fine-Tuning | 2018 | lLg3WRkAAAAJ:P5F9QuxV20EC |
| Mass segmentation in automated 3-D breast ultrasound using adaptive region growing and supervised edge-based deformable model | 2017 | lLg3WRkAAAAJ:CHSYGLWDkRkC |
| Harnessing artificial intelligence for prostate cancer management | 2024 | lLg3WRkAAAAJ:jL-93Qbq4QoC |
| Improved cancer detection in automated breast ultrasound by radiologists using computer aided detection | 2017 | lLg3WRkAAAAJ:D03iK_w7-QYC |
| Radiomics and artificial intelligence in breast imaging: a survey | 2023 | lLg3WRkAAAAJ:mlAyqtXpCwEC |
| Generative Models in Medical Visual Question Answering: A Survey | 2025 | lLg3WRkAAAAJ:6_hjMsCP8ZoC |
| Computer aided detection in automated 3-D breast ultrasound images: a survey | 2020 | lLg3WRkAAAAJ:08ZZubdj9fEC |
| Prediction of molecular subtypes of breast cancer using BI-RADS features based on a “white box” machine learning approach in a multi-modal imaging setting | 2019 | lLg3WRkAAAAJ:KxtntwgDAa4C |
| Retinal artery/vein classification using genetic-search feature selection | 2018 | lLg3WRkAAAAJ:EUQCXRtRnyEC |
| Simultaneous arteriole and venule segmentation with domain-specific loss function on a new public database | 2018 | lLg3WRkAAAAJ:NhqRSupF_l8C |
| Multi-modal and multi-vendor retina image registration | 2018 | lLg3WRkAAAAJ:_xSYboBqXhAC |
| Unsupervised cerebrovascular segmentation of TOF-MRA images based on deep neural network and hidden markov random field model | 2020 | lLg3WRkAAAAJ:eflP2zaiRacC |
| Computer‐aided detection of breast cancers using Haar‐like features in automated 3D breast ultrasound | 2015 | lLg3WRkAAAAJ:k_IJM867U9cC |
| CoTrFuse: a novel framework by fusing CNN and transformer for medical image segmentation | 2023 | lLg3WRkAAAAJ:DJbcl8HfkQkC |
| Lesion segmentation in ultrasound using semi-pixel-wise cycle generative adversarial nets | 2020 | lLg3WRkAAAAJ:u9iWguZQMMsC |
| Computer-aided diagnosis of lung carcinoma using deep learning-a pilot study | 2018 | lLg3WRkAAAAJ:l7t_Zn2s7bgC |
| Synthesis-based imaging-differentiation representation learning for multi-sequence 3D/4D MRI | 2024 | lLg3WRkAAAAJ:YohjEiUPhakC |
| Fully automatic deep learning trained on limited data for carotid artery segmentation from large image volumes | 2021 | lLg3WRkAAAAJ:eMMeJKvmdy0C |
| Breast cancer detection in automated 3D breast ultrasound using iso-contours and cascaded RUSBoosts | 2017 | lLg3WRkAAAAJ:OU6Ihb5iCvQC |
| Generative Artificial Intelligence in Medical Imaging: Foundations, Progress, and Clinical Translation | 2025 | lLg3WRkAAAAJ:qe6vwMD2xtsC |
| From Gaze to Insight: Bridging Human Visual Attention and Vision Language Model Explanation for Weakly-Supervised Medical Image Segmentation | 2025 | lLg3WRkAAAAJ:QyXJ3EUuO1IC |
| PCTMF-Net: heart sound classification with parallel CNNs-transformer and second-order spectral analysis. | 2023 | lLg3WRkAAAAJ:dBIO0h50nwkC |
| Dual retrieving and ranking medical large language model with retrieval augmented generation | 2025 | lLg3WRkAAAAJ:ce2CqMG-AY4C |
| Type 2 diabetes and HbA1c are independently associated with wider retinal arterioles: the Maastricht study | 2020 | lLg3WRkAAAAJ:bnK-pcrLprsC |
| Multi-modal artificial intelligence for the combination of automated 3D breast ultrasound and mammograms in a population of women with predominantly dense breasts | 2023 | lLg3WRkAAAAJ:_axFR9aDTf0C |
| Validation of radiologists’ findings by computer-aided detection (CAD) software in breast cancer detection with automated 3D breast ultrasound: a concept study in … | 2020 | lLg3WRkAAAAJ:geHnlv5EZngC |
| Respiration monitoring for premature neonates in NICU | 2019 | lLg3WRkAAAAJ:eJXPG6dFmWUC |
| Data augmentation strategies for semi-supervised medical image segmentation | 2025 | lLg3WRkAAAAJ:MhiOAD_qIWkC |
| Evaluation of the effect of computer-aided classification of benign and malignant lesions on reader performance in automated three-dimensional breast ultrasound | 2013 | lLg3WRkAAAAJ:r0BpntZqJG4C |
| LLM-Detector: Improving AI-Generated Chinese Text Detection with Open-Source LLM Instruction Tuning | 2024 | lLg3WRkAAAAJ:artPoR2Yc-kC |
| Video-based actigraphy for monitoring wake and sleep in healthy infants: A Laboratory Study | 2019 | lLg3WRkAAAAJ:dshw04ExmUIC |
| IvyGPT: InteractiVe Chinese pathwaY language model in medical domain | 2023 | lLg3WRkAAAAJ:9c2xU6iGI7YC |
| Probabilistic kinematic model of a robotic catheter for 3D position control | 2019 | lLg3WRkAAAAJ:TaaCk18tZOkC |
| Video-based discomfort detection for infants | 2019 | lLg3WRkAAAAJ:uWQEDVKXjbEC |
| A dual stream network for tumor detection in hyperspectral images | 2019 | lLg3WRkAAAAJ:VOx2b1Wkg3QC |
| A novel framework for segmentation of small targets in medical images | 2025 | lLg3WRkAAAAJ:-7ulzOJl1JYC |
| Fine-tuning medical language models for enhanced long-contextual understanding and domain expertise | 2025 | lLg3WRkAAAAJ:zCSUwVk65WsC |
| An improved U-net architecture for simultaneous arteriole and venule segmentation in fundus image | 2018 | lLg3WRkAAAAJ:p2g8aNsByqUC |
| A fundus image dataset for intelligent retinopathy of prematurity system | 2024 | lLg3WRkAAAAJ:QD3KBmkZPeQC |
| RadioLOGIC, a healthcare model for processing electronic health records and decision-making in breast disease | 2023 | lLg3WRkAAAAJ:4vMrXwiscB8C |
| Incorporating texture features in a computer-aided breast lesion diagnosis system for automated three-dimensional breast ultrasound | 2014 | lLg3WRkAAAAJ:isC4tDSrTZIC |
| ARGA-Unet: Advanced U-net segmentation model using residual grouped convolution and attention mechanism for brain tumor MRI image segmentation | 2024 | lLg3WRkAAAAJ:WHdLCjDvYFkC |
| Knee bone and cartilage segmentation based on a 3D deep neural network using adversarial loss for prior shape constraint | 2022 | lLg3WRkAAAAJ:q3CdL3IzO_QC |
| Xiaoqing: A Q&A model for glaucoma based on LLMs | 2024 | lLg3WRkAAAAJ:sJsF-0ZLhtgC |
| Automatic and continuous discomfort detection for premature infants in a NICU using video-based motion analysis | 2019 | lLg3WRkAAAAJ:5Ul4iDaHHb8C |
| Charting the path forward: CT image quality assessment-an in-depth review | 2025 | lLg3WRkAAAAJ:6yz0xqPARnAC |
| Light-vqa: A multi-dimensional quality assessment model for low-light video enhancement | 2023 | lLg3WRkAAAAJ:4hFrxpcac9AC |
| An Explainable Deep Framework: Towards Task-Specific Fusion for Multi-to-One MRI Synthesis | 2023 | lLg3WRkAAAAJ:mNrWkgRL2YcC |
| Segmentation of malignant lesions in 3D breast ultrasound using a depth‐dependent model | 2016 | lLg3WRkAAAAJ:J_g5lzvAfSwC |
| PhysLLM: Harnessing large language models for cross-modal remote physiological sensing | 2026 | lLg3WRkAAAAJ:HJSXoJQnj-YC |
| Synthesis of Contrast-Enhanced Breast MRI Using T1-and Multi-b-Value DWI-Based Hierarchical Fusion Network with Attention Mechanism | 2023 | lLg3WRkAAAAJ:OTTXONDVkokC |
| Multi-risk factors joint prediction model for risk prediction of retinopathy of prematurity | 2024 | lLg3WRkAAAAJ:NyGDZy8z5eUC |
| MimicNet: Mimicking manual delineation of human expert for brain tumor segmentation from multimodal MRIs | 2023 | lLg3WRkAAAAJ:umqufdRvDiIC |
| Ultrasound tissue classification: a review | 2021 | lLg3WRkAAAAJ:WA5NYHcadZ8C |
| Retinal image measurements and their association with chronic kidney disease in Chinese patients with type 2 diabetes: the NCD study | 2021 | lLg3WRkAAAAJ:Mojj43d5GZwC |
| Cystoscopic Image Classification Based on Combining MLP and GA | 2020 | lLg3WRkAAAAJ:kRWSkSYxWN8C |
| Detecting discomfort in infants through facial expressions | 2019 | lLg3WRkAAAAJ:LPZeul_q3PIC |
| A multimodal vision–language model for generalizable annotation-free pathology localization | 2026 | lLg3WRkAAAAJ:qwy9JoKyICEC |
| Blenet: a bio-inspired lightweight and efficient network for left ventricle segmentation in echocardiography | 2025 | lLg3WRkAAAAJ:OBSaB-F7qqsC |
| ERNet: edge regularization network for cerebral vessel segmentation in digital subtraction angiography images | 2023 | lLg3WRkAAAAJ:nZcligLrVowC |
| Multi-modal trained artificial intelligence solution to triage chest X-ray for COVID-19 using pristine ground-truth, versus radiologists | 2022 | lLg3WRkAAAAJ:PoWvk5oyLR8C |
| IMPORTANT-Net: Integrated MRI multi-parametric increment fusion generator with attention network for synthesizing absent data | 2024 | lLg3WRkAAAAJ:LgRImbQfgY4C |
| Chest wall segmentation in automated 3D breast ultrasound scans | 2013 | lLg3WRkAAAAJ:RHpTSmoSYBkC |
| Uniemo: Unifying emotional understanding and generation with learnable expert queries | 2026 | lLg3WRkAAAAJ:YB4bud6kWLwC |
| Ordinal Learning: Longitudinal Attention Alignment Model for Predicting Time to Future Breast Cancer Events from Mammograms | 2024 | lLg3WRkAAAAJ:nRpfm8aw39MC |
| Focus-RCNet: a lightweight recyclable waste classification algorithm based on focus and knowledge distillation | 2023 | lLg3WRkAAAAJ:fFSKOagxvKUC |
| DisAsymNet: Disentanglement of Asymmetrical Abnormality on Bilateral Mammograms Using Self-adversarial Learning | 2023 | lLg3WRkAAAAJ:IUKN3-7HHlwC |
| Transferring from ex-vivo to in-vivo: Instrument Localization in 3D Cardiac Ultrasound Using Pyramid-UNet with Hybrid Loss | 2019 | lLg3WRkAAAAJ:4fKUyHm3Qg0C |
| 2.75 D: Boosting learning by representing 3D Medical imaging to 2D features for small data | 2023 | lLg3WRkAAAAJ:_FM0Bhl9EiAC |
| Metabolic-associated fatty liver disease and the risk of cardiovascular disease | 2023 | lLg3WRkAAAAJ:ClCfbGk0d_YC |
| Optimal threshold in low-dose CT quantification of emphysema | 2020 | lLg3WRkAAAAJ:olpn-zPbct0C |
| Automatic corneal nerve fiber segmentation and geometric biomarker quantification | 2020 | lLg3WRkAAAAJ:V3AGJWp-ZtQC |
| Local to global learning: Gradually adding classes for training deep neural networks | 2019 | lLg3WRkAAAAJ:Tiz5es2fbqcC |
| Pcdal: A perturbation consistency-driven active learning approach for medical image segmentation and classification | 2025 | lLg3WRkAAAAJ:2VqYfGB8ITEC |
| MLC: Multi-level consistency learning for semi-supervised left atrium segmentation | 2024 | lLg3WRkAAAAJ:5MTHONV0fEkC |
| Multidrug-resistant infection in COVID-19 patients: A meta-analysis | 2022 | lLg3WRkAAAAJ:5qfkUJPXOUwC |
| Generative Artificial Intelligence in Medical Imaging: Foundations, Progress, and Clinical Translation | 2025 | lLg3WRkAAAAJ:EPG8bYD4jVwC |
| Bootstrapping BI-RADS classification using large language models and transformers in breast magnetic resonance imaging reports | 2025 | lLg3WRkAAAAJ:LXmCCkuhhTsC |
| Sonographic phenotypes of molecular subtypes of invasive ductal cancer in automated 3-D breast ultrasound | 2017 | lLg3WRkAAAAJ:abG-DnoFyZgC |
| UniMRISegNet: Universal 3D Network for Various Organs and Cancers Segmentation on Multi-Sequence MRI | 2024 | lLg3WRkAAAAJ:L1USKYWJimsC |
| A deep learning-based radiomics model for predicting lymph node status from lung adenocarcinoma | 2024 | lLg3WRkAAAAJ:wMgC3FpKEyYC |
| LYSTO: The lymphocyte assessment hackathon and benchmark dataset | 2023 | lLg3WRkAAAAJ:lvd772isFD0C |
| Comprehensive deep learning-based framework for automatic organs-at-risk segmentation in head-and-neck and pelvis for MR-guided radiation therapy planning | 2023 | lLg3WRkAAAAJ:yqoGN6RLRZoC |
| Predicting up to 10 year breast cancer risk using longitudinal mammographic screening history | 2023 | lLg3WRkAAAAJ:WJVC3Jt7v1AC |
| FedHNR: Federated hierarchical resilient learning for echocardiogram segmentation with annotation noise | 2025 | lLg3WRkAAAAJ:Ade32sEp0pkC |
| Dynamic multimodal segmentation selection and fusion | 2025 | lLg3WRkAAAAJ:F9fV5C73w3QC |
| Multi-modal longitudinal representation learning for predicting neoadjuvant therapy response in breast cancer treatment | 2025 | lLg3WRkAAAAJ:WC9gN4BGCRcC |
| Synthetic training data generation for improved machine learning model generalizability | 2023 | lLg3WRkAAAAJ:Dip1O2bNi0gC |
| Application of ultrasonic dual-mode artificially intelligent architecture in assisting radiologists with different diagnostic levels on breast masses classification | 2021 | lLg3WRkAAAAJ:gsN89kCJA0AC |
| Effectiveness and clinical impact of using deep learning for first-trimester fetal ultrasound image quality auditing | 2025 | lLg3WRkAAAAJ:HGTzPopzzJcC |
| CLP-Net: an advanced artificial intelligence technique for localizing standard planes of cleft lip and palate by three-dimensional ultrasound in the first trimester | 2025 | lLg3WRkAAAAJ:MAUkC_7iAq8C |
| LightR-YOLOv5: A compact rotating detector for SARS-CoV-2 antigen-detection rapid diagnostic test results | 2023 | lLg3WRkAAAAJ:GtLg2Ama23sC |
| Olfactory dysfunction after COVID‐19: metanalysis reveals persistence in one-third of patients 6 months after initial infection | 2023 | lLg3WRkAAAAJ:9pM33mqn1YgC |
| Cancer Detection in Mass Spectrometry Imaging Data by Recurrent Neural Networks | 2019 | lLg3WRkAAAAJ:tOudhMTPpwUC |
| Multimodality image processing techniques for training image data generation and usage thereof for developing mono-modality image inferencing models | 2023 | lLg3WRkAAAAJ:foquWX3nUaYC |
| Prompt mechanisms in medical imaging: a comprehensive survey | 2026 | lLg3WRkAAAAJ:oi2SiIJ9l4AC |
| FetalFlex: Anatomy-guided diffusion model for flexible control on fetal ultrasound image synthesis | 2025 | lLg3WRkAAAAJ:KaMxkj08jr0C |
| Revolutionizing HER-2 assessment: multidimensional radiomics in breast cancer diagnosis | 2025 | lLg3WRkAAAAJ:q-HalDI95KYC |
| Associations between metabolic dysfunction-associated fatty liver disease and atherosclerotic cardiovascular disease | 2024 | lLg3WRkAAAAJ:lgwcVrK6X84C |
| Dual-decoder consistency via pseudo-labels guided data augmentation for semi-supervised medical image segmentation | 2023 | lLg3WRkAAAAJ:HtS1dXgVpQUC |
| From Local to Global: A Graph Framework for Retinal Artery/Vein Classification | 2020 | lLg3WRkAAAAJ:t6usbXjVLHcC |
| Automated segmentation of lesions in ultrasound using semi-pixel-wise cycle generative adversarial nets | 2019 | lLg3WRkAAAAJ:isU91gLudPYC |
| Can Jev Judge Radiology Reports? Evaluating a System One Model for Clinical Factuality | 2026 | lLg3WRkAAAAJ:c59VksA5Vz4C |
| TRRG: Towards Truthful Radiology Report Generation With Cross-Modal Disease Clue Enhanced Large Language Models | 2025 | lLg3WRkAAAAJ:SnGPuo6Feq8C |
| Moedit: On learning quantity perception for multi-object image editing | 2025 | lLg3WRkAAAAJ:1Ye0OR6EYb4C |
| Multimodal Cross Global Learnable Attention Network for MR images denoising with arbitrary modal missing | 2025 | lLg3WRkAAAAJ:LPtt_HFRSbwC |
| Multi-iteration active learning for the composition design of potassium–sodium niobate ceramics with enhanced piezoelectric coefficient | 2024 | lLg3WRkAAAAJ:7H_MAutzIkAC |
| UniUSNet: A Promptable Framework for Universal Ultrasound Disease Prediction and Tissue Segmentation | 2024 | lLg3WRkAAAAJ:1yWc8FF-_SYC |
| BSANet: Boundary-aware and scale-aggregation networks for CMR image segmentation | 2024 | lLg3WRkAAAAJ:ALROH1vI_8AC |
| Revolutionizing breast cancer Ki-67 diagnosis: ultrasound radiomics and fully connected neural networks (FCNN) combination method | 2024 | lLg3WRkAAAAJ:CdxZDUztZiMC |
| Unsupervised cross-modality domain adaptation for vestibular schwannoma segmentation and koos grade prediction based on semi-supervised contrastive learning | 2022 | lLg3WRkAAAAJ:FPJr55Dyh1AC |
| SUGAR: Learning Skeleton Representation with Visual-Motion Knowledge for Action Recognition | 2026 | lLg3WRkAAAAJ:A8cqit5AE6sC |
| Phase-net: Physics-grounded harmonic attention system for efficient remote photoplethysmography measurement | 2026 | lLg3WRkAAAAJ:65Yg0jNCQDAC |
| An orchestration learning framework for ultrasound imaging: Prompt-guided hyper-perception and attention-matching downstream synchronization | 2025 | lLg3WRkAAAAJ:kWvqk_afx_IC |
| Diabetes mellitus and pancreatic cancer: investigation of causal pathways through mendelian randomization analysis | 2023 | lLg3WRkAAAAJ:nVrZBo8bIpAC |
| Cystoscopic Image Classification by Unsupervised Feature Learning and Fusion of Classifiers | 2021 | lLg3WRkAAAAJ:lmc2jWPfTJgC |
| Classification of breast lesions in automated 3D breast ultrasound | 2011 | lLg3WRkAAAAJ:R3hNpaxXUhUC |
| Dynamic mask stitching-guided region consistency for semi-supervised 3D medical image segmentation | 2025 | lLg3WRkAAAAJ:NDuN12AVoxsC |
| Predicting short-to long-term breast cancer risk from longitudinal mammographic screening history | 2025 | lLg3WRkAAAAJ:SIv7DqKytYAC |
| C2MAOT: Cross-modal Complementary Masked Autoencoder with Optimal Transport for Cancer Segmentation in PET-CT Images | 2025 | lLg3WRkAAAAJ:IsPWOBWtZBwC |
| All-in-one medical image-to-image translation | 2025 | lLg3WRkAAAAJ:5bg8sr1QxYwC |
| MSAByNet: A multiscale subtraction attention network framework based on Bayesian loss for medical image segmentation | 2025 | lLg3WRkAAAAJ:hsZV8lGYWTMC |
| Automatic Segmentation of Intracranial Hemorrhage in Computed Tomography Scans with Convolution Neural Networks | 2024 | lLg3WRkAAAAJ:v1_lew4L6wgC |
| System and methods for inferring thickness of anatomical classes of interest in two-dimensional medical images using deep neural networks | 2022 | lLg3WRkAAAAJ:Ug5p-4gJ2f0C |
| Classification of breast mass in 3D ultrasound images with annotations based on convolutional neural networks | 2018 | lLg3WRkAAAAJ:K3LRdlH-MEoC |
| Multi-omics deep learning improves FDG PET-CT-based long-term prognostication of breast cancer | 2026 | lLg3WRkAAAAJ:wE-fMHVdjMkC |
| Pseudo Label-Guided Data Fusion and output consistency for semi-supervised medical image segmentation | 2025 | lLg3WRkAAAAJ:a3BOlSfXSfwC |
| MedIQA: A Scalable Foundation Model for Prompt-Driven Medical Image Quality Assessment | 2025 | lLg3WRkAAAAJ:kF1pexMAQbMC |
| A Diffusion-Driven Temporal Super-Resolution and Spatial Consistency Enhancement Framework for 4D MRI imaging | 2025 | lLg3WRkAAAAJ:3bvyWxjaHKcC |
| DpDNet: An Dual-Prompt-Driven Network for Universal PET-CT Segmentation | 2025 | lLg3WRkAAAAJ:w0F2JDEymm0C |
| Exploring personalized neoadjuvant therapy selection strategies in breast cancer: an explainable multi-modal response model | 2025 | lLg3WRkAAAAJ:ziOE8S1-AIUC |
| Explainable and controllable motion curve guided cardiac ultrasound video generation | 2024 | lLg3WRkAAAAJ:wKETBy42zhYC |
| LUCMT: Learnable under-sampling and reconstructed network with cross multi-head attention transformer for accelerating MR image reconstruction | 2024 | lLg3WRkAAAAJ:PyEswDtIyv0C |
| Chest CT-IQA: A multi-task model for chest CT image quality assessment and classification | 2024 | lLg3WRkAAAAJ:1lhNe0rCu4AC |
| Precision dose prediction for breast cancer patients undergoing IMRT: The Swin-UMamba-Channel Model | 2024 | lLg3WRkAAAAJ:CaZNVDsoPx4C |
| DLW-YOLO: Improved YOLO for Student Behaviour Recognition | 2024 | lLg3WRkAAAAJ:k_7cPK9k7w8C |
| A Parameterized Generative Adversarial Network Using Cyclic Projection for Explainable Medical Image Classifications | 2024 | lLg3WRkAAAAJ:OP4eGU-M3BUC |
| Exploring the causal association between rheumatoid arthritis and the risk of cervical cancer: a two-sample Mendelian randomization study | 2024 | lLg3WRkAAAAJ:4xDN1ZYqzskC |
| Deep-Learning-based Segmentation of Organs-at-Risk in the Head for MR-assisted Radiation Therapy Planning. | 2021 | lLg3WRkAAAAJ:i2xiXl-TujoC |
| Detection of breast cancer in automated 3D breast ultrasound | 2012 | lLg3WRkAAAAJ:_Qo2XoVZTnwC |
| From noisy labels to intrinsic structure: A geometric-structural dual-guided framework for noise-robust medical image segmentation | 2026 | lLg3WRkAAAAJ:An6A6Jpfc1oC |
| UltraTwin: Towards Cardiac Anatomical Twin Generation from Multi-view 2D Ultrasound | 2025 | lLg3WRkAAAAJ:JTqpx9DYBaYC |
| Synergy-Guided Regional Supervision of Pseudo Labels for Semi-Supervised Medical Image Segmentation | 2025 | lLg3WRkAAAAJ:jU7OWUQzBzMC |
| Dual-uncertainty guided multimodal MRI-based visual pathway extraction | 2025 | lLg3WRkAAAAJ:3NQIlFlcGxIC |
| An end-to-end multi-task deep learning framework for bronchoscopy image classification: R. Setayeshi et al. | 2024 | lLg3WRkAAAAJ:XUvXOeBm_78C |
| WaveFrSnow: Comprehensive perception wavelet transform frequency separation transformer for image snow removal | 2024 | lLg3WRkAAAAJ:43bX7VzcjpAC |
| Scribblevs: scribble-supervised medical image segmentation via dynamic competitive pseudo label selection | 2024 | lLg3WRkAAAAJ:CB2v5VPnA5kC |
| Enhancing test time adaptation with few-shot guidance | 2024 | lLg3WRkAAAAJ:mUJArPsKIAAC |
| 3mt-net: a multi-modal multi-task model for breast cancer and pathological subtype classification based on a multicenter study | 2024 | lLg3WRkAAAAJ:LdasjJ6CEcoC |
| EfficientNet-YOLOv5: Improved YOLOv5 Based on EfficientNet Backbone for Object Detection on Marine Microalgae | 2022 | lLg3WRkAAAAJ:HIFyuExEbWQC |
| Image harmonization for deep learning model optimization | 2021 | lLg3WRkAAAAJ:SpbeaW3--B0C |
| Cystoscopy image classification using deep convolutional neural networks | 2019 | lLg3WRkAAAAJ:5ugPr518TE4C |
| TF-LLM: Enhanced Time Series Analysis with Time-Frequency Large Language Models | 2026 | lLg3WRkAAAAJ:L_l9e5I586QC |
| Diagnostic Performance of Universal-Learning Ultrasound AI Across Multiple Organs and Tasks: the UUSIC25 Challenge | 2025 | lLg3WRkAAAAJ:2v_ZtQDX9iAC |
| All-in-One Multi-Organ Segmentation in 3D CT Images via Self-Supervised and Cross-Dataset Learning | 2025 | lLg3WRkAAAAJ:sszUF3NjhM4C |
| A deep learning model fusion algorithm for the diagnosis of gastric Mucosa-associated lymphoid tissue lymphoma | 2024 | lLg3WRkAAAAJ:bKqednn6t2AC |
| Reinvestigating the performance of artificial intelligence classification algorithms on COVID-19 X-Ray and CT images | 2024 | lLg3WRkAAAAJ:AHdEip9mkN0C |
| Controllable Deep Learning Denoising Model for Ultrasound Images Using Synthetic Noisy Image | 2023 | lLg3WRkAAAAJ:5icHVeHT4IsC |
| GENERATING MULTIMODAL TRAINING DATA COHORTS TAILORED TO SPECIFIC CLINICAL MACHINE LEARNING (ML) MODEL INFERENCING TASKS | 2023 | lLg3WRkAAAAJ:rmuvC79q63oC |
| RGA-Unet: An improved U-net segmentation model based on residual grouped convolution and convolutional block attention module for brain tumor MRI image segmentation | 2022 | lLg3WRkAAAAJ:PVjk1bu6vJQC |
| FOR COVID19 | 2020 | lLg3WRkAAAAJ:HbR8gkJAVGIC |
| VLA: Prior-Guided Vision-Language-Action Models via World Knowledge Variation | 2026 | lLg3WRkAAAAJ:SxCCDk4iOpsC |
| Visualizing Radiologic Connections: An Explainable Coarse-to-Fine Foundation Model with Multiview Mammograms and Associated Reports | 2025 | lLg3WRkAAAAJ:8Xgff_V0N9gC |
| Mammo-AGE: deep learning estimation of breast age from mammograms | 2025 | lLg3WRkAAAAJ:DyXnQzXoVgIC |
| Tumor Segmentation with Heterogeneity Clustering in Non-Contrast Breast MRI | 2025 | lLg3WRkAAAAJ:QUX0mv85b1cC |
| Distance guided generative adversarial network for explainable medical image classifications | 2024 | lLg3WRkAAAAJ:_OXeSy2IsFwC |
| To raise or not to raise: The autonomous learning rate question | 2024 | lLg3WRkAAAAJ:xtoqd-5pKcoC |
| Multimodal Breast MRI Language-Image Pretraining (MLIP): An Exploration of a Breast MRI Foundation Model | 2024 | lLg3WRkAAAAJ:rHJHxKgnXwkC |
| Improving Neoadjuvant Therapy Response Prediction by Integrating Longitudinal Mammogram Generation with Cross-Modal Radiological Reports: A Vision-Language Alignment-Guided Model | 2024 | lLg3WRkAAAAJ:j7_hQOaDUrUC |
| Non-Adversarial Learning: Vector-Quantized Common Latent Space for Multi-Sequence MRI | 2024 | lLg3WRkAAAAJ:ubry08Y2EpUC |
| Significance of N6-methyladenosine RNA methylation regulators in diagnosis and subtype classification of primary Sjögren’s syndrome | 2024 | lLg3WRkAAAAJ:vDZJ-YLwNdEC |
| Artificial intelligence-based medical image automatic diagnosis and prognosis prediction | 2023 | lLg3WRkAAAAJ:HtEfBTGE9r8C |
| Improved fully convolutional neuron networks on small retinal vessel segmentation using local phase as attention | 2023 | lLg3WRkAAAAJ:kh2fBNsKQNwC |
| Pristine annotations-based multi-modal trained artificial intelligence solution to triage chest x-ray for covid-19 | 2021 | lLg3WRkAAAAJ:-FonjvnnhkoC |
| Automated 3D breast ultrasound image analysis | 2014 | lLg3WRkAAAAJ:ruyezt5ZtCIC |
| VLA: Prior-Guided Vision-Language-Action Models via World Knowledge Variation | 2026 | lLg3WRkAAAAJ:MIg0yeAD4ggC |
| A roadmap for medical large language models: a review of foundations, applications, and challenges | 2026 | lLg3WRkAAAAJ:t-hv7AR41mYC |
| Mambacontrol: Anatomy graph-enhanced mamba controlnet with fourier refinement for diffusion-based disease trajectory prediction | 2025 | lLg3WRkAAAAJ:RoXSNcbkSzsC |
| CVFSNet: A Cross View Fusion Scoring Network for end-to-end mTICI scoring | 2025 | lLg3WRkAAAAJ:DBa1UEJaJKAC |
| Enhancing fetal ultrasound image quality assessment with multi-scale fusion and clustering-based optimization | 2025 | lLg3WRkAAAAJ:WC23djZS0W4C |
| Methods and systems for image registration | 2024 | lLg3WRkAAAAJ:_5tno0g5mFcC |
| Aurora: Activating Chinese chat capability for Mixtral-8x7B sparse Mixture-of-Experts through Instruction-Tuning | 2023 | lLg3WRkAAAAJ:8xutWZnSdmoC |
| Ultrasonic evaluation of fetal lung development using deep learning with graph | 2023 | lLg3WRkAAAAJ:anf4URPfarAC |
| A fully automated pipeline of extracting biomarkers to quantify vascular changes in retina-related diseases | 2019 | lLg3WRkAAAAJ:nb7KW1ujOQ8C |
| Virtual Museums and Active Learning: Evidence from a Technology-Mediated Intervention | 2026 | lLg3WRkAAAAJ:CNPyR2KL9-0C |
| Implicit Neural Representation-Based MRI Reconstruction Method with Sensitivity Map Constraints | 2026 | lLg3WRkAAAAJ:1DsIQWDZLl8C |
| Anatomy-guided Prompting with Cross-Modal Self-Alignment for Whole-body PET-CT Breast Cancer Segmentation | 2026 | lLg3WRkAAAAJ:X9ykpCP0fEIC |
| Less is More: Efficient PET/CT Segmentation and Multimodal Prediction of Recurrence-Free Survival and HPV Status in Head and Neck Cancer | 2026 | lLg3WRkAAAAJ:kJDgFkosVoMC |
| Parallel Multimodal Language Model: Enhanced Breast Nodule Diagnosis through Parallel Multimodal Representations and Large Language Models | 2026 | lLg3WRkAAAAJ:raTqNPD5sRQC |
| SAMASK-CLTR: A Spatial-Aware Mask Guided Learning Model for Benign and Malignant Tumor Classification in ABUS | 2025 | lLg3WRkAAAAJ:PkcyUWeTMh0C |
| ADAptation: Reconstruction-based Unsupervised Active Learning for Breast Ultrasound Diagnosis | 2025 | lLg3WRkAAAAJ:F2UWTTQJPOcC |
| Self-Adaptive Illumination Enhancement for Neonatal Remote Physiological Measurement in NICUs | 2025 | lLg3WRkAAAAJ:2l5NCbZemmgC |
| VariMix: A variety-guided data mixing framework for explainable medical image classifications | 2025 | lLg3WRkAAAAJ:BrOSOlqYqPUC |
| A universal parameter-efficient fine-tuning approach for stereo image super-resolution | 2025 | lLg3WRkAAAAJ:jE2MZjpN3IcC |
| A novel heart rate estimation framework with self-correcting face detection for Neonatal Intensive Care Unit | 2024 | lLg3WRkAAAAJ:7wO8s98CvbsC |
| Dose prediction for cervical cancer in radiotherapy based on the beam channel generative adversarial network | 2024 | lLg3WRkAAAAJ:7BrZ7Jt4UNcC |
| Quantification of Hypsarrhythmia in Infantile Spasmatic EEG: A Large Cohort Study | 2024 | lLg3WRkAAAAJ:u-coK7KVo8oC |
| Mass Segmentation in Automated 3-D Breast Ultrasound Using Dual-Path U-net | 2021 | lLg3WRkAAAAJ:k8Z6L05lTy4C |
| Image quality in automated breast ultrasound images: a preliminary study for the development of automated image quality assessment | 2013 | lLg3WRkAAAAJ:maZDTaKrznsC |
| Finding lesion correspondences in different views of automated 3D breast ultrasound | 2013 | lLg3WRkAAAAJ:4JMBOYKVnBMC |
| An Efficient Frequency-Aware Network with Local-Global Dynamics Fusion for Memory-Constrained Clinical Medical Image Classification | 2026 | lLg3WRkAAAAJ:s9ia6_kGH2AC |
| Tumor-preserving Deformable Registration of Longitudinal DCE Breast MRI during Neoadjuvant Chemotherapy | 2026 | lLg3WRkAAAAJ:KWzIFqRkAKkC |
| Synergistic perception: Fusing expert knowledge and foundation models for semi-supervised mammogram segmentation | 2026 | lLg3WRkAAAAJ:SGW5VrABaM0C |
| SGAFNet: Robust brain tumor segmentation via learnable sequence-guided adaptive fusion in available MRI acquisitions | 2026 | lLg3WRkAAAAJ:v6i8RKmR8ToC |
| Interpretable Machine Learning for the Design of (K, Na)NbO3-Based Piezoceramics Using Combinatorial and Knowledge-Embedded Descriptors | 2025 | lLg3WRkAAAAJ:aIdbFUkbNIkC |
| AI in breast imaging: A systematic review of reader studies evaluating design, performance, and clinical impact | 2025 | lLg3WRkAAAAJ:QsaTk4IG4EwC |
| BioVFM-21M: Benchmarking and Scaling Self-supervised Vision Foundation Models for Biomedical Image Analysis | 2025 | lLg3WRkAAAAJ:w1MjKQ0l0TYC |
| Bi-branch bidirectional coupled interaction fusion network for multi-retinal diseases diagnosis | 2025 | lLg3WRkAAAAJ:HhcuHIWmDEUC |
| Training Set Diversity: A Key Factor in AI-Driven Breast Ultrasound Classification | 2025 | lLg3WRkAAAAJ:UuEBAcK4md4C |
| Advancing early detection of sepsis with physiological variable interactions and temporal contrastive learning in critical care | 2025 | lLg3WRkAAAAJ:Dem6FJhTUoYC |
| Comprehensive Mendelian randomization analysis of low-density lipoprotein cholesterol and multiple cancers | 2024 | lLg3WRkAAAAJ:prdVHNxh-e8C |
| DuEU-Net: Dual Encoder UNet with Modality-Agnostic Training for PET-CT Multi-modal Organ and Lesion Segmentation | 2024 | lLg3WRkAAAAJ:SjuI4pbJlxcC |
| Benchmarking Machine Learning Algorithms for Epilepsy Detection on Multi-Age Datasets | 2024 | lLg3WRkAAAAJ:BzfGm06jWhQC |
| Predicting the risk of primary Sjögren's syndrome with key N7-methylguanosine-related genes: A novel XGBoost model | 2024 | lLg3WRkAAAAJ:uDGL6kOW6j0C |
| To deform or not: treatment-aware longitudinal registration for breast DCE-MRI during neoadjuvant chemotherapy via unsupervised keypoints detection | 2024 | lLg3WRkAAAAJ:Aul-kAQHnToC |
| Visualize what you learn: a well-explainable joint-learning framework based on multi-view mammograms and associated reports | 2023 | lLg3WRkAAAAJ:DUooU5lO8OsC |
| Current Status, Prospect and Bottleneck of Ultrasound AI Development: A Systemic Review. | 2023 | lLg3WRkAAAAJ:0izLItjtcgwC |
| Double-Camera Fusion System for Animal-Position Awareness in Farming Pens | 2022 | lLg3WRkAAAAJ:hCrLmN-GePgC |
| 基于卷积神经网络和多信息融合的三维乳腺超声分类方法 | 2018 | lLg3WRkAAAAJ:0N-VGjzr574C |
| Novel morphological features for non-mass-like breast lesion classification on DCE-MRI | 2016 | lLg3WRkAAAAJ:g5m5HwL7SMYC |
| Automated linking of suspicious findings between automated 3D breast ultrasound volumes | 2016 | lLg3WRkAAAAJ:O3NaXMp0MMsC |
| Automatic nipple detection on 3D images of an automated breast ultrasound system (ABUS) | 2014 | lLg3WRkAAAAJ:TFP_iSt0sucC |
| Leveraging modality-guided pre-training for dual-prompt-driven multi-cancer PET-CT segmentation | 2026 | lLg3WRkAAAAJ:BJrgspguQaEC |
| UKAN+: Enhancing medical image segmentation via fusion attention with Kolmogorov-Arnold Networks | 2026 | lLg3WRkAAAAJ:D_tqNUsBuKoC |
| Adaptive multi-teacher knowledge distillation framework with foundation models for medical image analysis | 2026 | lLg3WRkAAAAJ:z6xuaG2dYH0C |
| MOTDNet: Multi Organ Task Decoupling Network for Cell Segmentation | 2026 | lLg3WRkAAAAJ:__bU50VfleQC |
| Incorporating global-local tissue changes to predict future breast cancer from longitudinal screening mammograms | 2026 | lLg3WRkAAAAJ:qE4H1tSSYIIC |
| FLOW: Optimal Transport-Driven Feature Warping for Generalized Remote Physiological Measurement | 2026 | lLg3WRkAAAAJ:_AeoHAGD03cC |
| UA-MAE: An Uncertainty-Aware Masked Autoencoder for Breast Lesion Segmentation in Ultrasound Images | 2025 | lLg3WRkAAAAJ:1tZ8xJnm2c8C |
| SABPI-Net: A Novel Structure-Aware Network for Accurate and Domain-Invariant Retinopathy of Prematurity Diagnosis | 2025 | lLg3WRkAAAAJ:rbm3iO8VlycC |
| Paired Image Generation with Diffusion-Guided Diffusion Models | 2025 | lLg3WRkAAAAJ:TlpoogIpr_IC |
| Synthetizing SWI from 3T to 7T by generative diffusion network for deep medullary veins visualization | 2025 | lLg3WRkAAAAJ:pS0ncopqnHgC |
| Singular value decomposition based under‐sampling pattern optimization for MRI reconstruction | 2025 | lLg3WRkAAAAJ:-jrNzM816MMC |
| CMMIQA: a prompt-driven cross-modality multi-organ medical image quality assessment model | 2025 | lLg3WRkAAAAJ:-95Q15plzcUC |
| MSAN-Net: An End-to-End Multi-Scale Attention Network for Universal Industrial Defect Detection | 2025 | lLg3WRkAAAAJ:VN7nJs4JPk0C |
| Auto-detection of hypsarrhythmia eeg in west syndrome by dedicated feature fusion and machine learning | 2025 | lLg3WRkAAAAJ:mKu_rENv82IC |
| Artificial intelligence-based dual energy x-ray image motion correction training method and system | 2025 | lLg3WRkAAAAJ:0CzhzZyukY4C |
| Parameter map guided explainable segmentation framework for breast cancer using amide proton transfer weighted imaging | 2025 | lLg3WRkAAAAJ:yxmsSjX2EkcC |
| DiffSteISR: Harnessing diffusion prior for superior real-world stereo image super-resolution | 2025 | lLg3WRkAAAAJ:cK4Rrx0J3m0C |
| Variational Field Constraint Learning for Degree of Coronary Artery Ischemia Assessment | 2024 | lLg3WRkAAAAJ:FiytvqdAVhgC |
| Automatic detection of breast lesions in automated 3D breast ultrasound with cross-organ transfer learning | 2024 | lLg3WRkAAAAJ:1taIhTC69MYC |
| Light mixed‐supervised segmentation for 3D medical image data | 2024 | lLg3WRkAAAAJ:yMeIxYmEMEAC |
| Is There a Difference between Paper and Electronic Chinese Signatures? | 2023 | lLg3WRkAAAAJ:OcBU2YAGkTUC |
| Predicting long term breast cancer risk using longitudinal mammographic screening history | 2023 | lLg3WRkAAAAJ:OR75R8vi5nAC |
| Few-Shot Image Semantic Segmentation based on Contextual Information Encoding Strategy | 2023 | lLg3WRkAAAAJ:fbc8zXXH2BUC |
| Synthesis of Contrast-Enhanced Breast MRI Using Multi-b-Value DWI-based Hierarchical Fusion Network with Attention Mechanism | 2023 | lLg3WRkAAAAJ:BJbdYPG6LGMC |
| Reduced plasma cholesterol in Plasmodium falciparum infection: A meta-analysis | 2023 | lLg3WRkAAAAJ:NXb4pA-qfm4C |
| Joint conditional generative adversarial networks for eyelash artifact removal in ultra-wide-field fundus images | 2023 | lLg3WRkAAAAJ:a9-T7VOCCH8C |
| IMPORTANT-Net: Integrated MRI Multi-Parameter Reinforcement Fusion Generator with Attention Network for Synthesizing Absent Data | 2023 | lLg3WRkAAAAJ:4fGpz3EwCPoC |
| Automated discomfort detection for premature infants in NICU using time-frequency feature-images and CNNs | 2020 | lLg3WRkAAAAJ:BrmTIyaxlBUC |
| 2.75 D convolutional neural network for pulmonary nodule classification in chest CT | 2020 | lLg3WRkAAAAJ:mvPsJ3kp5DgC |
| Chest-wall segmentation in automated 3D breast ultrasound images using thoracic volume classification | 2014 | lLg3WRkAAAAJ:RGFaLdJalmkC |
| Hippocampus Region Segmentation for Alzheimer’s Disease Detection | 2009 | lLg3WRkAAAAJ:8k81kl-MbHgC |
| 医科生学习素质在年级与性别上的差异研究 | 2006 | lLg3WRkAAAAJ:XvxMoLDsR5gC |
| PW-GAN: Pseudo-Warping Field Guided GAN for Unsupervised Denoising of Fetal Brain MRI Images | 2026 | lLg3WRkAAAAJ:wLxue7F8ec0C |
| Conditional diffusion models for high-fidelity synthetic CT generation from CBCT in nasopharyngeal carcinoma adaptive radiotherapy: a multi-center study | 2026 | lLg3WRkAAAAJ:s85pQhAUCrAC |
| ClinRAG-GRAPH: Clinical-Prior Retrieval-Augmented Graph Model with Domain Adversarial Learning for Breast pCR Prediction | 2026 | lLg3WRkAAAAJ:YTuZlYwrTOUC |
| Multi-task Specialized Expert Model for Hierarchical Aspect-based Sentiment Analysis in Consumer Healthcare | 2026 | lLg3WRkAAAAJ:BmWJbWwHJAwC |
| SemanticST: Semantics-enhanced Spatio-Temporal Modeling for Ejection Fraction Estimation in Echocardiography | 2026 | lLg3WRkAAAAJ:RtRctb2lSbAC |
| Multi-modal segment anything model (mmSAM) for tumor segmentation in multi-tracer oncologic PET/CT | 2026 | lLg3WRkAAAAJ:hvmnpdAuIbkC |
| HiFi-Mesh: High-Fidelity Efficient 3D Mesh Generation via Compact Autoregressive Dependence | 2026 | lLg3WRkAAAAJ:-yGd096yOn8C |
| LUMIN: A Longitudinal Multi-modal Knowledge Decomposition Network for Predicting Breast Cancer Recurrence | 2026 | lLg3WRkAAAAJ:c1e4I3QdEKYC |
| PhysVLM: Vision-language Model for Generalizable Multi-task Remote Physiological Measurement | 2026 | lLg3WRkAAAAJ:-6RzNnnwWf8C |
| M SegNet: A Multi-Modal and Multi-Branch Framework for Nasopharyngeal Carcinoma Segmentation in Radiotherapy Planning | 2026 | lLg3WRkAAAAJ:ghEM2AJqZyQC |
| Vision-Language Semantic Guidance for Ejection Fraction Assessment in Echocardiography | 2025 | lLg3WRkAAAAJ:eAlLMO4JVmQC |
| Grad-MTSeg: Mitigating Multi-Task Gradient Conflicts via Hierarchical Gradient Optimization for NPC Radiotherapy Delineation | 2025 | lLg3WRkAAAAJ:RJOyoaXV5v8C |
| Tree-Diffusion: Octree-Based Conditional Diffusion Model for Small Bowel Skeleton Generation with Geometric Direction Modeling | 2025 | lLg3WRkAAAAJ:0aBXIfxlw9sC |
| Enhancing breast cancer diagnosis: non-invasive prediction of MKI-67 (Ki67) expression using ultrasound images | 2025 | lLg3WRkAAAAJ:Xz60mAmATU4C |
| MRICombo: a deep-learning-based framework for universal volume segmentation, grading-staging, and malignancy detection across heterogeneous MRI | 2025 | lLg3WRkAAAAJ:UmS_249rOGwC |
| Multi-Granularity Query Network With Adaptive Category Feature Embedding for Behavior Recognition | 2025 | lLg3WRkAAAAJ:27LrP4qxOz0C |
| RefineNet: Elevating Medical Foundation Models Through Quality-Centric Data Curation by MLLM-Annotated Proxy Distillation | 2025 | lLg3WRkAAAAJ:69ZgNCALVd0C |
| HRMamba: Fusing Luminance Information for Remote Physiological Measurement in Varied Lighting Conditions | 2025 | lLg3WRkAAAAJ:DrR-2ekChdkC |
| Conditional Diffusion Model with Anatomical-Dose Dual Constraints for End-to-End Multi-Tumor Dose Prediction | 2025 | lLg3WRkAAAAJ:mWEH9CqjF64C |
| Image harmonization and de-harmonization based on singular value decomposition (SVD) in medical domain | 2025 | lLg3WRkAAAAJ:-nhnvRiOwuoC |
| A deep learning framework for reconstructing Breast Amide Proton Transfer weighted imaging sequences from sparse frequency offsets to dense frequency offsets | 2025 | lLg3WRkAAAAJ:U_HPUtbDl20C |
| Systems and methods for segmenting objects in medical images | 2025 | lLg3WRkAAAAJ:3htObqc8RwsC |
| Guest Editorial: Multi-Modal Joint Learning in Healthcare Imaging | 2025 | lLg3WRkAAAAJ:O0nohqN1r9EC |
| System and method for visualizing placement of a medical tube or line | 2025 | lLg3WRkAAAAJ:sNmaIFBj_lkC |
| Prediction of PD-L1 and EBV expression in gastric cancer from H&E-stained Whole Slide Imaging using deep learning | 2024 | lLg3WRkAAAAJ:Br1UauaknNIC |
| Multi-layer image registration | 2024 | lLg3WRkAAAAJ:-mN3Mh-tlDkC |
| Semisupervised Breast MRI Density Segmentation Integrating Fine and Rough Annotations | 2024 | lLg3WRkAAAAJ:owLR8QvbtFgC |
| Knee cartilage estimation based on knee bone geometry using posterior shape model | 2024 | lLg3WRkAAAAJ:7Hz3ACDFbsoC |
| Enhancing Video Grounding with Dual-Path Modality Fusion on Animal Kingdom Datasets | 2024 | lLg3WRkAAAAJ:PaBasH6fAo0C |
| A Multimodal Behavior Recognition Network with Interconnected Architectures | 2024 | lLg3WRkAAAAJ:MpfHP-DdYjUC |
| Controllable Quality Improvement of Mobile Ultrasound | 2024 | lLg3WRkAAAAJ:U4n9YNQMCAIC |
| Combining machine and deep transfer learning for mediastinal lymph node evaluation in patients with lung cancer | 2024 | lLg3WRkAAAAJ:jgBuDB5drN8C |
| AI-based region-of-interest masks for improved data reconstruction | 2024 | lLg3WRkAAAAJ:bz8QjSJIRt4C |
| Fine-Grained Unsupervised Cross-Modality Domain Adaptation for Vestibular Schwannoma Segmentation | 2023 | lLg3WRkAAAAJ:P7Ujq4OLJYoC |
| Accelerated Search for KNN-Based Ceramics with Large Piezoelectric Constants Using Machine Learning Methods | 2023 | lLg3WRkAAAAJ:HeT0ZceujKMC |
| A Hybrid Supervised Fusion Deep Learning Framework for Microscope Multi-Focus Images | 2023 | lLg3WRkAAAAJ:GFxP56DSvIMC |
| Towards Idea Mining: Problem-Solution Phrase Extraction from Text | 2022 | lLg3WRkAAAAJ:86PQX7AUzd4C |
| Guest Editorial Artificial Intelligence in Pre-DICOM | 2022 | lLg3WRkAAAAJ:XoXfffV-tXoC |
| Autonomous Learning Rate Optimization for Deep Learning | 2022 | lLg3WRkAAAAJ:Ri6SYOTghG4C |
| Guest Editorial: Deep Learning in Ultrasound Imaging | 2020 | lLg3WRkAAAAJ:XiVPGOgt02cC |
| Mass Segmentation in Automated 3D Breast Ultrasound using Deep Learning | 2018 | lLg3WRkAAAAJ:AXPGKjj_ei8C |
| Determining Mass Boundary in 3D Automated Breast Ultrasound Images Using a Deformable Model | 2017 | lLg3WRkAAAAJ:xtRiw3GOFMkC |
| Joint synthesis of longitudinal MRI and enhanced prediction of neoadjuvant chemotherapy response in breast cancer: a multicohort study | 2026 | lLg3WRkAAAAJ:NxmKEeNBbOMC |
| Generative Active Learning for Label-Efficient Pan-Organ Ultrasound Diagnosis | 2026 | lLg3WRkAAAAJ:BOlwja0KXvYC |
| APTGNet: The age-prompted and text-guided EEG model for epilepsy detection across all-age groups | 2026 | lLg3WRkAAAAJ:silx2ntsSuwC |
| Beyond Modeling Order: Dual-Path Spatiotemporal Representation Learning for Cross-Subject EEG Emotion Recognition | 2026 | lLg3WRkAAAAJ:naSTrk-c4S8C |
| From Sparsity to Geometry: Spatial Modeling for 3D Reconstruction from Biplanar Bone X-rays | 2026 | lLg3WRkAAAAJ:ijdKiLOsEJMC |
| Organ-Invariant Tumor Representation Learning via Disentangled Adversarial MAE for Multi-organ Ultrasound Imaging | 2026 | lLg3WRkAAAAJ:dAp6zn-oMfAC |
| Multi-Annotation Adaption: A Label-Informed Dynamic Framework for Medical Segmentation and Localization | 2026 | lLg3WRkAAAAJ:jmjb1lOE9QIC |
| Proactive Domain Unification for Robust Echocardiography Segmentation | 2026 | lLg3WRkAAAAJ:c_xDhezhKKUC |
| AsynDiff: Asynchronous-Timestep Diffusion with Noise-Aware Attention for Multi-sequence MRI Synthesis | 2026 | lLg3WRkAAAAJ:OzeSX8-yOCQC |
| MSQG-3DNet: Multi-scale Token Selection with Query-Decoder and Gated Fusion for 3D Breast Tumor Classification | 2026 | lLg3WRkAAAAJ:QVtou7C4vgoC |
| ClinLoop: Human-AI Collaborative Agents for Multimodal Breast Cancer Diagnosis Under Incomplete Clinical Data | 2026 | lLg3WRkAAAAJ:JWITY9-sCbMC |
| MiGAD: Gut Microbiota-Informed Genetic Surrogates for Multimodal Alzheimer’s Disease Diagnosis | 2026 | lLg3WRkAAAAJ:pQTOvowfQioC |
| SAFE-Diff: Scale-Aware Attention and Feature-Dispersive Diffusion with Uncertainty Estimation for Contrast-Enhanced Breast MRI Synthesis | 2026 | lLg3WRkAAAAJ:8dzOF9BpDQoC |
| Beyond the Batch: Momentum-Updated Virtual Cohorts for 3D PET-CT Prognosis | 2026 | lLg3WRkAAAAJ:37UQlXuwjP4C |
| Towards Unified Image–Video Modeling Across B-Mode and Contrast-Enhanced Ultrasound for Multi-task Analysis | 2026 | lLg3WRkAAAAJ:Ic1VZgkJnDsC |
| A Deep Learning Model to Predict Breast Cancer Recurrence Using Longitudinal Mammograms and Clinical Data | 2026 | lLg3WRkAAAAJ:z8nqeaKD1nsC |
| Dual‐branch MRI denoising and motion artifact suppression with uncertainty estimation and segmentation‐based evaluation | 2026 | lLg3WRkAAAAJ:nqdriD65xNoC |
| CDMIQA: A Cross-Domain Perceptual Method and Benchmark Dataset for Medical Image Quality Assessment | 2026 | lLg3WRkAAAAJ:lYAcb2jw7qUC |
| ROP-VL: An Open Dataset Integrating Fundus Photograph and Clinical Knowledge for Retinopathy of Prematurity | 2026 | lLg3WRkAAAAJ:jtI9f0ekYq0C |
| MRICombo: a deep-learning-based framework for universal volumetric segmentation grading-staging and malignancy detection across heterogeneous MRI | 2026 | lLg3WRkAAAAJ:LK8CI43ZvvMC |
| Recurrent Optimization Network for RGB-T salient object detection | 2026 | lLg3WRkAAAAJ:zUl2_INMlC4C |
| S2DENet: Shallow suppression and deep enhancement network for general ultrasound image segmentation | 2026 | lLg3WRkAAAAJ:nPT8s1NX_-sC |
| Interpretable machine-learning survival prediction of breast cancer prognosis from lifestyle factors: evidence from UK biobank | 2026 | lLg3WRkAAAAJ:hQUaER0FWQ4C |
| BPEFNet: a bit plane enhanced fusion network for echocardiographic segmentation | 2026 | lLg3WRkAAAAJ:LGlY6t8CeOMC |
| TNAM: Temporal Neural Additive Models for Multivariate Clinical Time-Series | 2026 | lLg3WRkAAAAJ:hGdtkIFZdKAC |
| DRFMamba: Multi-focus Microscopic Image Registration Fusion Based on Vision Mamba | 2026 | lLg3WRkAAAAJ:mel-f30kHHgC |
| MPU-rPPG: A Comprehensive and High-Fidelity Dataset for Remote Photoplethysmography Across Diverse Conditions and Demographics | 2026 | lLg3WRkAAAAJ:RuPIJ_LgqDgC |
| Deep learning image analysis with increased modularity and reduced footprint | 2026 | lLg3WRkAAAAJ:4X0JR2_MtJMC |
| MFS-VQ-VAE: Synthesizing 7T-like MR images from 1.5 T MR images with Prompt Attention in VQ-VAE | 2026 | lLg3WRkAAAAJ:4aZ_i-5WJEQC |
| From Static Risk to Dynamic Trajectories: Toward World-Model-Inspired Clinical Prediction | 2026 | lLg3WRkAAAAJ:Zh0EY9V9P6UC |
| Lightweight multi-scale weight pruning network for salient object detection | 2026 | lLg3WRkAAAAJ:-uzm3Y7AvW0C |
| Radiomic signatures associated with longitudinal TNM downstaging for prognostic stratification in breast cancer | 2026 | lLg3WRkAAAAJ:NMlhSUseqAsC |
| Decoding Tumor Phenotypes: A Radiologist-Inspired Deep Learning Framework for Breast Cancer Recurrence Prediction | 2026 | lLg3WRkAAAAJ:H_jBuBxbQIAC |
| Accelerating Hankel low-rank MR reconstruction with a patch-based Hankel scheme | 2026 | lLg3WRkAAAAJ:g5Ck-dwhA_QC |
| LoGo-MR: Screening Breast MRI for Cancer Risk Prediction by Efficient Omni-Slice Modeling | 2026 | lLg3WRkAAAAJ:AzKEL7Gb_04C |
| 3D-IRMM-Net: An Interpretable Radiologist-Mimicking 3D Multimodal Network for Lesion Detection in ABUS with LLM-Based Guidance and Uncertainty Quantification | 2026 | lLg3WRkAAAAJ:ZqE1mSdD_DYC |
| AMIF: Authorizable Medical Image Fusion Model with Built-in Authentication | 2026 | lLg3WRkAAAAJ:zwpXiJ37cpgC |
| BDCNet: Feature-Decoupling and Cross-Task Collaboration Network with Biological Priors for Cell Segmentation and Classification | 2026 | lLg3WRkAAAAJ:unp9ATQDT5gC |
| UVTracking: unified vision-based multi-instrument tracking framework for diverse surgical procedures | 2026 | lLg3WRkAAAAJ:EsEWqaRxkBgC |
| Anatomy-Aware MR-Imaging-Only Radiotherapy | 2026 | lLg3WRkAAAAJ:C33y2ycGS3YC |
| Demographic‐aware deep learning for multi‐organ segmentation: Mitigating gender and age biases in CT images | 2026 | lLg3WRkAAAAJ:tHtfpZlB6tUC |
| Impact of Lifestyle Patterns on Breast Cancer Prognosis: Evidence from a UK Biobank Survival Study | 2026 | lLg3WRkAAAAJ:zdjWy_NXXwUC |
| MoGen: A Unified Collaborative Framework for Controllable Multi-Object Image Generation | 2026 | lLg3WRkAAAAJ:-DxkuPiZhfEC |
| System and method for employing residual noise in deep learning denoising for x-ray imaging | 2026 | lLg3WRkAAAAJ:PVgj2kMGcgYC |
| Automated diagnosis of Sturge-Weber Syndrome by detecting leptomeningeal angiomatosis from MRI using a multi-task deep learning framework | 2026 | lLg3WRkAAAAJ:oPLKW5k6eA4C |
| Cross-domain dynamic routing decoders for multi-domain generalization in ultrasound imaging | 2025 | lLg3WRkAAAAJ:hSRAE-fF4OAC |
| A Transducer-adaptive Denoising Model for Medical Ultrasound Imaging | 2025 | lLg3WRkAAAAJ:YlPif8NxrbYC |
| Advancing Clinical Generalization in Remote Photoplethysmography via Age-Specific Physiological Features | 2025 | lLg3WRkAAAAJ:Wq2b2clWBLsC |
| Spatiotemporal Uncertainty-Aware Mamba-Transformer Synergy: Breast Cancer Detection in ABUS | 2025 | lLg3WRkAAAAJ:2ywjKiB__4kC |
| SHIELDNet: Multi-Region Fusion and Denoising for Enhanced rPPG Signal Extraction in Healthcare Monitoring | 2025 | lLg3WRkAAAAJ:eGYfIraVYiQC |
| Multi-scale context U-net for breast cancer postoperative radiotherapy in patients with brachial plexus | 2025 | lLg3WRkAAAAJ:CYCckWUYoCcC |
| BioVFM-21M: Benchmarking and Scaling Self-supervised Vision Foundation Models for Biomedical Image Analysis | 2025 | lLg3WRkAAAAJ:Xl6nMSl579sC |
| Artificial Intelligence and Imaging for Diagnostic and Treatment Challenges in Breast Care: Second Deep Breast Workshop, Deep-Breath 2025, Held in Conjunction with MICCAI 2025 … | 2025 | lLg3WRkAAAAJ:SAZ1SQo2q1kC |
| Training Set Diversity: A Key Factor | 2025 | lLg3WRkAAAAJ:Hck25ST_3aIC |
| Region-Based Text-Consistent Augmentation for Multimodal Medical Segmentation | 2025 | lLg3WRkAAAAJ:jSAVyFp_754C |
| BiMSRec: A Progressive Image Reconstruction Framework for Medical Image Fusion Guided by Multi-scale Deformation Fields | 2025 | lLg3WRkAAAAJ:rTD5ala9j4wC |
| Multimodality image processing techniques for training image data generation and usage thereof for developing mono-modality image inferencing models | 2025 | lLg3WRkAAAAJ:wvYxNZNCP7wC |
| BRPDNet: A BioRegion Prompt Distillation Network for Physiological Monitoring | 2025 | lLg3WRkAAAAJ:kzcSZmkxUKAC |
| Multimodality image processing techniques for training image data generation and usage thereof for developing mono-modality image inferencing models | 2025 | lLg3WRkAAAAJ:r_AWSJRzSzQC |
| System and methods for inferring thickness of object classes of interest in two-dimensional medical images using deep neural networks | 2025 | lLg3WRkAAAAJ:Ak0FvsSvgGUC |
| Methods and systems for image denoising | 2025 | lLg3WRkAAAAJ:gKiMpY-AVTkC |
| An Optic Nerve Segmentation Model Based on Fully-Convolutional-Based Masked Autoencoders and Direction Field | 2025 | lLg3WRkAAAAJ:jFemdcug13IC |
| Contrastive Learning via Randomly Generated Deep Supervision | 2025 | lLg3WRkAAAAJ:AXkvAH5U_nMC |
| Artificial Intelligence and Imaging for Diagnostic and Treatment Challenges in Breast Care: First Deep Breast Workshop, Deep-Breath 2024, Held in Conjunction with MICCAI 2024 … | 2025 | lLg3WRkAAAAJ:FiDNX6EVdGUC |
| Pretraining (MLIP): An Exploration | 2025 | lLg3WRkAAAAJ:6bLC7aUMtPcC |
| Detection of leptomeningeal angiomas in brain MRI of Sturge-Weber syndrome using multi-scale multi-scan Mamba | 2025 | lLg3WRkAAAAJ:sA9dB-pw3HoC |
| FDF-VQVAE: A Frequency Disentanglement and Fusion Learning Framework for Multi-Sequence MRI Enhancement | 2025 | lLg3WRkAAAAJ:zGdJYJv2LkUC |
| X-ray tomosynthesis system providing neural-net guided resolution enhancement and thinner slice generation | 2024 | lLg3WRkAAAAJ:ODE9OILHJdcC |
| Multi-layer image registration | 2024 | lLg3WRkAAAAJ:6ZxmRoH8BuwC |
| Image harmonization for deep learning model optimization | 2024 | lLg3WRkAAAAJ:cWzG1nlazyYC |
| Deep learning image processing | 2024 | lLg3WRkAAAAJ:48xauSegjOkC |
| DeepUniUSTransformer: Towards A Universal UltraSound Model with Prompted Guidance | 2024 | lLg3WRkAAAAJ:otzGkya1bYkC |
| Deep learning image analysis with increased modularity and reduced footprint | 2024 | lLg3WRkAAAAJ:pAkWuXOU-OoC |
| 澳門乳腺癌篩查的模式探討 | 2024 | lLg3WRkAAAAJ:IaI1MmNe2tcC |
| Machine Learning Model for Predicting Risk of Primary Sj? gren's syndrome using N7-methylguanosine-related Genes | 2024 | lLg3WRkAAAAJ:buQ7SEKw-1sC |
| Combining machine and deep transfer learning for mediastinal lymph node evaluation in patients with lung cancer. | 2024 | lLg3WRkAAAAJ:JP7YXuLIOvAC |
| Neural network inferencing efficiency with fewer parameters | 2023 | lLg3WRkAAAAJ:Ehil0879vHcC |
| Improved YOLOX Framework for Automatic Large Intracranial Artery Stenosis Detection in Digital Subtraction Angiography Images | 2023 | lLg3WRkAAAAJ:tH6gc1N1XXoC |
| Is There a Difference between Paper and Electronic Chinese Signatures? | 2023 | lLg3WRkAAAAJ:ZzlSgRqYykMC |
| RDT-FSDet: Few-shot Object Detection for Rapid Antigen Test | 2023 | lLg3WRkAAAAJ:LhH-TYMQEocC |
| Comprehensive deep learning-based framework for automatic organs-at-risk segmentation in head-and-neck and pelvis for MR-guided radiation therapy planning | 2023 | lLg3WRkAAAAJ:yFnVuubrUp4C |
| SVM in Classification of stage 0~ II and III~ IV with Breast Cancer: A Retrospective Cohort Study on a bicentric cohort | 2023 | lLg3WRkAAAAJ:gVv57TyPmFsC |
| PCDAL: A Perturbation Consistency-Driven Active Learning Approach for Medical Image Segmentation and Classification (preprint) | 2023 | lLg3WRkAAAAJ:QYdC8u9Cj1oC |
| Freeze-out as a regularizer in training neural networks | 2022 | lLg3WRkAAAAJ:S16KYo8Pm5AC |
| Research on inertial navigation component measurement and control system | 2022 | lLg3WRkAAAAJ:LO7wyVUgiFcC |
| Automated organ at risk delineation in T2w head and pelvis MR images for MR-only radiation therapy | 2021 | lLg3WRkAAAAJ:e_rmSamDkqQC |
| Postocclusive Reactive Hyperemia of the Cutaneous Microcirculation: Impact of Different Mechanisms | 2019 | lLg3WRkAAAAJ:vRqMK49ujn8C |
| An Improved U-Net Architecture | 2018 | lLg3WRkAAAAJ:AYInfyleIOsC |
| Dedicated computer-aided detection software for automated 3D breast ultrasound | 2018 | lLg3WRkAAAAJ:kVjdVfd2voEC |
| 医学影像诊断及介入式手术的人工智能应用 | 2018 | lLg3WRkAAAAJ:edDO8Oi4QzsC |
| Computer aided detection in automated breast ultrasound screening: a pilot study | 2015 | lLg3WRkAAAAJ:sSrBHYA8nusC |
| Computer-aided detection of breast cancers using Haar-like features in automated 3D breast ultrasound Computer-aided detection of breast cancers using Haar-like features in … | 2015 | lLg3WRkAAAAJ:738O_yMBCRsC |
| Pectoral muscle surface segmentation in automated 3D breast ultrasound using cylindrical transform and atlas information | 2015 | lLg3WRkAAAAJ:ns9cj8rnVeAC |
| Mismatch-Aware Spatiotemporal Learning with MinIP Structural Supervision for Frame-Wise Vessel Segmentation in DSA Sequences |  | lLg3WRkAAAAJ:X0DADzN9RKwC |
| Deep-Learning-based Segmentation of Organs-at-Risk in the Head for MR-assisted Radiation Therapy Planning |  | lLg3WRkAAAAJ:G1UMdFYMoxkC |
| Hierarchical Tissue-Specific Modeling of Pathology Images Predicts Response in HER2+ Breast Cancer |  | lLg3WRkAAAAJ:T_ojBgVMvoEC |
| Contrastive learning through randomly generated dynamic supervision signals |  | lLg3WRkAAAAJ:eO3_k5sD8BwC |
| A Patch-Based Hankel Low-Rank Method for MRI Reconstruction |  | lLg3WRkAAAAJ:DkZNVXde3BIC |
| 3MT-Net: A Multi-modal Multi-task Ensemble Model for Breast Cancer and Lesion Type Classification Based on a Multicentre Study |  | lLg3WRkAAAAJ:WAzi4Gm8nLoC |
| Sdformer: Similarity-Guided Dynamic Frequency Enhancement for Multi-Modality Image Fusion |  | lLg3WRkAAAAJ:YsrPvlHIBpEC |
| One-Uvics: A High Performance One-Stage Model for Ultrasound Video Classification and Segmentation |  | lLg3WRkAAAAJ:uVUOdF_882EC |
| Exploring the future of breast cancer screening in Macao |  | lLg3WRkAAAAJ:kw52XkFRtyQC |
| HyperDisGAN: A Controllable Variety Generative Model Via Hyperplane Distances for Downstream Classifications |  | lLg3WRkAAAAJ:F1b5ZUV5XREC |
| Towards Idea Mining: Problem-Solution Phrase Extraction fromText |  | lLg3WRkAAAAJ:Bg7qf7VwUHIC |
| VIDEO-BASED DISCOMFORT MONITORING FOR PREMATURE INFANTS IN NICU |  | lLg3WRkAAAAJ:D_sINldO8mEC |
| Technical Committee of KBEI-2019 |  | lLg3WRkAAAAJ:B3FOqHPlNUQC |

### 引用量变化（0）

| 标题 | citation_id | 上次 | 本次 |
|---|---|---:|---:|
| — | — | — | — |

### 本次未见的旧论文（0）

| 标题 | 年份 | citation_id |
|---|---:|---|
| — | — |

## API 请求与额度估算

- HTTP API 请求尝试次数（含重试）：5
- 额度消耗保守估算：5 次搜索请求
- 已完成分页的本地缓存命中不发起 API 请求，因而不增加本轮请求数。
- SerpApi 服务端缓存命中可能免费；本报告按每次 HTTP 尝试一次搜索请求估算，实际扣额以账户面板为准。

报告生成时间：2026-11-22T09:41:13Z
