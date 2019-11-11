# DiFuMo atlases

1. We provide Dictionaries of Functional Modes “DiFuMo” that can serve as atlases to extract
   functional signals, eg to serve as IDPs, with different dimensionalities
   (64, 128, 256, 512, and 1024). These modes are optimized to represent well raw BOLD timeseries,
   over a with range of experimental conditions.
   
2. Additionally, we provide meaningful names for these modes, based on their anatomical
   location, to facilitate reporting of results.
   

      
       All atlases are available in .nii.gz format and sampled to MNI space


## Datasets and Statistical model

For this, we leverage the wealth of openly-available functional images
(Poldrack et al., 2013) and stochastic online matrix factorization algorithm
(SOMF, Mensch et al., 2018), sparse dictionary learning.

## Cite this work if you use these atlases

__Authors__: Kamalaker Dadi, Gaël Varoquaux, Antonia Machlouzarides-Shalit, Krzysztof J. Gorgolewski,
             Demian Wassermann, Bertrand Thirion, Arthur Mensch.
__Title__: Fine-grain atlases of functional modes for fMRI analysis
__Status__: Paper in preparation

### References

Mensch, A., Mairal, J., Thirion, B., Varoquaux, G., 2018. Stochastic
Subsampling for Factorizing Huge Matrices. IEEE Transactions
on Signal Processing 66, 113–128.

Poldrack, R.A., Barch, D.M., Mitchell, J.P., et al., 2013. Toward
open sharing of task-based fMRI data: the OpenfMRI project.
Frontiers in neuroinformatics 7.

