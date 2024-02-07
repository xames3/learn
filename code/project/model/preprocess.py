"""\
Generic Data Preprocessing APIs
===============================

Author: Akshay Mestry <xa@mes3.dev>
Created on: Sunday, February 04 2024
Last updated on: Wednesday, February 07 2024

:copyright: (c) 2024 Akshay Mestry. All rights reserved.
:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations

import abc
import os
import random
import shutil
import time
import typing as t
from os import path as p

import cv2
import numpy as np
import pandas as pd
import pydicom
from tqdm import tqdm

from .. import OutputFormatError
from .. import big_bang
from .. import logger
from .. import shorten
from ..logging import last_record
from ..types import _Any
from ..types import _Dataset
from ..types import _Image
from ..types import _SupportedFormats
from .config import cfg

supported_processors: dict[str, type[BaseImageProcessor]] = {}
mini_bang = time.time()


class BaseImageProcessor:
    """Base class to (process) convert and transform DICOM/DCM files to
    suitable formats.

    In a Machine Learning task, especially when working with images, we
    need to make sure the images are in right format. In this case, we
    are working with images from the medical field, where the images are
    usually in ``DCM`` or ``DICOM`` format which is an industry standard
    for medical imaging. Traditional image processing methods are not
    applicable on this format and hence require some inital conversion
    and preprocessing.

    This class provides a mean to convert the images to various formats
    using simple class extension. The original dataset contains around
    40,000 images (roughly) in total, called ``slices``. Out of these
    40,000, we use 29,000 (roughly) DICOM images which are present in
    the base CSV file.

    This class provides an abstraction for converting and transforming
    these DICOM images to respective images formats according to the
    base CSV file and specified format.

    :var supported_formats: Sequence of supported image formats.
    :param refresh: Boolean flag to whether refresh the conversion
                    setting or not, defaults to ``True``.
    """

    supported_formats: _SupportedFormats = cfg.images.supported_formats

    def __init_subclass__(cls) -> None:
        """Register all the derived image processors."""
        cls.format = cls.__name__.lower()
        logger.info(f"Mapping processor: {cls.format} to base instance")
        supported_processors[cls.format] = cls

    def __init__(self, *, refresh: bool = True) -> None:
        """Initialize ``BaseImageProcessor`` with refreshing option."""
        self.path = p.join(cfg.path.processed, self.format)
        if refresh:
            logger.warning(
                "Running the image processing with refresh flag on, this will "
                f"refresh ({self.format}) images from previous conversion"
            )
            if p.exists(self.path):
                shutil.rmtree(self.path)
            else:
                logger.info(
                    f"Path: {shorten(self.path)} was empty or didn't exist,"
                    " so nothing is erased (no cleanup)"
                )
        paths = map(lambda x: p.join(self.path, str(x)), cfg.images.labels)
        os.mkdir(self.path)
        for path in paths:
            os.mkdir(path)
        if not self.format in self.supported_formats:
            raise OutputFormatError(
                f"Only {', '.join(self.supported_formats[:-1])} and "
                f"{self.supported_formats[-1]} formats are supported"
            )
        logger.info(f"Loading (csv) dataset: {cfg.path.csv}")
        self.csv = pd.read_csv(cfg.path.csv)
        logger.info(
            f"Dataset loaded successfully: {self.csv.shape[0]} records found "
            f"in {time.time() - big_bang:.3f} secs"
        )

    def prepare_dataset(self) -> _Dataset:
        """Maps and builds a dataset from raw image files and their
        corresponding labels for further processing.

        This method iterates over all the available raw images specified
        by the path in the configuration settings (``cfg.path.images``).
        It uses the base CSV file, where each row corresponds to an image
        file and contains metadata including the label for the image. The
        method filters and pairs each valid image with its label based on
        the presence of the image file name in the CSV index, effectively
        creating a dataset suitable for further image processing tasks,
        such as training machine learning models.

        The dataset is structured as a list of tuples, where each tuple
        consists of a label and the full path to the corresponding image
        file. This structure facilitates easy loading and processing of
        image data in subsequent steps.

        :returns: A list of tuples, with each tuple containing a label
                  and the path to an image file.
        """
        dataset: _Dataset = []
        logger.info(
            "Starting to iterate over all the available raw images from path: "
            f"{shorten(cfg.path.images)} for sourcing all the valid "
            "observations"
        )
        self.csv.set_index("file", inplace=True)
        for root, _, files in os.walk(cfg.path.images):
            for file in files:
                if file in self.csv["instance"]:
                    label = self.csv.loc[file, "label"]
                    dataset.append((label, p.join(root, file)))
        logger.info(
            f"Mapped {len(self.csv.index)} raw images from the dataset "
            f"across {len(cfg.images.labels)} different classes"
        )
        return dataset

    def process(self, transforms: t.Sequence[Transform]) -> None:
        """Process all valid images in the dataset using specified
        transformations.

        This method leverages the dataset prepared by the
        ``BaseImageProcessor.prepare_dataset()`` to iterate over each
        image and its label.

        Each image is read and converted to an array format suitable for
        processing. A series of transformations, as specified by the
        ``transforms`` parameter, are then applied sequentially to each
        image. The transformed images are saved in a new format specified
        by ``self.format`` to a designated path within a label-specific
        directory.

        :param transforms: A sequence of transformation operations
                           (``Transform``) to be applied to each image
                           in the dataset.

        .. seealso::

            [1] This method uses ``pydicom`` to read DICOM images and
                ``cv2`` for saving the transformed images.
        """
        dataset = tqdm(self.prepare_dataset(), unit=" images")
        for label, image in dataset:
            file = f"{p.splitext(p.basename(image))[0]}.{self.format}"
            image = pydicom.dcmread(image).pixel_array
            for transform in transforms:
                image = transform.apply(image)
            logger.loop("Processing images")
            dataset.set_description(last_record.pop())
            cv2.imwrite(p.join(self.path, str(label), file), image)
        logger.info(
            "Processed all raw images from the dataset "
            f"through ({len(transforms)}) different transforms in "
            f"{time.time() - mini_bang:.3f} secs"
        )


class PNG(BaseImageProcessor):
    """DICOM to PNG image processor."""


class ImageProcessor:
    """Image processor class.

    This class act as an entrypoint for converting and transforming the
    original DICOM images to various file formats like ``png``, ``jpeg``
    or ``bmp``.

    .. code-block:: python

        >>> processor = ImageProcessor()
        >>> processor.png.process()

    :param refresh: Boolean flag to whether refresh the conversion
                    setting or not, defaults to ``True``.
    """

    def __init__(self, *, refresh: bool = True) -> None:
        """Initialize ``ImageProcessor`` with refreshing option."""
        self.refresh = refresh

    def __getattr__(self, attr: str) -> _Any:
        """Override ``getattr`` and build processor class on runtime."""
        return supported_processors[attr](refresh=self.refresh)


class Transform(abc.ABC):
    """Base class for image augmentation and transformations.

    This class serves as the foundation for defining and implementing
    custom image transformation strategies. It provides a structured
    framework for creating strategies that can include a variety of
    operations such as scaling, padding, rotating, flipping, and more.

    All the subclasses should implement the ``apply`` method to apply a
    specific image transformation.

    .. code-block:: python

        >>> import cv2
        >>> class HorizontalFlip(Transform):
        ...     def apply(self, image):
        ...         return cv2.flip(image, 1)

    .. warning::

        This class is intended as a base class for creating custom
        strategies. It does not provide specific image transformation
        methods. Subclasses are expected to implement their own
        transformation logic.
    """

    @abc.abstractmethod
    def apply(self, image: _Image) -> _Image:
        """Implement ``apply`` method in the subclasses."""
        raise NotImplementedError


class NormalizeTransform(Transform):
    """A transformation class for normalizing image pixel values.

    This class inherits from a base ``Transform`` class and implements
    an ``apply`` method to normalize the pixel values of an input image.

    Normalization adjusts the pixel values such that the resulting image
    spans the full possible range of intensities (0 to 255 for 8-bit
    images). This process can enhance the contrast of the image, making
    it more suitable for visual inspection and further image processing
    tasks, including machine learning and computer vision applications.
    """

    def apply(self, image: _Image) -> _Image:
        """Applies normalization to the input image to enhance its
        contrast.

        The method creates a copy of the input image and adjusts its
        pixel values to span the full range of 0 to 255. This is
        achieved by scaling the pixel values based on the ratio of 255
        to the range of the input image's pixel values, followed by an
        adjustment to ensure the minimum pixel value starts at 0.

        The result is a contrast-enhanced image with normalized pixel
        values.

        :param image: The input image to be normalized.
        :returns: The normalized image as a 2D array with dtype
                  ``uint8``, ensuring that pixel values are within the
                  8-bit range (0 to 255).

        .. note::

            The input image should be a 2D array-like structure
            representing an image where pixel values are numeric.
        """
        ratio = 255 / (image.max() - image.min())
        image = image * ratio
        image -= image.min()
        return image.astype("uint8")


class ResizeTransform(Transform):
    """A transformation class to add padding (resize) around images.

    This class is designed to adjust the size of images by adding
    padding, ensuring that all images have the same dimensions as
    specified in the project's configuration settings.

    Padding is applied evenly on all sides of the image if necessary,
    and the added padding has a pixel value of 0 (black).

    .. note::

        It is important to ensure that the ``cfg.images.size``
        configuration is set correctly before initializing this class.
        The logged warning serves as a reminder to check this
        configuration.
    """

    def __init__(self) -> None:
        """Initialize ``ResizeTransform`` class with warning message."""
        self.w, self.h = cfg.images.size
        logger.warning(
            "Padding is chosen as one of transformation techniques, "
            f"the output images will be padded [{self.w}x{self.h}]"
        )

    def apply(self, image: _Image) -> _Image:
        """Adds padding to the input image to match the specified
        dimensions.

        This method calculates the necessary padding to be added to each
        side of the image to achieve the target size specified by
        ``cfg.images.size``.

        The padding is applied symmetrically, and the pixel values of
        the padding are set to 0 (black).

        :param image: A 2D array representing the grayscale image to be
                      padded.
        :returns: The padded image as a 2D array of the same type as the
                  input image.
        """
        h, w = image.shape
        ph, pw = max(self.h - h, 0), max(self.w - w, 0)
        t = ph // 2
        b = ph - t
        l = pw // 2
        r = pw - l
        return np.pad(image, ((t, b), (l, r)), constant_values=0)


class HorizontalFlipTransform(Transform):
    """A transformation class for horizontally flipping an image as part
    of data augmentation.

    This class inherits from ``Transformation`` and implements the
    ``apply`` method to flip images horizontally. The horizontal flip is
    applied randomly based on a probability check, offering a simple yet
    effective form of data augmentation for machine learning models,
    particularly in computer vision tasks.

    This randomness introduces variation in the training dataset, which
    can help improve the generalization of models.

    .. note::

        The decision to flip the image is made randomly with a 50%
        chance. This behavior can be adjusted if a different probability
        is desired by modifying the condition in the ``apply`` method.
    """

    def apply(self, image: _Image) -> _Image:
        """Apply horizontal flipping to the input image with a 50%
        probability.

        :param image: The input image to be flipped horizontally.
        :returns: The horizontally flipped image, if the random condition
                  is met; otherwise, the original image is returned
                  unchanged.
        """
        return cv2.flip(image, 1) if random.random() < 0.5 else image


class RotationTransform(Transform):
    """A transformation class for rotating an image by a specified angle.

    This class extends ``Transformation`` to provide functionality for
    rotating images. The rotation angle can be specified during class
    initialization. If no angle is provided, a random angle (90, 180, or
    270 degrees) is selected to apply the rotation.

    This approach adds variability to the training dataset, potentially
    improving model robustness by presenting it with images viewed from
    different orientations.

    :param angle: The angle in degrees by which the image will be
                  rotated. The angle defaults to a random choice among
                  90, 180, and 270 degrees if not explicitly provided.
                  Defaults to ``None``.
    """

    def __init__(self, angle: t.Optional[int | float] = None) -> None:
        """Initialize ``RotationTransform`` class with an angle."""
        self.angle = angle if angle else random.choice((90, 180, 270))

    def apply(self, image: _Image) -> _Image:
        """Apply rotation to the input image based on the specified
        angle.

        :param image: The input image to be rotated. This image should
                      be in a format compatible with OpenCV operations.
        :returns: The rotated image, maintaining the original image's
                  dimensions.
        """
        h, w = image.shape
        center = (h // 2, w // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, self.angle, 1.0)
        return cv2.warpAffine(image, rotation_matrix, (h, w))


if __name__ == "__main__":
    processor = ImageProcessor()
    transforms = [
        NormalizeTransform(),
        ResizeTransform(),
    ]
    processor.png.process(transforms)
