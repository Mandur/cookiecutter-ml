import argparse
import glob
import os

import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split


# define functions
def main(args):

    # TO DO: enable autologging
    mlflow.sklearn.autolog()

    # read data
    df = get_csvs_df(args.raw_data)

    # split the raw dataset into train and test data
    train_data = df.sample(frac=0.75)   
    test_data = df.drop(train_data.index)

    if not os.path.exists(args.train_data_folder):
        os.makedirs(args.train_data_folder)
    if not os.path.exists(args.test_data_folder):
        os.makedirs(args.test_data_folder)

    # save the train and test data as csv files
    train_data.to_csv(args.train_data_folder+'/train_data.csv',index=False)
    test_data.to_csv(args.test_data_folder+'/test_data.csv',index=False)


def get_csvs_df(path):
    if not os.path.exists(path):
        raise RuntimeError(f"Cannot use non-existent path provided: {path}")
    csv_files = glob.glob(f"{path}/*.csv")
    if not csv_files:
        raise RuntimeError(f"No CSV files found in provided data path: {path}")
    return pd.concat((pd.read_csv(f) for f in csv_files), sort=False)


def parse_args():
    # setup arg parser
    parser = argparse.ArgumentParser()

    # add arguments
    parser.add_argument("--raw_data", dest='raw_data',
                        type=str)
    parser.add_argument("--train_data_folder", dest='train_data_folder',
                        type=str)
    parser.add_argument("--test_data_folder", dest='test_data_folder',
                        type=str)

    # parse args
    args = parser.parse_args()

    # return args
    return args


# run script
if __name__ == "__main__":
    # add space in logs
    print("\n\n")
    print("*" * 60)

    # parse args
    args = parse_args()

    # run main function
    main(args)

    # add space in logs
    print("*" * 60)
    print("\n\n")