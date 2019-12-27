"""
"""
import pandas as pd
from os.path import join

from sklearn.datasets.base import Bunch
from nilearn import datasets
from nilearn.datasets.utils import _get_dataset_dir, _fetch_files


def _check_atlases(atlas_names):
    """Check that the atlases provided are valid names, string or
    list of strings, otherwise raise an error.
    """
    valid_atlases = ['harvard_oxford', 'destrieux', 'diedrichsen',
                     'juelich', 'jhu', 'mist', 'yeo_networks7',
                     'yeo_networks17']
    err_msg = ("You provided atlas name(s) {0} which is "
               "not valid. Provide in {1}")

    if isinstance(atlas_names, str):
        atlas_names = [atlas_names, ]

    for name in atlas_names:
        if name not in valid_atlases:
            raise ValueError(err_msg.format(name, valid_atlases))
    return atlas_names


def _fetch_atlas_diedrichsen(atlas_name):
    """Cerebellum atlas registered to MNI with FNIRT

    Parameters
    ----------
    atlas_name : str
        Anyone could be from a list
        ['prob-1mm', 'prob-2mm', 'maxprob-thr50-1mm', 'maxprob-thr50-2mm',
         'maxprob-thr25-1mm', 'maxprob-thr25-2mm', 'maxprob-thr0-1mm',
         'maxprob-thr0-2mm']

    Returns
    -------
    maps : str
        Path to cerebellum atlas

    labels : list of str
        Anatomical labels assigned to each label
    """
    atlas_name = 'Cerebellum-MNIfnirt-{0}.nii.gz'.format(atlas_name)
    labels_img = join('/usr/local/fsl/data/atlases/Cerebellum/',
                      atlas_name)
    label_file = '/usr/local/fsl/data/atlases/Cerebellum_MNIfnirt.xml'
    names = {}
    from xml.etree import ElementTree
    names[0] = 'Background'
    for label in ElementTree.parse(label_file).findall('.//label'):
        names[int(label.get('index')) + 1] = label.text
    names = list(names.values())
    return Bunch(maps=labels_img, labels=names)


def _fetch_atlas_juelich(atlas_name):
    """Juelich atlas

    Parameters
    ----------
    atlas_name : str
        Anyone could be from a list
        ['maxprob-thr0-1mm', 'maxprob-thr0-2mm',
         'maxprob-thr25-1mm', 'maxprob-thr25-2mm', 'maxprob-thr50-1mm',
         'maxprob-thr50-2mm', 'prob-1mm', 'prob-2mm']

    Returns
    -------
    maps : str
        Path to Juelich atlas

    labels : list of str
        Anatomical labels assigned to each label
    """
    atlas_name = 'Juelich-{0}.nii.gz'.format(atlas_name)
    labels_img = join('/usr/local/fsl/data/atlases/Juelich/',
                      atlas_name)
    label_file = '/usr/local/fsl/data/atlases/Juelich.xml'
    names = {}
    from xml.etree import ElementTree
    names[0] = 'Background'
    for label in ElementTree.parse(label_file).findall('.//label'):
        names[int(label.get('index')) + 1] = label.text
    names = list(names.values())
    return Bunch(maps=labels_img, labels=names)


def _fetch_atlas_jhu(atlas_name):
    """John Hopkins University atlas

    Parameters
    ----------
    atlas_name : str
        Anyone could be from a list
        ['labels-1mm', 'labels-2mm']

    Returns
    -------
    maps : str
        Path to JHU atlas

    labels : list of str
        Anatomical labels assigned to each label
    """
    atlas_name = 'JHU-ICBM-{0}.nii.gz'.format(atlas_name)
    labels_img = join('/usr/local/fsl/data/atlases/JHU/',
                      atlas_name)
    label_file = '/usr/local/fsl/data/atlases/JHU-labels.xml'
    names = {}
    from xml.etree import ElementTree
    names[0] = 'Background'
    for label in ElementTree.parse(label_file).findall('.//label'):
        names[int(label.get('index')) + 1] = label.text
    names = list(names.values())
    return Bunch(maps=labels_img, labels=names)


def fetch_mist():
    """Download MIST parcellation n=122
    https://mniopenresearch.org/articles/1-3

    Returns
    -------
    maps : str
        Path to MIST parcellation

    labels : list of str
        Anatomical labels assigned to each label
    """
    url = 'https://ndownloader.figshare.com/files/9811081'
    opts = {'uncompress': True}
    data_dir = _get_dataset_dir('mist', data_dir=None,
                                verbose=1)
    files = [(join('Release', 'Parcel_Information', 'MIST_122.csv'),
              url, opts),
             (join('Release', 'Parcellations', 'MIST_122.nii.gz'),
              url, opts)]
    files = _fetch_files(data_dir, files, resume=True, verbose=1)
    parcel_info = pd.read_csv(files[0], sep=';')
    names = parcel_info['name']
    df = pd.DataFrame(['Background'], columns=['name'])
    for i in range(names.shape[0]):
        df2 = pd.DataFrame([names[i]], columns=['name'])
        df = df.append(df2, ignore_index=True)
    return Bunch(maps=files[1], labels=df)


