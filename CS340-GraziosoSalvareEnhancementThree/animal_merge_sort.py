'''This merge sort will sort the animal records that the dashboard had already loaded into Python'''

import math

# These will be the only fields that a user can choose for sorting
sort_fields = ("age_upon_outcome_in_weeks", "name", "breed")

def merge_sort(records, field, descending=False): # Merge Sort algorithm has a O(n log n) time complexity
    ''' Returns a sorted copy of the animal records. Records that are missing or have issues go last. Records with the same values stay in the original order'''

    if field not in sort_fields:
        raise ValueError("Sort field has to be either age, name, or breed") # Raise causes an error if it receives a value not wanted

    if not isinstance(descending, bool): # Check if it is the wanted data
        raise ValueError("Descending must be withere True or False")

    def value_for(record):
        '''Get value to compare with another record'''
        value = record.get(field)

        if field == "age_upon_outcome_in_weeks":
            # Age has to be a number. Missing age, string, bool, or NaN can't be sorted like normal so it will be treated as missing
            if isinstance(value, bool):
                return None

            if not isinstance(value, (int, float)):
                return None

            if math.isnan(value):
                return None

            return value

        # Names and breeds have to have correct text
        if not isinstance(value, str) or not value.strip():
            return None

        # Removes whitespace and ignores capitals
        return value.strip().casefold()

    def left_first(left_record, right_record):
        '''Figures out what two records should be added next'''

        left_value = value_for(left_record)
        right_value = value_for(right_record)

        # Missing value should remain at end
        if left_value is None:
            return right_value is None

        if right_value is None:
            return True

        if descending:
            # The bigger value goes first when descending. Using >= keeps equal records in the original order
            return left_value >= right_value
        
        # Smaller value goes first when ascending. Using <= keeps equal records in original order
        return left_value <= right_value

    def sort(items):
        '''Recursively divide and merge'''

        # A list that has zero or only one record is already sorted
        if len(items) <= 1:
            return items

        # Find middle and divide the list into two smaller lists
        middle = len(items) // 2
        left = sort(items[:middle])
        right = sort(items[middle:])

        merged = []
        left_index = 0
        right_index = 0

        # Compare what is unused from each half of the sorted list
        while left_index < len(left) and right_index < len(right):
            if left_first(left[left_index], right[right_index]):
                merged.append(left[left_index])
                left_index += 1
            else:
                merged.append(right[right_index])
                right_index += 1

        # One side might still have records. Those records will be sorted so add them at end
        merged.extend(left[left_index:])
        merged.extend(right[right_index:])

        return merged

    # list(records) creates copy
    # original list that was supplied to the function is not reorganized
    return sort(list(records))