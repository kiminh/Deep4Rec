import os

import deep4rec.models

from deep4rec.datasets.census import CensusDataset
from deep4rec.datasets.frappe import FrappeDataset
from deep4rec.datasets.ml100k import MovieLens100kDataset
from deep4rec.datasets.ml import MovieLensDataset
from deep4rec.datasets.clf_negative import ClfNegativeSamplingDataset
import deep4rec.utils as utils

# Datasets ready to be used by users
datasets = {"frappe": FrappeDataset, "ml-100k": MovieLens100kDataset}

# TODO: add these datasets when ready
wip_datasets = {
    "census": CensusDataset,
    "ml-1m": MovieLensDataset,
    "ml-1m-neg": ClfNegativeSamplingDataset,
    "ml-20m": MovieLensDataset,
}


def options():
    """Returns a list containing the available datasets."""
    return list(datasets.keys())


def build_dataset(
    dataset_name,
    output_dir=None,
    verbose=True,
    maybe_download=True,
    maybe_preprocess=True,
):
    """Build Dataset instance.

  Args:
    dataset_name: A string indicating the dataset to be build.
    output_dir: A string indicating the output directory used to store auxiliary files. If None,
    then the default path defined in `utils.py` will be used.
    maybe_download: A boolean indicating if the files should be downloaded.
    maybe_preprocess: A boolean indicating if the files should be preprocessed.

  Returns:
    A Dataset instance.
  """
    if not output_dir:
        output_dir = os.path.join(utils.DEFAULT_OUTPUT_DIR, dataset_name)

    if dataset_name in datasets:
        dataset = datasets[dataset_name](
            output_dir=output_dir, dataset_name=dataset_name, verbose=verbose
        )
    elif dataset_name in wip_datasets:
        dataset = wip_datasets[dataset_name](
            output_dir=output_dir, dataset_name=dataset_name, verbose=verbose
        )
    else:
        raise ValueError("Unkown dataset {}".format(dataset_name))

    if maybe_download:
        dataset.maybe_download()

    if maybe_preprocess:
        dataset.maybe_preprocess()

    # Some datasets need a building step.
    dataset.build()

    return dataset
