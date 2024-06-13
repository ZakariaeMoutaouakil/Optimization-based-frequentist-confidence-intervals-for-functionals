import argparse
import ast
from time import time
from typing import List, Tuple, Dict, Callable

import pandas as pd
from cvxpy import Variable
from scipy.stats import norm

from certify.smallest_subset import smallest_subset
from distribution.final_step import final_step
from distribution.generate_quantiles import generate_quantiles
from distribution.sort_callable_values import second_largest
from lower_bound.get_quantiles import get_quantiles
from lower_bound.max_first_coordinate import max_first_coordinate
from utils.discrete_simplex import discrete_simplex

parser = argparse.ArgumentParser(description='Certify many examples')
parser.add_argument("--data", type=str, help="Location of tsv data")
parser.add_argument("--outfile", type=str, help="Location of output tsv file")
args = parser.parse_args()

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
df = pd.read_csv(args.data, sep='\t', dtype=dtype_dict, converters={'counts': ast.literal_eval})

k = 3
n = sum(df.iloc[0]['counts'])
grid = 101
alpha = 0.001
precision = 0.01
step = 0.1
sigma = 0.12

constraint_set: Tuple[Tuple[float, ...], ...] = discrete_simplex(k=k, n=grid, normalize=True)

phi: Callable[[Variable], float] = lambda p: p[1]
filter_func: Callable[[float], bool] = lambda x: x > 0
quantiles_p2 = generate_quantiles(constraint_set=constraint_set, filter_value=filter_func, func=second_largest, n=n,
                                  phi=phi, alpha=alpha, precision=precision, debug=False)
quantiles_p1 = get_quantiles(alpha=alpha, n=n, m=k, step=step)

# Dictionary to cache results and time of final_result function
final_result_cache: Dict[Tuple[int, ...], Tuple[Tuple[float, float], float]] = {}
elapsed_time, cached_time = 0., 0.

for i in range(len(df)):
    print("old:", df.iloc[i])
    counts: List[int] = df.iloc[i]['counts']
    prediction = counts.index(max(counts))
    print("counts:", counts)
    print("prediction:", prediction)
    observation = sorted(smallest_subset(vector=sorted(counts), num_partitions=k))
    reduced_counts = [int(x) for x in observation]
    reduced_counts_tuple = tuple(reduced_counts)
    print("reduced_counts:", reduced_counts)
    radius = 0.

    if reduced_counts_tuple in final_result_cache:
        radius, cached_time = final_result_cache[reduced_counts_tuple]
    else:
        start_time = time()
        p1 = max_first_coordinate(quantiles=quantiles_p1, maximum=max(reduced_counts))
        print("p1:", p1)
        p2 = 1 - p1
        print("p2:", p2)
        try:
            p2_ = final_step(constraint_set=constraint_set, quantiles=quantiles_p2, observation=reduced_counts_tuple,
                             func=second_largest, minimize=False, debug=False)
            print("p2_:", p2_)
            p2 = min(p2, p2_)
        except Exception as e:
            pass
        end_time = time()
        elapsed_time = end_time - start_time
        print("time:", elapsed_time)
        # Cache the result and time
        if p2 < p1:
            radius = 0.5 * sigma * norm.ppf(p1) - norm.ppf(p2)
        else:
            prediction = -1
        print("radius:", radius)
        final_result_cache[reduced_counts_tuple] = (radius, elapsed_time)

    df.loc[df.index[i], 'radius'] = radius
    df.loc[df.index[i], 'correct'] = int(prediction == df.iloc[i]['label'])
    df.loc[df.index[i], 'predict'] = prediction

    if reduced_counts_tuple not in final_result_cache:
        df.loc[df.index[i], 'time'] = f"{elapsed_time:.6f}"
    else:
        df.loc[df.index[i], 'time'] = f"{cached_time:.6f}"
    print("new:", df.iloc[i])

# Remove the last three columns
df_modified = df.iloc[:, :-2]  # This slices out all rows and all columns except the last two

# Save to TSV file
df_modified.to_csv(args.outfile, sep='\t',
                   index=False)  # Set index=False if you don't want to save the index as a separate column
# raw_vectors: List[List[int]] = df['counts'].to_list()
# for i in range(len(raw_vectors)):
#     print(raw_vectors[i])
#
# vectors = get_unique_vectors(vectors=raw_vectors)
# vectors = [sorted(vector) for vector in vectors]
# indices = unique_vector_indices(raw_vectors=raw_vectors, unique_vectors=vectors)
#
# print("length of vectors:", len(vectors))
# p1s: List[float] = []
# num_partitions = 3
# for vec in vectors:
#     print("vec:", vec)
#     observation = [vec[len(vec) - 1]]
#     rest = vec[:len(vec) - 1]
#     # print("rest:", rest)
#     i = smallest_subset(vector=rest, num_partitions=num_partitions - 1, debug=False)
#     # print("i:", i)
#     # print(i == len(rest) - num_partitions + 1)
#     second_class = vec[:i]
#     observation.append(sum(second_class))
#     # print("second_class:", second_class)
#     third_classes = vec[i:len(vec) - 1]
#     # print("third_classes:", third_classes)
#     observation.append(sum(third_classes))
#     observation = sorted(observation)
#     print("observation:", observation)
#     # partitions_ = partition_iterator(num_partitions=num_partitions-1, third_classes)
#     p1 = final_result(alpha=0.05, x=observation)
#     print("p1:", p1)
#     p1s.append(p1)
# for i in range(len(df)):
#     print(type(df.iloc[i]['counts'][0]))
