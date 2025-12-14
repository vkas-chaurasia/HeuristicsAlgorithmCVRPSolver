import pandas as pd
import os
from santa_challenge.utils.data_loader import load_gifts
from santa_challenge.algorithms.greedy_kd_tree import form_trips_iterative
from santa_challenge.utils.metrics import weighted_reindeer_weariness
from santa_challenge.utils.config import WEIGHT_LIMIT, SLEIGH_WEIGHT

def main():
    # Define paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Assuming gifts.csv is still in the parent directory, or we can move it to 'data/'
    # User plan said "input files (will move gifts.csv here if possible/requested)".
    # Let's check if we should look in 'data/'. If not there, look in parent.
    
    # Check local data folder first
    data_path = os.path.join(base_dir, 'data', 'gifts.csv')
    
    if not os.path.exists(data_path):
        # Fallback to parent dir if local not found (though we copied it)
        parent_data = os.path.join(base_dir, '..', 'gifts.csv')
        if os.path.exists(parent_data):
            data_path = parent_data
        
    output_path = os.path.join(base_dir, 'results', 'submission.csv')

    print(f"Loading data from {data_path}...")
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found.")
        return

    df = load_gifts(data_path)
    print(f"Loaded {len(df)} gifts.")

    print("Running Greedy KD-Tree Heuristic Solver...")
    # Solve
    trip_data = form_trips_iterative(df, weight_limit=WEIGHT_LIMIT, sleigh_weight=SLEIGH_WEIGHT)
    
    # Create DataFrame
    trip_df = pd.DataFrame(trip_data, columns=['TripId', 'GiftId'])
    
    # Merge with original data to get Lat/Long/Weight for scoring
    full_df = pd.merge(trip_df, df, on='GiftId', how='left')
    
    print("Calculating metrics (Weighted Reindeer Weariness)...")
    score = weighted_reindeer_weariness(full_df)
    print(f"Total Weighted Reindeer Weariness: {score}")

    # Prepare submission
    submission_df = trip_df[['GiftId', 'TripId']]
    submission_df['GiftId'] = submission_df['GiftId'].astype(int)
    
    # Ensure results dir exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print(f"Saving submission to {output_path}...")
    submission_df.to_csv(output_path, index=False)
    print("Done.")

if __name__ == "__main__":
    main()
