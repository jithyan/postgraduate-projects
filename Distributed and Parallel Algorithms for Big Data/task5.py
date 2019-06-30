"""
Author: Jithya Nanayakkara (21329281)
"""

import csv
import time

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


def hash_for_joins(date):
    date_parts = []
    if "/" in date:
        date_parts = [int(x) for x in date.split("/")]
    elif "-" in date:
        date_parts = [int(x) for x in date.split("-")]
    else:
        return None

    return sum(date_parts)


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


def hash_groupby(val, n):
    str_ascii_parts = [ord(char) for char in val]
    return sum(str_ascii_parts) % n


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


def get_csv_data(filename):
    """
        Returns a list of records loaded from a CSV file, without the headers.
    """
    csv_file = open(filename)
    csv_data = csv.reader(csv_file, delimiter=",")
    return list(csv_data)[1:]


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


def extract_t5(fire_record, climate_record, join_attribute):
    return (climate_record[0], fire_record[7])


def join_groupby(partition, partition_join_attribute, table, table_join_attribute):
    joined_result = hash_join(partition, partition_join_attribute, table, table_join_attribute, hash_for_joins, extract_t5)
    return avg_agg(joined_result, 0, 1)


def avg_agg(data, group_index, val_index):
    """
    Finds the average value of the given group.

    Arguments:
        data -- list of records
        group_index -- index of the attribute value to use as the group/category
        val_index -- index of the attribute value to average 
    """
    temp = {}
    final_result = {}

    for record in data:
        key = record[group_index]
        val = int(record[val_index])

        if key in temp:
            temp[key].append(val)
        else:
            temp[key] = [val]
    
    for key, vals in temp.items():
        final_result[key] = sum(vals) / len(vals)

    return final_result


def task5(climate_data, fire_data):
    """
    In this task, we assume a shared memory architecture, with both tables yet to 
    be partitioned.

    The group-by attribute is station and the join attribute is date.
    As the group-by and join attributes are different, a join-first-then-group-by parallel
    approach is taken.

    The specific approach used is GroupBy Partitioning Scheme.
    In this scheme, one table is partitioned according to its group-by attribute.
    These partitions are allocated to each processor, then a join is performed
    locally by passing the entirety of the second table.
    This is similar to the divide and broadcast approach, however the division part it
    is essential that the partitioning is by the group attribute.
    Once the tables are joined in each sub-result, the group-by aggregation is performed.

    The union of all results by each processor is the final result.
    This is because each processor is guaranteed to have all data related to each group
    allocated to it, so no further global aggregation is required.
    """
    n_processor = 3
    climate_groupby_attribute = 0
    fire_join_attribute = 6
    climate_join_attribute = 1

    climate_partitioned = hash_partition(climate_data, n_processor, hash_groupby, climate_groupby_attribute)
    print(partition_lengths(climate_partitioned))

    result = {}
    for pid, partition in climate_partitioned.items():
        print(pid)
        result.update(join_groupby(partition, climate_join_attribute, fire_data, fire_join_attribute))

    return result


print(task5(get_csv_data("ClimateData.csv"), get_csv_data("FireData.csv")))

