#!/usr/bin/python
# coding=utf-8

"""
Downloads the kaggle blur dataset training data.

The data must be downloaded to "/datasets/kaggle_blur"

The module must define the data extraction logic.

# You can run this on google colab for get faster downloads speeds

"""

import os
import shutil
import pathlib

from kaggle import api
import pandas as pd


def refactor_folder(path):
    """
    Refactor dataset folder for be structered as sharp/blurred images.

    Args:
        path (str): The path where the function will operate

    """
    old_sharp_path = os.path.join(path, 'old_sharp')
    old_defocus_path = os.path.join(path, 'defocused_blurred')
    old_motion_path = os.path.join(path, 'motion_blurred')
    new_sharp_path = os.path.join(path, 'sharp')
    new_blur_path = os.path.join(path, 'blur')

    # Rename sharp folder to old_sharp
    os.rename(
        new_sharp_path,
        old_sharp_path,
    )

    # Create final dataset folders
    os.mkdir(new_sharp_path)
    os.mkdir(new_blur_path)

    # rename everything from old_sharp to sharp only keeping the image id
    images = os.listdir(old_sharp_path)
    for sharp_image in images:
        os.rename(
            os.path.join(old_sharp_path, sharp_image),
            os.path.join(new_sharp_path, '{path}.jpg'.format(path=sharp_image.split('_')[0])),
        )

    # Duplicates the sharp images, with its own id
    images = os.listdir(new_sharp_path)
    image_count = len(images)
    for source_image in images:
        shutil.copy2(
            os.path.join(new_sharp_path, source_image),
            os.path.join(new_sharp_path, '{path}.jpg'.format(path=str(int(source_image.split('.')[0]) + image_count))),
        )

    # Rename everything from defocused_blurred to blur only keeping the id
    images = os.listdir(old_defocus_path)
    for defocus_image in images:
        os.rename(
            os.path.join(old_defocus_path, defocus_image),
            os.path.join(new_blur_path, '{path}.jpg'.format(path=defocus_image.split('_')[0])),
        )

    # Rename everything from motion_blurred to blur and assigning a new id
    images = os.listdir(old_motion_path)
    for motion_image in images:
        os.rename(
            os.path.join(old_motion_path, motion_image),
            os.path.join(new_blur_path, '{path}.jpg'.format(path=str(int(motion_image.split('_')[0]) + image_count))),
        )


def run(path):
    """
    Run the script.

    Args:
        path (str): Path to download dataset files.

    """
    # Logs
    print('Downloading kaggle_blur')

    download_path = pathlib.Path(path)/'kaggle_blur'
    file_name = download_path/'blur-dataset.zip'

    if (not file_name.exists()):
        api.dataset_download_cli(
            'kwentar/blur-dataset',
            path=download_path,
            unzip=True,
        )

        refactor_folder(download_path)


if (__name__ == '__main__'):
    folder_path = os.path.join(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(__file__),
                    ),
                ),
            ),
        ),
        'datasets',
    )
   
    run(folder_path)