def fetch_yeo(network_name):
    """Return atlas and networks names of Yeo et al. 2011

    Parameters
    ----------
    network_name : str
        Valid names are 'yeo_networks7', 'yeo_networks17'

    Returns
    -------
    maps : str
        Path to Yeo et al. 2011 atlas specified by network name

    labels : list of str
        Network names are manually annotated.

    NOTES
    -----
    Problem: map "networks number" from original yeo et al. 2011 to "network names"

    Solution: Is to match/close match between RGB color look up table (tuple)
              associated to each network number in
              https://github.com/ThomasYeoLab/CBIG/blob/master/stable_projects/brain_parcellation/Schaefer2018_LocalGlobal/Parcellations/MNI/Schaefer2018_1000Parcels_17Networks_order.txt

    Another source discussion on this issue:
    https://github.com/ThomasYeoLab/CBIG/issues/2

    Original Yeo et al 2011 data can be fetched using function
    datasets.fetch_atlas_yeo_2011 with Nilearn package.

    =============================================================
    # Yeo2011_7Networks_ColorLUT

    0            NONE   0   0   0   0
    1     7Networks_1 120  18 134   0
    2     7Networks_2  70 130 180   0
    3     7Networks_3   0 118  14   0
    4     7Networks_4 196  58 250   0
    5     7Networks_5 220 248 164   0
    6     7Networks_6 230 148  34   0
    7     7Networks_7 205  62  78   0

    =============================================================
    # Yeo2011_17Networks_ColorLUT

    0            NONE   0   0   0   0
    1    17Networks_1 120  18 134   0
    2    17Networks_2 255   0   0   0
    3    17Networks_3  70 130 180   0
    4    17Networks_4  42 204 164   0
    5    17Networks_5  74 155  60   0
    6    17Networks_6   0 118  14   0
    7    17Networks_7 196  58 250   0
    8    17Networks_8 255 152 213   0
    9    17Networks_9 220 248 164   0
    10   17Networks_10 122 135  50   0
    11   17Networks_11 119 140 176   0
    12   17Networks_12 230 148  34   0
    13   17Networks_13 135  50  74   0
    14   17Networks_14  12  48 255   0
    15   17Networks_15   0   0 130   0
    16   17Networks_16 255 255   0   0
    17   17Networks_17 205  62  78   0

    """
    yeo_networks7 = {"0": "Background",
                     "7Networks_1": "VisCent",       # VisualCentral
                     "7Networks_2": "SomMotA",       # SomatoMotor A
                     "7Networks_3": "DorsAttnB",     # DorsalAttention B
                     "7Networks_4": "SalVentAttnA",  # SalienceVentralAttention A
                     "7Networks_5": "LimbicA",       # Limbic A Temporoporal
                     "7Networks_6": "ContA",         # Control A IPS
                     "7Networks_7": "DefaultB"       # Default B
                     }
    yeo_networks17 = {"0": "Background",
                      "17Networks_1": "VisCent",       # VisualCentral
                      "17Networks_2": "VisPeri",       # VisualPeripheral
                      "17Networks_3": "SomMotA",       # SomatoMotor A
                      "17Networks_4": "SomMotB",       # SomatoMotor B
                      "17Networks_5": "DorsAttnA",     # DorsalAttention A
                      "17Networks_6": "DorsAttnB",     # DorsalAttention B
                      "17Networks_7": "SalVentAttnA",  # SalienceVentralAttention A
                      "17Networks_8": "SalVentAttnB",  # SalienceVentralAttention B
                      "17Networks_9": "LimbicA",       # Limbic A Temporoporal
                      "17Networks_10": "LimbicB",      # Limbic B OrbitoFrontalC
                      "17Networks_11": "ContC",        # Cont C Cingp
                      "17Networks_12": "ContA",        # Cont A IPS
                      "17Networks_13": "ContB",        # Cont B IPL
                      "17Networks_14": "TempPar",      # Temporo Parietal
                      "17Networks_15": "DefaultC",     # Default C RSP
                      "17Networks_16": "DefaultA",     # Default A pCunPCC
                      "17Networks_17": "DefaultB"      # Default B
                      }
    data = datasets.fetch_atlas_yeo_2011()
    if network_name == 'yeo_networks7':
        maps = data.thick_7
        labels = list(yeo_networks7.values())
    elif network_name == 'yeo_networks17':
        maps = data.thick_17
        labels = list(yeo_networks17.values())
    else:
        raise ValueError("Invalid network name is provided for Yeo thick"
                         " version of parcellations.")
    return Bunch(maps=maps, labels=labels)


def fetch_atlases(atlas_names):
    """Fetch atlases provided by name(s)

    Parameters
    ----------
    atlas_names : str or list of str
        Grab atlas from web given the name. Few are shipped with FSL
        and Nilearn.
        Valid options:  ['harvard_oxford', 'destrieux', 'diedrichsen',
                         'juelich', 'jhu', 'mist', 'yeo_networks7',
                         'yeo_networks17']

    Returns
    -------
    data : dict
        Bunch of atlases
    """
    data = {}
    atlas_names = _check_atlases(atlas_names)
    for atlas_name in atlas_names:
        if atlas_name == 'harvard_oxford':
            name = 'cort-maxprob-thr25-2mm'
            data[atlas_name] = datasets.fetch_atlas_harvard_oxford(name)
        elif atlas_name == 'destrieux':
            data[atlas_name] = datasets.fetch_atlas_destrieux_2009()
        elif atlas_name == 'diedrichsen':
            data[atlas_name] = _fetch_atlas_diedrichsen('maxprob-thr25-2mm')
        elif atlas_name == 'juelich':
            data[atlas_name] = _fetch_atlas_juelich('maxprob-thr25-2mm')
        elif atlas_name == 'jhu':
            data[atlas_name] = _fetch_atlas_jhu('labels-2mm')
        elif atlas_name == 'mist':
            data[atlas_name] = fetch_mist()
        elif atlas_name in ['yeo_networks7', 'yeo_networks17']:
            data[atlas_name] = fetch_yeo(atlas_name)
        else:
            raise ValueError("Not a valid atlas. Given atlas is exhausted")
    return data
