import os
import torch
import argparse
from opacus.accountants.utils import get_noise_multiplier
from opacus.accountants import create_accountant

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--target_epochs", type=int, default=20, help="Number of epochs for running noise multiplier()")
    parser.add_argument("--target_delta", type=float, default=1e-10, help="Target delta for the experiment")
    args = parser.parse_args()
    
    # other hypers for grid search
    n_data = 500
    target_epsilons = [0.1,1,2,3,4,5,6,7,8,9,10]
    batch_size = [i for i in range(5,105,5)]

    for eps in target_epsilons:
        for num_batches in batch_size:
            expected_len_dataloader = n_data // num_batches
            sample_rate = 1/expected_len_dataloader
            print("--------------------------------------------------------------------------")
            print("SETTING: epsilon = {}, batch size = {}, epochs = {}, delta = {}".format(eps,
                                                                                           num_batches, 
                                                                                           args.target_epochs, 
                                                                                           args.target_delta))            
            noise_sigma = get_noise_multiplier(
                        target_epsilon = eps,
                        epochs = args.target_epochs,
                        target_delta = args.target_delta,
                        sample_rate = sample_rate,    
                        steps = None,
                        accountant = "prv",
                        epsilon_tolerance = 0.01)
            
            print("Optimal noise = {}.".format(noise_sigma))
            print("--------------------------------------------------------------------------")

if __name__=="__main__":
    main()