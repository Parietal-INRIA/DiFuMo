# DiFuMo atlases

1. We provide Dictionaries of Functional Modes “DiFuMo” that can serve as atlases to extract
   functional signals, eg to serve as IDPs, with different dimensionalities
   (64, 128, 256, 512, and 1024). These modes are optimized to represent well raw BOLD timeseries,
   over a with range of experimental conditions.
   
2. Additionally, we provide meaningful names for these modes, based on their anatomical
   location, to facilitate reporting of results.
   

      
       - All atlases are available in .nii.gz format and sampled to MNI space
       - Anatomical names are available for each resolution in .csv

## Simple demo

![Signals extraction and reconstruction](notebook/demo.ipynb "Simple demo")

[Run the demo online](https://mybinder.org/v2/gh/Parietal-INRIA/DiFuMo/master?filepath=notebook%2Fdemo.ipynb)

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

