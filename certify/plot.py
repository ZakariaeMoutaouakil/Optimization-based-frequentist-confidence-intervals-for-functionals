from argparse import ArgumentParser

import matplotlib.pyplot as plt  # Importing matplotlib library for plotting
import numpy as np  # Importing numpy library for numerical operations
import pandas as pd  # Importing pandas library for data manipulation

from utils.logging_config import setup_logger

parser = ArgumentParser(description='Certify many examples')
parser.add_argument("--files", type=str, nargs='+', help="List of tsv files", required=True)
parser.add_argument("--labels", type=str, nargs='+', help="List of labels", required=True)
parser.add_argument("--log", type=str, help="Location of log file", required=True)
parser.add_argument("--plot", type=str, help="Save path of plot")
args = parser.parse_args()

logger = setup_logger("plot", args.log)
logger.info(args)


def process_file(file_path):
    """Load and process the dataset to calculate certified accuracy for various radii."""
    # Load the dataset
    df = pd.read_csv(file_path, delimiter='\t')  # Reading the dataset from the specified file path

    # Filter rows where the prediction is correct
    df_correct = df[df['correct'] == 1]  # Filtering the dataframe to include only correct predictions

    # Sort by radius
    df_correct = df_correct.sort_values(by='radius')  # Sorting the filtered dataframe by the 'radius' column

    # Unique radius values in the dataset
    unique_radii = np.sort(df_correct['radius'].unique())  # Extracting unique radius values from the sorted dataframe

    # Calculate the certified accuracy at each unique radius
    certified_accuracies = []  # List to store certified accuracies
    for r in unique_radii:
        certified_count = len(df_correct[df_correct['radius'] >= r])  # Counting certified predictions for each radius
        certified_accuracy = certified_count / len(df)  # Calculating certified accuracy
        certified_accuracies.append(certified_accuracy)  # Appending certified accuracy to the list

    # Append a final point projecting the curve to the x-axis
    if len(unique_radii) > 0:
        last_r = unique_radii[-1]  # Extracting the last radius value
        unique_radii = np.append(unique_radii, last_r + 0.01)  # Adding a small increment to project the curve
        certified_accuracies.append(0)  # Appending 0 to certified accuracies for the final point

    return unique_radii, certified_accuracies  # Returning unique radii and certified accuracies


def plot_multiple_files(file_paths, labels, save_path=None):
    """Plot certified accuracy curves from multiple files in the same figure."""
    plt.figure(figsize=(12, 8))  # Creating a new figure with specified size

    for i, (file_path, label) in enumerate(zip(file_paths, labels)):
        unique_radii, certified_accuracies = process_file(file_path)  # Processing each file

        plt.plot(unique_radii, certified_accuracies, linestyle='-', label=label)  # Plotting certified accuracy curve

    plt.xlabel('Radius (r)')  # Setting the label for x-axis
    plt.ylabel('Certified Accuracy')  # Setting the label for y-axis
    plt.title('Certified Accuracy in Terms of Radius')  # Setting the title of the plot
    plt.legend()  # Displaying legend
    plt.grid(False)  # Removing the grid lines from the plot

    # Save the plot if save_path is provided
    if save_path:
        plt.savefig(save_path)  # Saving the plot to the specified path
    else:
        plt.show()  # Displaying the plot


# Example usage with multiple files
plot_multiple_files(args.files, args.labels, args.plot)  # Calling the function to plot the certified accuracy curves
