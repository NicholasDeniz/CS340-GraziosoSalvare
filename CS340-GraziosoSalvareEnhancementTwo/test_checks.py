from animal_merge_sort import merge_sort

# Set of records made for testing
animals = [
    {
        "id": "1",
        "age_upon_outcome_in_weeks": 5,
        "name": " Drake  ",
        "breed": "Beagle"
    },
    {
        "id": "2",
        "age_upon_outcome_in_weeks": 8,
        "name": "DRAKE",
        "breed": "  Terrier "
    },
    {
        "id": "3",
        "age_upon_outcome_in_weeks": 10,
        "name": "Bill",
        "breed": "BEAGLE"
    },
    {
        "id": "4" # # Missing age, breed, and name
    },
    {
        "id": "5",
        "age_upon_outcome_in_weeks": "test",
        "name": " ",
        "breed": " "
    },
]

# Saves copies to check that sorting didn't change them
original = []

for animal in animals:
    original.append(animal.copy())

# Runs a sorting check
def check_sort(label, field, descending, expected):
    result = merge_sort(animals, field, descending)

    # Gets IDs in the order returned from merge sort
    actual = []

    for animal in result:
        actual.append(animal["id"])

    # Checks the order and make complete sure that a new list was returned
    if actual == expected and result is not animals:
        print(label + ": Pass")
    else:
        print(label + ": Fail")
        print("Expected", expected)
        print("Gotten:", actual)

# False is ascending while descending is True
check_sort(
    "Age ascending",
    "age_upon_outcome_in_weeks",
    False,
    ["1", "2", "3", "4", "5"]
)

check_sort(
    "Age descending",
    "age_upon_outcome_in_weeks",
    True,
    ["3", "2", "1", "4", "5"]
)

check_sort(
    "Name ascending",
    "name",
    False,
    ["3", "1", "2", "4", "5"]
)

check_sort(
    "Name descending",
    "name",
    True,
    ["1", "2", "3", "4", "5"]
)

check_sort(
    "Breed ascending",
    "breed",
    False,
    ["1", "3", "2", "4", "5"]
)

check_sort(
    "Breed descending",
    "breed",
    True,
    ["2", "1", "3", "4", "5"]
)

# Check the original records stayed the same
if animals == original:
    print("Original records unchanged: Pass")
else:
    print("Original records unchanged: Fail")