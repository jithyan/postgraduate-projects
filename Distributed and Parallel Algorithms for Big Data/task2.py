"""
Author: Jithya Nanayakkara (21329281)
"""

import time
import csv

def flatten_list(nested_list):
    """
        Un-nests a nested list.
    """
    flattened_list = []

    for sublist in nested_list:
        if sublist:
            for item in sublist:
                flattened_list.append(item)
    
    return flattened_list


def get_csv_data(filename):
    """
        Returns a list of records loaded from a CSV file, without the headers.
    """
    csv_file = open(filename)
    csv_data = csv.reader(csv_file, delimiter=",")
    return list(csv_data)[1:]


def range_partition(sorted_data, ranges, attribute, compare=lambda x,y: x <= y):
    num_partitions = len(ranges)
    partitions = []

    j = 0
    for i in range(num_partitions):
        t = []
        while (j < len(sorted_data)) and (compare(sorted_data[j][attribute], ranges[i])):
            t.append(sorted_data[j])
            j+=1

        partitions.append(t)
    
    if j < len(sorted_data):
        partitions.append(sorted_data[j:])

    return partitions


def date_comp(date1, date2):
    """
    Helper function to compart two dates in the form "dd/mm/yyyy"
    Returns True if date1 <= date2
    """

    d1 = ""
    d2 = ""

    try:
        d1 = time.strptime(date1, "%d/%m/%Y")
    except:
        d1 = time.strptime(date1, "%Y-%m-%d")

    try:
        d2 = time.strptime(date2, "%d/%m/%Y")
    except:
        d2 = time.strptime(date2, "%Y-%m-%d")
    
    if d1 == d2:
        return 0
    elif d1 < d2:
        return -1
    else:
        return 1


def h6(date, n):
    """
        Adds all the individual components of a date, and returns the mod of that with n.

        Arguments:
            date -- date with the date attribute at index 1
            n -- number of processors
        
        Returns:
            A hash value h such that: 0 <= h < n
    """
    date_parts = []
    if "/" in date:
        date_parts = [int(x) for x in date.split("/")]
    elif "-" in date:
        date_parts = [int(x) for x in date.split("-")]
    else:
        return None

    return sum(date_parts) % n


def hash_partition(data, n, h, hash_attribute):
    """
    This strategy uses the hash of a particular attribute to determine which processor a record is allocated to.
    
    Arguments:
        data -- List of records
        n -- number of processors
        h -- hashing function that takes two arguments
    """
    partitions = {}
    for record in data:
        hash_val = h(record[hash_attribute], n)
        if (hash_val not in partitions):
            partitions[hash_val] = []

        partitions[hash_val].append(record)
    
    return partitions


def hash_for_joins(date):
    date_parts = []
    if "/" in date:
        date_parts = [int(x) for x in date.split("/")]
    elif "-" in date:
        date_parts = [int(x) for x in date.split("-")]
    else:
        return None

    return sum(date_parts)


def construct_hash_table(data, hash_f, attribute_index):
    hash_table = {}
 
    for record in data:        
        key = hash_f(record[attribute_index])

        if key in hash_table:
            hash_table[key].append(record)
        else:
            hash_table[key] = [record]
    
    return hash_table


def probe_hash_table(hash_table, data, hash_f, attribute_index, ht_attribute_index, extract):
    results = []

    for record in data:
        key = hash_f(record[attribute_index])

        if key in hash_table:
            for h_rec in hash_table[key]:
                if date_comp(h_rec[ht_attribute_index], record[attribute_index]) == 0:
                    joined_record = extract(record, h_rec, record[attribute_index])
                    results.append(joined_record)

    return results


def hash_join(T1, T1_join_attribute, T2, T2_join_attribute, hash_f, extract):
    hash_table = construct_hash_table(T1, hash_f, T1_join_attribute)
    return probe_hash_table(hash_table, T2, hash_f, T2_join_attribute, T1_join_attribute, extract)


def partition_lengths(partitions):
    """
    Returns a dictionary containing the lengths of each partition in the input.
    
    Arguments:
        partitions: A list of list, or a dictionary of a hash mapped to a list.
    
    Returns:
        a dictionary. If the input is a list, the dictionary key is the index of the partition
        in the input.
        If the input is a dictionary, then the original input dictionary key is used.    
    """

    part_lens = {}

    if type(partitions) is dict:
        for h,l in partitions.items():
            part_lens[h] = len(l)

    elif type(partitions) is list:
        for i, p in enumerate(partitions):
            part_lens[i] = len(p)
    
    else:
        print("Unsupported type")
        return None
        
    return part_lens


def extract_t2q1(fire_record, climate_record, join_attribute):
    return (fire_record[7], join_attribute, [climate_record[2], climate_record[3], climate_record[5]])


