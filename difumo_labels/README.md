# DiFuMo atlases

1. We provide Dictionaries of Functional Modes “DiFuMo” that can serve as atlases to extract
   functional signals, eg to serve as IDPs, with different dimensionalities
   (64, 128, 256, 512, and 1024). These modes are optimized to represent well raw BOLD timeseries,
   over a with range of experimental conditions.

       - All atlases are available in .nii.gz format and sampled to MNI space
   
2. We provide meaningful names for these modes, based on their anatomical
   location, to facilitate reporting of results. Additionally, we also
   attach the corresponding Yeo et al. 2011 functional networks to these
   modes. Naively, we also provide indicators of "GM", "WM", "CSF" to each
   mode. So the columns in the csvs of each dimension looks like this:

       - The corresponding component named as "Component"  
       - Anatomical names to each component named as "Difumo_names"
       - Yeo et al. 2011 network names to each mode named as "Yeo_networks7", "Yeo_networks17".
       - ICBM brain masks indicator to each mode named as "GM", "WM", "CSF".
   

CAVEAT
------
Rather than concluding on what a ICBM structure is, we added three columns that
give the overlap to gm, wm, csf in numerical values. The values we provide
helps to pick on GM regions > 0.3 for fMRI analysis. Excluding components from
white matter and cerebro spinal fluid.

Please see the script about how we compute these values:
https://github.com/Parietal-INRIA/DiFuMo/blob/master/region_labeling/brain_masks_overlaps.py


## Datasets and Statistical model used to extract these atlases

For this, we leverage the wealth of openly-available functional images
(Poldrack et al., 2013) and stochastic online matrix factorization algorithm
(SOMF, Mensch et al., 2018), sparse dictionary learning.

## Cite this work if you use these atlases

Dadi, K., Varoquaux, G., Machlouzarides-Shalit, A., Gorgolewski, KJ.,
Wassermann, D., Thirion, B., Mensch, A. Fine-grain atlases of functional
modes for fMRI analysis **Paper in preparation**

### References

Mensch, A., Mairal, J., Thirion, B., Varoquaux, G., 2018. Stochastic
Subsampling for Factorizing Huge Matrices. IEEE Transactions
on Signal Processing 66, 113–128.

Poldrack, R.A., Barch, D.M., Mitchell, J.P., et al., 2013. Toward
open sharing of task-based fMRI data: the OpenfMRI project.
Frontiers in neuroinformatics 7.

Yeo, B., Krienen, F., Sepulcre, J., Sabuncu, M., et al., 2011. The
organization of the human cerebral cortex estimated by intrinsic
functional connectivity. J Neurophysio 106, 1125.

Fonov, V.S., Evans, A.C., Botteron, K., Almli, C.R., McKinstry, R.C.,
Collins, D.L., and BDCG., 2011. Unbiased average age-appropriate atlases
for pediatric studies. NeuroImage, 54.
