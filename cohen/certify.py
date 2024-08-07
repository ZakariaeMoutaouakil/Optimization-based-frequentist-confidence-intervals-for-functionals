# evaluate a smoothed classifier on a dataset
import argparse
import datetime
from json import dumps
from time import time

import torch

from architectures import get_architecture
from core import Smooth
from datasets import get_dataset, DATASETS, get_num_classes
from utils.logging_config import setup_logger

parser = argparse.ArgumentParser(description='Certify many examples')
parser.add_argument("--dataset", choices=DATASETS, help="which dataset")
parser.add_argument("--base_classifier", type=str, help="path to saved pytorch model of base classifier")
parser.add_argument("--sigma", type=float, help="noise hyperparameter")
parser.add_argument("--outfile", type=str, help="output file")
parser.add_argument("--batch", type=int, default=1000, help="batch size")
parser.add_argument("--max", type=int, default=-1, help="stop after this many examples")
parser.add_argument("--split", choices=["train", "test"], default="test", help="train or test set")
parser.add_argument("--N0", type=int, default=100)
parser.add_argument("--N", type=int, default=100000, help="number of samples to use")
parser.add_argument("--alpha", type=float, default=0.001, help="failure probability")
parser.add_argument("--log", type=str, help="Location of log file")
args = parser.parse_args()

logger = setup_logger("cohen certification", args.log)
args_dict = vars(args)

# Pretty print the dictionary with json.dumps
formatted_args = dumps(args_dict, indent=4)

# Log the formatted arguments
logger.info(formatted_args)

if __name__ == "__main__":
    # load the base classifier
    checkpoint = torch.load(args.base_classifier, map_location=torch.device('cuda'))
    # checkpoint = torch.load(args.base_classifier, map_location=torch.device('cpu'))
    base_classifier = get_architecture(checkpoint["arch"], args.dataset)
    base_classifier.load_state_dict(checkpoint['state_dict'])

    # create the smoothed classifier g
    smoothed_classifier = Smooth(base_classifier, get_num_classes(args.dataset), args.sigma)

    # prepare output file
    f = open(args.outfile, 'w')
    print("idx\tlabel\tpredict\tradius\tcorrect\ttime\tcounts\tprediction", file=f, flush=True)

    # iterate through the dataset
    dataset = get_dataset(args.dataset, args.split)
    for i in range(len(dataset)):
        if i == args.max:
            break

        x, label = dataset[i]

        before_time = time()
        # certify the prediction of g around x
        x = x.cuda()
        prediction, radius, counts_estimation, cAHat = smoothed_classifier.certify(x, args.N0, args.N, args.alpha,
                                                                                   args.batch)
        after_time = time()
        correct = int(prediction == label)
        counts_estimation = '[' + ', '.join(map(str, counts_estimation)) + ']'
        time_elapsed = str(datetime.timedelta(seconds=(after_time - before_time)))
        print("{}\t{}\t{}\t{:.3}\t{}\t{}\t{}\t{}".format(
            i, label, prediction, radius, correct, time_elapsed, counts_estimation, cAHat), file=f, flush=True)

    f.close()