def task2_joins_q1(climate_data, fire_data):
    """
    For this question, we assume that the tables have yet to be partitioned.
    Given this scenario, we adopt a disjoint partitioning method,
    where both tables are partitioned by their join attribute (date).

    Join parallelism is obtained from data partitioning and performing serial joins within
    within each processor.

    The partitioning method for each table we are using is hash partitioning (using 
    a common hash method), as from experimentiation we found the partitions obtained
    are less skewed than using ranged partitioning.
    This is because while climate data records are unique based on date,
    this is not the case for fire data, so it's difficult to ensure balanced
    load for each data set when using the same ranges.
    For disjoint partitioning based joins, round robin for both datasets would not work as it is not
    an attribute based partitioning method so the final join would be incorrect
    (the partitions need to be based on the join attribute).

    The serial join method used is hash join, which has the best performance with
    O(M+N) complexity, however the  hash table needs to fit into main memory. 
    For this reason we use the partitions of climate data for constructing the hash table
    and the larger partitions of fire data for probing.

    The benefit of this approach is that each processor works on smaller subsets of data
    to obtain speed up in the join. 
    However the drawbacks of this approach is that both data sets need to be partitioned by 
    their join attribute (however it is not an issue if the data has already been
    partitioned on the join attribute, or not yet been partitioned).
    Another drawback is that load balancing cannot be guaranteed with hash or range based partitioning.

    THE FORMAT OF THE RESULTING JOIN IS:
     (surface temperature, date, [air temperature, relative humidity, max wind speed])
    """
    n_processors = 4
    c_join_attribute = 1
    f_join_attribute = 6

    # Partition both data sets by their join attribute
    climate_partitions = hash_partition(climate_data, n_processors, h6, c_join_attribute)
    fire_partitions = hash_partition(fire_data, n_processors, h6, f_join_attribute)

    # Allocate partitions based on their key to their respective processors
    # I.e. each processor gets records from both T1 and T2 that return the same hash
    # value for their join  attribute.
    results = []
    for key in climate_partitions:
        results.append(hash_join(climate_partitions[key], c_join_attribute, fire_partitions[key], f_join_attribute, hash_for_joins, extract_t2q1))

    # Consolidate results
    return flatten_list(results)


def linear_range_search(data, attribute, start, end):
    result = []

    for i in range(len(data)):
        record = data[i]
        
        if (int(record[attribute]) >= start) and (int(record[attribute]) <= end):
                result.append(record)
    
    return result


def extract_t2q2(fire_record, climate_record, join_attribute):
    return ([fire_record[3], fire_record[5], fire_record[7]], join_attribute, climate_record[2]) 


def task2_joins_q2(climate_data, fire_data):
    """
    In this question, we assume a shared memory architecture, where the two tables have
    already been partitioned by date using hash partitioning.

    In this approach, we first filter the fire data set by searching for all the records
    that meet the confidence criteria.
    The reason why why we search first, then join is because joins are one of the most expensive
    database operations, so speed up can be obtained by reducing the number of records needed
    in the join.

    Since we assume the fire data has already been partitioned by date, we need to search 
    through all the partitions, because we're searching for confidence, which is not the attribute
    the partitioning is based on.

    The resulting subset of records  will be our new table T2.

    The already partitioned climate data will be table T1.

    With these two tables, we use use the divide and broadcast partitioning method.
    In this method, one table (T1) is partitioned and allocated to different processing
    elements, and a local join is performed in each processing element with the
    partition and the entire table T2.

    In a shared-nothing architecture, where both tables are parititioned and physically
    reside in different processing elements, the parititions of T2 will have to be replicated
    and broadcasted to every other processing element, so that they have access to T2.
    This broadcasting phase incurs a cost, however as we are assuming a shared-memory
    architecture, T2 does not need to be broadcast.

    The benefit of this approach is that if one table has already been paritioned 
    on a non-join attribute, you don't need to repartition on the join attribute 
    to perform a parallel join.

    An important factor however is that the partitioning of T1 should be 
    even, to ensure good load balancing. Ideally, round robin would achieve this.
    In our scenario, we don't care about the initial partitioning, we just know
    that they are approximately equal (in the code, we use range partitioning).

    The local join method we're using is Hash Join, as it is the most efficient
    with a worst case complexity of O(N + M) as long as the hash table can fit in
    memory. For this reason, we use the smaller dataset, the partitions of 
    climate_data, to construct the hash table, and use the larger fire_data
    to do probing.

    THE FORMAT OF THE RESULTING JOIN IS:
     ([datetime, confidence, surface temperature], date, air temperature)
    """
    n_processors = 4

    # We assume the data has previously been partitioned by some method
    # In this case, range partitioning, and resulting partitioning is almost even
    ranges = ["01/04/2017", "01/07/2017", "01/10/2017"]
    climate_partitions = range_partition(climate_data, ranges, 1, compare=date_comp)
    fire_partitions = hash_partition(fire_data, n_processors, h6, 6 )

    # Search for the subset of records that meet the confidence range <=100 and >= 80
    # As the fire data is partitioned on a non-search attribute, we have to use
    # activate all processors to perform the parallel search.
    fire_confidence_subset = []
    for id, partition in fire_partitions.items():
        fire_confidence_subset.append(linear_range_search(partition, 5, 80, 100))
    
    fire_confidence_subset = flatten_list(fire_confidence_subset)

    # Perform divide and broadcast search
    # In this case, the climate data is already partitioned and is allocated to each
    # processor. The fire data search results is sent in its entirety to each 
    # processor.
    results = []
    for partition in climate_partitions:
        results.append(hash_join(partition, 1, fire_confidence_subset, 6, hash_for_joins, extract_t2q2))

    results = flatten_list(results)
    return results


climate_data = get_csv_data("ClimateData.csv")
fire_data = get_csv_data("FireData.csv")


#r = task2_joins_q1(climate_data, fire_data)
r = task2_joins_q2(climate_data, fire_data)
# print(len(r))
# fw = open("dump5.txt", "w")

# for a in r:
#     fw.write(str(a) + "\n")

