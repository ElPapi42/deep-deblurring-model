#!/usr/bin/python
# coding=utf-8

"""
Use all the available data for generate a .csv with blur/sharp images paths.

Every folder must contain two subfolder with the respective shar/blur images:

- <dataset_name>
-- sharp
--- img01.jpg
--- img02.jpg
-- blur
--- img01.jpg
--- img02.jpg

The image pairs must have the same name inside different folders
img01.jpg is present in blur and sharp folders

"""

import os

import pandas as pd


def run(path):
    """
    Generate train/valid/test.csv with sharp/blur image pairs.

    Args:
        path (str): Path containg datasets folders. csv will be stored here too

    """
    # Storage paths
    csv_path = os.path.join(path, 'csv')
    train_path = os.path.join(csv_path, 'train.csv')
    valid_path = os.path.join(csv_path, 'valid.csv')
    test_path = os.path.join(csv_path, 'test.csv')

    # Only executes if the csv folder is not there
    if (not (os.path.exists(csv_path) and os.path.isdir(csv_path))):
        # Logs
        print('Generating .csv files')

        # Make csv folder
        os.mkdir(csv_path)

        # list possible datasets subfolders
        ds_folders = os.listdir(path)

        # Ensures there is no tfrecords folder in the list
        if (ds_folders.count('tfrecords') > 0):
            ds_folders.pop(ds_folders.index('tfrecords'))

        dataset = pd.DataFrame()

        for dset in ds_folders:
            dset_path = os.path.join(path, dset)

            sharp_path = os.path.join(dset_path, 'sharp')
            blur_path = os.path.join(dset_path, 'blur')

            if (os.path.isdir(sharp_path) and os.path.isdir(blur_path)):
                # Get names of kaggle blur images
                sharp_list = os.listdir(sharp_path)
                blur_list = os.listdir(blur_path)

                # Builds dataframe with kaggle blur image pairs paths
                dataframe = pd.DataFrame()
                dataframe['sharp'] = sharp_list
                dataframe['sharp'] = os.path.join(sharp_path, '') + dataframe['sharp']
                dataframe['blur'] = blur_list
                dataframe['blur'] = os.path.join(blur_path, '') + dataframe['blur']

                # loads, updates and writes the new gen dataframe to the csv
                if (dataset.empty):
                    dataset = dataframe
                else:
                    dataset.append(dataframe)

            # Split dataset
            train = dataset.sample(frac=0.75, random_state=124)
            dataset = dataset.drop(train.index)
            valid = dataset.sample(frac=0.5, random_state=124)
            test = dataset.drop(valid.index)

            # Writes to storage
            train.to_csv(train_path, index=None)
            valid.to_csv(valid_path, index=None)
            test.to_csv(test_path, index=None)
        
        # Logs
        print('.csv files successfully generated')
    else:
        # Logs
        print('.csv files already generated')


if (__name__ == '__main__'):
    # Get the path to the datasets folder
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