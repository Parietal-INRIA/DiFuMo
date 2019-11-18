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
                     'juelich', 'jhu', 'mist']
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


def fetch_atlases(atlas_names):
    """Fetch atlases provided by name(s)

    Parameters
    ----------
    atlas_names : str or list of str
        Grab atlas from web given the name. Few are shipped with FSL
        and Nilearn.
        Valid options:  ['harvard_oxford', 'destrieux', 'diedrichsen',
                         'juelich', 'jhu', 'mist']

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
        else:
            raise ValueError("Not a valid atlas. Given atlas is exhausted")
    return data
