from argparse import ArgumentParser
from ast import literal_eval
from json import dumps
from time import time
from typing import List, Tuple, Dict

from pandas import read_csv
from scipy.stats import norm

from certify.smallest_subset import smallest_subset
from lower_bound.generate_multiple_indices import generate_multiple_indices
from lower_bound.get_quantiles import get_quantiles
from lower_bound.max_first_coordinate import max_first_coordinate
from utils.logging_config import setup_logger
from utils.remove_zeros import remove_zeros

parser = ArgumentParser(description='Certify many examples')
parser.add_argument("--data", type=str, help="Location of tsv data", required=True)
parser.add_argument("--outfile", type=str, help="Location of output tsv file", required=True)
parser.add_argument("--log", type=str, help="Location of log file", required=True)
parser.add_argument("--k", type=int, default=3, help="Number of coordinates")
parser.add_argument("--step", type=float, default=0.001, help="Step size")
parser.add_argument("--alpha", type=float, default=0.001, help="Failure probability")
parser.add_argument("--sigma", type=float, default=0.12, help="Noise parameter")
args = parser.parse_args()

logger = setup_logger("certification", args.log)

# Use pprint to log the arguments in a more readable format
logger.info("Parsed arguments:")
args_dict = vars(args)

# Pretty print the dictionary with json.dumps
formatted_args = dumps(args_dict, indent=4)

# Log the formatted arguments
logger.info(formatted_args)

# Define the data types for each column
dtype_dict = {
    'idx': int,
    'label': int,
    'predict': int,
    'radius': float,
    'correct': int,
    'time': str
}

# Read the preprocessed TSV data into a DataFrame with specified dtypes
df = read_csv(args.data, sep='\t', dtype=dtype_dict, converters={'counts': literal_eval})

n = sum(df.iloc[0]['counts'])
logger.info("n: " + str(n))

indices_p1 = generate_multiple_indices(maximum=n, dimension=args.k, n=n)
logger.debug("indices_p1: " + str(indices_p1))
quantiles_p1 = get_quantiles(alpha=args.alpha, n=n, m=args.k, step=args.step, indices=indices_p1)
logger.debug("quantiles_p1: " + str(quantiles_p1))

# Dictionary to cache results and time of final_result function
final_result_cache: Dict[Tuple[int, ...], Tuple[Tuple[float, float], float]] = {}
elapsed_time, cached_time = 0., 0.

for i in range(len(df)):
    logger.info("old:")
    logger.info(df.iloc[i])
    counts: List[int] = df.iloc[i]['counts']
    prediction = counts.index(max(counts))
    reduced_counts = remove_zeros(coords=tuple(counts), min_dimension=args.k)
    logger.debug("reduced_counts: " + str(reduced_counts))
    observation = sorted(smallest_subset(vector=reduced_counts, num_partitions=args.k))
    reduced_counts_tuple = tuple(int(x) for x in observation)
    logger.debug("reduced_counts_tuple: " + str(reduced_counts_tuple))
    radius = 0.

    if reduced_counts_tuple in final_result_cache:
        radius, cached_time = final_result_cache[reduced_counts_tuple]
    else:
        start_time = time()
        p1 = max_first_coordinate(quantiles=quantiles_p1, maximum=max(reduced_counts_tuple))
        logger.debug("p1: " + str(p1))
        end_time = time()
        elapsed_time = end_time - start_time
        logger.info("elapsed_time: " + str(elapsed_time))
        if p1 > 0.5:
            radius = args.sigma * norm.ppf(p1)
        else:
            prediction = -1
            logger.warning("Don't certify this example")
        # Cache the result and time
        final_result_cache[reduced_counts_tuple] = (radius, elapsed_time)

    logger.debug("radius: " + str(radius))
    logger.debug("prediction: " + str(prediction))
    df.loc[df.index[i], 'radius'] = radius
    df.loc[df.index[i], 'correct'] = int(prediction == df.iloc[i]['label'])
    df.loc[df.index[i], 'predict'] = prediction

    if reduced_counts_tuple not in final_result_cache:
        df.loc[df.index[i], 'time'] = f"{elapsed_time:.6f}"
    else:
        df.loc[df.index[i], 'time'] = f"{cached_time:.6f}"
    logger.info("new:")
    logger.info(df.iloc[i])

# Remove the last three columns
df_modified = df.iloc[:, :-2]  # This slices out all rows and all columns except the last two

# Save to TSV file
df_modified.to_csv(args.outfile, sep='\t',
                   index=False)  # Set index=False if you don't want to save the index as a separate column
