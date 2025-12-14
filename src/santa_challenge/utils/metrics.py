from haversine import haversine
from .config import NORTH_POLE, SLEIGH_WEIGHT

def weighted_trip_length(stops, weights):
    """
    Calculates the weighted trip length for a single trip.
    
    Args:
        stops (pd.DataFrame): DataFrame containing Latitude and Longitude.
        weights (list): List of weights for the gifts.
        
    Returns:
        float: The weighted length of the trip.
    """
    tuples = [tuple(x) for x in stops.values]
    tuples.append(NORTH_POLE)  # Add North Pole as return
    
    # We work with a local copy of weights to avoid modifying the input inplace if it's a list
    current_weights = weights.copy()
    current_weights.append(SLEIGH_WEIGHT)  # Add sleigh weight

    dist = 0.0
    prev_stop = NORTH_POLE
    prev_weight = sum(current_weights)
    
    for location, weight in zip(tuples, current_weights):
        dist += haversine(location, prev_stop) * prev_weight
        prev_stop = location
        prev_weight -= weight
    return dist

def weighted_reindeer_weariness(all_trips):
    """
    Calculates the total weighted reindeer weariness for all trips.
    
    Args:
        all_trips (pd.DataFrame): DataFrame containing TripId, Latitude, Longitude, and Weight.
        
    Returns:
        float: Total weighted weariness.
    """
    uniq_trips = all_trips.TripId.unique()
    total_dist = 0.0
    for trip_id in uniq_trips:
        this_trip = all_trips[all_trips.TripId == trip_id]
        total_dist += weighted_trip_length(this_trip[['Latitude', 'Longitude']], this_trip.Weight.tolist())
    return total_dist
