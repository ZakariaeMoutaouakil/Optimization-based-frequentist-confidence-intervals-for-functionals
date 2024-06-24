from argparse import ArgumentParser
from ast import literal_eval
from time import time
from typing import List, Tuple, Dict

import pandas as pd
from scipy.stats import norm

from certify.smallest_subset import smallest_subset
from higher_bound.get_quantiles import get_quantiles as get_quantiles_p2
from lower_bound.generate_multiple_indices import generate_multiple_indices
from lower_bound.get_quantiles import get_quantiles as get_quantiles_p1
from lower_bound.max_first_coordinate import max_first_coordinate
from utils.logging_config import setup_logger
from utils.remove_zeros import remove_zeros

parser = ArgumentParser(description='Certify many examples')
parser.add_argument("--data", type=str, help="Location of tsv data", required=True)
parser.add_argument("--outfile", type=str, help="Location of output tsv file", required=True)
parser.add_argument("--log", type=str, help="Location of log file", required=True)
parser.add_argument("--k", type=int, default=3, help="Number of coordinates")
parser.add_argument("--step", type=float, default=0.01, help="Step size")
parser.add_argument("--precision", type=float, default=0.01, help="Precision")
parser.add_argument("--alpha", type=float, default=0.001, help="Failure probability")
parser.add_argument("--beta", type=float, default=0.9, help="Ratio of failure probability")
parser.add_argument("--grid", type=int, default=101, help="Grid size")
parser.add_argument("--sigma", type=float, default=0.12, help="Noise parameter")
args = parser.parse_args()

logger = setup_logger("certification", args.log)
logger.info(args)

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
df = pd.read_csv(args.data, sep='\t', dtype=dtype_dict, converters={'counts': literal_eval})

n = sum(df.iloc[0]['counts'])
logger.info("n: " + str(n))
indices_p1 = generate_multiple_indices(maximum=n, dimension=args.k, n=n)
logger.debug("indices_p1: " + str(indices_p1))
beta = args.beta * args.alpha
logger.info("beta: " + str(beta))
quantiles_p1 = get_quantiles_p1(alpha=beta, n=n, m=args.k, step=args.step, indices=indices_p1)
logger.debug("quantiles_p1: " + str(quantiles_p1))
gamma = (1 - args.beta) * args.alpha / (1 - args.beta * args.alpha)
logger.info("gamma: " + str(gamma))

S = max(set(sum(sorted(df.iloc[i]['counts'])[:-1]) for i in range(len(df))))
logger.debug("S: " + str(S))
quantiles_p2 = {}
for s in range(S + 1):
    indices_p2 = generate_multiple_indices(maximum=s, dimension=args.k - 1, n=s)
    logger.debug("indices_p2: " + str(indices_p2))
    quantiles_p2_s = get_quantiles_p2(alpha=gamma, n=s, m=args.k - 1, step=args.step, indices=indices_p2)
    logger.debug(f"quantiles_p2_{s}: " + str(quantiles_p2_s))
    quantiles_p2[s] = quantiles_p2_s

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
        y = reduced_counts_tuple[:- 1]
        logger.debug("y: " + str(y))
        q = max_first_coordinate(quantiles=quantiles_p2[max(y)], maximum=max(y))
        p2 = q * (1 - p1)
        logger.debug("p1: " + str(p1))
        logger.debug("q : " + str(q))
        logger.debug("p2: " + str(p2))
        logger.debug("1-p1: " + str(1 - p1))
        end_time = time()
        elapsed_time = end_time - start_time
        logger.info("elapsed_time: " + str(elapsed_time))
        if p2 < p1:
            radius = 0.5 * args.sigma * (norm.ppf(p1) - norm.ppf(p2))
            logger.debug("Certify this example")
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
