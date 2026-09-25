"""Compare merge sort and bubble sort"""
'''Will create artifical animal records, sort them by age with both sorts, check that they get the same result, and display the median run time from five runs'''

import random 
from statistics import median
from time import perf_counter
from animal_merge_sort import merge_sort

age_field = "age_upon_outcome_in_weeks"

# Repeating each measurement 5 times
time_runs = 5

def bubble_sort(records):
    '''Returns new list holding the records in ascending order. 
    Bubble sort repeatedly compares surrounding records and swaps them if they're out of order. After a pass
    the biggest value in the unsorted area goes to the final position near the end'''

    sorted_records = list(records)

    # One less pass is enough to sort
    for pass_number in range(len(sorted_records) - 1):
        # The final value from the previous passes are in the correct positions so don't need to be compared again
        last_comparison = len(sorted_records) - 1 - pass_number

        for index in range(last_comparison):
            current_age = sorted_records[index][age_field]
            next_age = sorted_records[index + 1][age_field]

            # Move the older animal to the right once
            if current_age > next_age:
                sorted_records[index], sorted_records[index + 1] = (
                    sorted_records[index + 1],
                    sorted_records[index],
                )
    return sorted_records

def merge_sort_by_age(records):
    # Returns records sorted by age using the merge sort
    return merge_sort(records, age_field)

def measure_time(sort_function, records):
    '''Returns the median execution time in milliseconds. It will be ran multiple times with the same input. Both sorting functions will return a new list so each run will get records in the same original order'''
    recorded_times = []

    for blank in range(time_runs):
        start_time = perf_counter()
        sort_function(records)
        end_time = perf_counter()

        # perf_counter records in seconds so to get milliseconds multiply by 1,000
        passed_milliseconds = (end_time - start_time) * 1000
        recorded_times.append(passed_milliseconds)

    return median(recorded_times)

if __name__ == "__main__":
    # Fixed seed to ensure the test of data. Running it again will produce the same organization of animal ages
    random.seed(499) # makes it reproducable

    print("Artifical animal by age sorting")
    print(f"Median of {time_runs} runs in milliseconds")
    print("Records | Merge sort | Bubble sort")\
    # Test will happen on increasing inputs to show how the algorithms handle scale
    for size in (200, 800, 1500): 
        records = []

        # Build artifical animal records. The ID will match the records while the randomly generated age is the value being sorted
        for record_number in range(size):
            record = {
                "id": record_number,
                age_field: random.randint(4, 300), # minum and maximum ages
            }
            records.append(record)

        # Making sure it is correct before comparingperformance. If it isn't then it is stopped
        merge_result = merge_sort_by_age(records)
        bubble_result = bubble_sort(records)
        assert merge_result == bubble_result # Check to see if both algoritms produce the same order

        # Time the algorithms take
        merge_time = measure_time(merge_sort_by_age, records)
        bubble_time = measure_time(bubble_sort, records)

        print(f"{size:7} | " f"{merge_time:10.3f} | " f"{bubble_time:11.3f}") # Gives minimum width of rcharacters and set the decimal points           
