import argparse
import glob
import os
import argparse
import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from pathlib import Path
from matplotlib import pyplot as plt
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score

# define functions
def main(args):

    # TO DO: enable autologging
    mlflow.sklearn.autolog()

    if not os.path.exists(args.evaluation_output_folder):
        os.makedirs(args.evaluation_output_folder)

    # read data
    df = get_csvs_df(args.test_data_folder)

    X = df[['Pregnancies', 'PlasmaGlucose', 'DiastolicBloodPressure',
            'TricepsThickness', 'SerumInsulin', 'BMI', 'DiabetesPedigree',
            'Age']]
    y = df['Diabetic']

    model = mlflow.sklearn.load_model(args.model)

    yhat_test, score = model_evaluation(
        X, y, model, args.evaluation_output_folder)


def model_evaluation(X_test, y_test, model, evaluation_output):

    # Get predictions to y_test (y_test)
    yhat_test = model.predict(X_test)

    # Save the output data with feature columns, predicted cost, and actual cost in csv file
    output_data = X_test.copy()
    output_data["real_label"] = y_test
    output_data["predicted_label"] = yhat_test
    output_data.to_csv((Path(evaluation_output) / "predictions.csv"))

    # Evaluate Model performance with the test set
    accuracy = accuracy_score(y_test, yhat_test)
    precision = precision_score(y_test, yhat_test)
    recall = recall_score(y_test, yhat_test)
    f1 = f1_score(y_test, yhat_test)

    (Path(evaluation_output) / "accuracy.txt").write_text(
        f"{accuracy:.2f}"
    )

    # Print score report to a text file
    (Path(evaluation_output) / "score.txt").write_text(
        f"Scored with the following model:\n{format(model)}"
    )
    with open((Path(evaluation_output) / "score.txt"), "a") as outfile:
        outfile.write(f"\nAccuracy: {accuracy:.2f} \n")
        outfile.write(f"Precision: {precision:.2f} \n")
        outfile.write(f"Recall: {recall:.2f} \n")
        outfile.write(f"F1 score: {f1:.2f} \n")

    mlflow.log_metric("test Accuracy", accuracy)
    mlflow.log_metric("test Precision", precision)
    mlflow.log_metric("test Recall", recall)
    mlflow.log_metric("test f1_score", f1)

    # Visualize results
    plt.scatter(y_test, yhat_test, color='black')
    plt.plot(y_test, y_test, color='blue', linewidth=3)
    plt.xlabel("Real value")
    plt.ylabel("Predicted value")
    plt.title("Comparing Model Classification to Real values - Test Data")
    plt.savefig(Path(evaluation_output) / "classifications.png")

    # To look at mlflow
    mlflow.log_artifact(Path(evaluation_output) / "classifications.png")

    return yhat_test, f1


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
    parser.add_argument("--model", dest='model',
                        type=str)
    parser.add_argument("--test_data_folder", dest='test_data_folder',
                        type=str)
    parser.add_argument("--evaluation_output_folder", dest='evaluation_output_folder',
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