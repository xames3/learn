"""\
Generic Model Specific Configurations
===================================

Author: Akshay Mestry <xa@mes3.dev>
Created on: Sunday, February 04 2024
Last updated on: Sunday, February 04 2024

:copyright: (c) 2024 Akshay Mestry. All rights reserved.
:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations

import typing as t
from os import path as p

from .. import cfg
from ..types import _Path
from ..types import _SupportedFormats as _SF
from ..utils import AttrDict

# Define path to the dataset i.e the base CSV file and the raw Dicom files.
# The base CSV file has 7 columns each with specific importance for
# instance, ``file`` corresponds to the filename of the raw Dicom image in
# the ``images`` directory. Whereas ``instance`` and ``slice``
# correspond to the file name without ``.dcm`` extension. The ``label``
# is the label of the image or the class of the image. Finally, the
# ``agreement`` and the ``radiologist`` are the agreement ratings among
# various radiologists.
cfg.path.csv: _Path = p.join(cfg.path.raw, "base.csv")
cfg.path.images: _Path = p.join(cfg.path.raw, "images")

# Define all the attributes related the images.
cfg.images: AttrDict = AttrDict(
    {
        # Since we can't use the Dicom images for processing the images
        # directly we need to convert them into suitable or usable
        # formats. Currently, the code supports 3 image file formats.
        "supported_formats": t.get_args(_SF),
        # All the unique available labels from the ``base.csv`` file.
        "labels": list(range(1, 6)),
        "size": (71, 71),
    }
)
