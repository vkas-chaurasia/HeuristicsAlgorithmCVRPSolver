import pandas as pd
from sklearn.neighbors import KDTree
from ..utils.config import NORTH_POLE, SLEIGH_WEIGHT, WEIGHT_LIMIT

def form_trips_iterative(df, weight_limit=WEIGHT_LIMIT, sleigh_weight=SLEIGH_WEIGHT):
    """
    Forms trips iteratively using a greedy nearest neighbor approach with KDTree.
    
    Args:
        df (pd.DataFrame): DataFrame containing gift data (Latitude, Longitude, Weight, GiftId).
        weight_limit (float): Maximum weight for a trip.
        sleigh_weight (float): Base weight of the sleigh.
        
    Returns:
        list: A list of tuples (TripId, GiftId).
    """
    coordinates = df[['Latitude', 'Longitude']].values
    tree = KDTree(coordinates, metric='euclidean')
    
    visited = set()  # Track visited cities
    trip_data = []  # List to store TripId and GiftId
    trip_counter = 1  # Start with trip 1

    current_location = NORTH_POLE   # Start from the North Pole

    # unvisited_cities = set() # (From notebook, unused in logic but present)
    
    k_neighbours = 9000

    print("Starting trip generation...")

    while len(visited) < len(df):
        total_weight = 0
        trip = []  # List to store cities in the current trip

        while total_weight <= weight_limit:

            next_index = None
            
            while next_index is None:

            # Query the KD-Tree to find the nearest unvisited city
                dist, ind = tree.query([current_location], k=k_neighbours)  # Find k nearest neighbors
                
                # Check neighbors
                for i, idx in enumerate(ind[0]):
                    if idx not in visited:
                        next_index = idx
                        break
                
                # If no unvisited neighbor found, increase k
                if next_index is None:
                    k_neighbours += 3000
                    if k_neighbours >= len(df):
                        break
                    print(f"k_neighbours increased to: {k_neighbours}")
                        
            # If still None (covered all points), break
            if next_index is None:
                break

            # Fetch gift details
            gift = df.iloc[next_index]
            gift_weight = gift['Weight']

            # Check if adding this city exceeds the weight limit
            if total_weight + gift_weight > weight_limit:
                break  # If it exceeds, end this trip

            # Add this gift to the current trip
            trip.append(next_index)
            total_weight += gift_weight
            visited.add(next_index)
            # unvisited_cities.discard(next_index)

            # Store TripId and GiftId
            trip_data.append((trip_counter, gift['GiftId']))

            # Update current location to the new city
            current_location = (gift['Latitude'], gift['Longitude'])


        # Once the current trip is completed, go to the next trip
        # print(f"trip: {trip_counter}") # Reduced verbosity
        if trip_counter % 100 == 0:
            print(f"Completed trip: {trip_counter}")
            
        trip_counter += 1
        
        # Reset current location to North Pole for new trip? 
        # The notebook code does NOT explicitly reset current_location to North Pole after the inner loop breaks.
        # It breaks the inner loop when weight limit is hit.
        # However, the loop `while total_weight <= weight_limit` finishes.
        # Then `trip_counter += 1`.
        # Then the outer loop `while len(visited) < len(df)` continues.
        # `total_weight` is reset to 0. `trip` is reset.
        # BUT `current_location` remains at the last visited city of the previous trip?
        # Let's check the notebook logic carefully.
        # In the notebook: `current_location` is updated inside the inner loop.
        # When inner loop breaks (trip full), it goes to outer loop.
        # Next iteration of outer loop starts a new trip.
        # It queries KDTree from `current_location`.
        # Is the sleigh flying from the last dropoff location to the next pickup?
        # Typically Santa goes back to North Pole to refill.
        # If the algorithm queries from `current_location` (last dropoff), it assumes Santa picks up gifts from there?
        # That doesn't make sense physically if he has to reload.
        # BUT I must faithfully reproduce the notebook's algorithm as requested ("how algorithm was implemented").
        # In the notebook, `current_location` is NOT reset to North Pole in the outer loop.
        # Wait, usually `weighted_trip_length` adds North Pole as start and end.
        # If the *construction* algorithm assumes start from last point, it might be an optimization or a bug in the notebook.
        # Let's look at the notebook again.
        # outer loop: `while len(visited) < len(df):`
        #   `total_weight = 0`
        #   `trip = []`
        #   inner loop `while total_weight <= weight_limit:`
        #      ... query from `current_location`
        #      ... update `current_location`
        #
        # Yes, it implies the next trip starts from where the previous one ended?
        # Or maybe the first point of the new trip is found relative to the last point of the old trip?
        # But `weighted_trip_length` calculates distance from North Pole for the first point?
        # `weighted_trip_length` implementation:
        # `tuples = [tuple(x) for x in stops.values]`
        # `tuples.append(north_pole)`
        # `prev_stop = north_pole`
        # `for location, weight in zip(tuples, weights):` (iterates through stops)
        # So WRW calculation assumes each trip starts at North Pole.
        # But the *generation* might be using the last location.
        # If I change it, I change the algorithm.
        # The user asked: "make it python and also describe how alogirhtm was implemented etc"
        # So I should keep it as is, and maybe note it in the description if it looks odd.
        # BUT, if `current_location` is not reset, the first gift of the NEW trip is chosen based on proximity to the LAST gift of the OLD trip.
        # However, since the sleigh MUST go to North Pole to refill (which is implicit in starting a new trip), searching near the last dropoff might be suboptimal if the last dropoff is far from North Pole?
        # Or maybe it's efficient if we want to cluster sectors?
        # Actually, `weighted_trip_length` costs: `haversine(location, prev_stop) * prev_weight`.
        # `prev_stop` starts at North Pole.
        # So the first gift of the trip should be close to North Pole?
        # If we query from the last dropoff of previous trip (which could be in Antarctica), we might pick a neighbor in Antarctica.
        # Then the new trip starts: North Pole -> Antarctica. High cost!
        # This looks like a bug in the notebook or a specific strategy (e.g. sweeping).
        # Let's check if the notebook resets it.
        # I read lines 1567-1636.
        # I don't see `current_location = north_pole` inside the outer loop.
        # I see `current_location = north_pole` BEFORE the outer loop (line 1572).
        # So I will strictly follow the notebook.

    print(f"Final k: {k_neighbours}")
    return trip_data
