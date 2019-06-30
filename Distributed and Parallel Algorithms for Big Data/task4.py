"""
Author: Jithya Nanayakkara (21329281)
"""

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



def redistribute_data(processors):
    """
        Given a set of partitioned data from every every processor,
        allocate the appropriate partition to their processor

        Arguments:
            processors - A nested diction. The first dictionary is of processors, 
                         who have partitioned their data into a dictionary, where 
                         the dictionary key is the processor the partition should 
                         be allocated to.

        Returns:
            A dictionary of lists. The key is the processor id, and the value is
            the list of records which belong to the processor. It is redistributed
            data from the given argument.             
    """
    new_distribution = {}

    for processor_id in range(len(processors)):
        for pid, partition in processors[processor_id].items():
            if pid not in new_distribution:
                new_distribution[pid] = [partition]
            else:
                new_distribution[pid].append(partition)

    for pid, partition in new_distribution.items():
        new_distribution[pid] = flatten_list(new_distribution[pid])
    
    return new_distribution


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
    This strategy uses the hash of a particular attribute to determine which processor a 
    record is allocated to.
    
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


def partition_lengths(partitions):
    """
    A helper function.
    Returns a dictionary containing the lengths of each partition in the input.
    This is to see the distribution of records to partitions.
    
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


def count_agg(data, index):
    """
    Performs an aggregated count of all the records with the value
    at the given index.

    Arguments:
        data -- A list of records
        index -- the index of the attribute to count the occurrence of its value
    
    Returns:
        A dictionary in the form "date": count
        Where count is an int, the total number of records with that value of date.
    """
    result = {}

    for record in data:
        attribute_val = record[index]
        
        if attribute_val in result:
            result[attribute_val] += 1
        else:
            result[attribute_val] = 1

    return result


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


def task4_q1(fire_data):
    """
    In this task, we assume the data has already been partitioned some way and allocated
    to processors. We also assume a multi-processor architecture such that
    data can be passed between processors very quickly.

    The partitioning algorithm employed for parallel group by is the redistribution method.
    In this method, each processor partitions its data in parallel so that each partition is allocated
    to an appropriate processor, based on the group-by attribute.
    We have used hash partitioning as the way of allocating records to processors, based 
    on the group by attribute of date.
    These partitions are then redistributed to their respective processors.

    Finally, a local group by aggregation is performed by each processor in parallel.
    The final result is the union of the result of each processor.

    Unlike other parallel groupby methods, this method performs the final aggregation in
    the final step.
    The benefit of this approach is when compared to other approaches such as the
    traditional method or the two phase method, the final aggregation step is 
    not a bottleneck, as the final aggregation is done in parallel by all processors.

    The biggest cost component of this phase is the distribution phase. It is also
    at the mercy of the distribution of records being even.
    """
    n_processors = 4
    date_attribute_index = 6

    # Random unequal partitioned fire data
    fire_data_partitioned = [fire_data[0:500], fire_data[500: 1000], fire_data[1000:1500], fire_data[1500:]]
    processors = {}

    # Perform parallel partitioning within each processor's data
    for processor_id in range(n_processors):
        processors[processor_id] = hash_partition(fire_data_partitioned[processor_id], n_processors, h6, date_attribute_index)

    # Perform redistribution
    partitions = redistribute_data(processors)

    # Perform parallel aggregation using a local aggregation method in each processor
    results = []
    for pid, partition in partitions.items():
        results.append(count_agg(partition, date_attribute_index))

    # Result is union of all local aggregations
    final_result = {}
    for result in results:
        final_result.update(result)


def task4_q2(fire_data):
    """
    Follows the exact same method of question 1, but using an average
    aggregation function instead.
    """
    
    n_processors = 4
    date_attribute_index = 6
    surface_temp_attribute_index = 7 

    # Random unequal partitioned fire data
    fire_data_partitioned = [fire_data[0:500], fire_data[500: 1000], fire_data[1000:1500], fire_data[1500:]]
    processors = {}

    # Perform parallel partitioning
    for processor_id in range(n_processors):
        processors[processor_id] = hash_partition(fire_data_partitioned[processor_id], n_processors, h6, surface_temp_attribute_index)

    # Perform redistribution
    partitions = redistribute_data(processors)

    # Perform parallel aggregation using a local aggregation method in each processor
    results = []
    for pid, partition in partitions.items():
        results.append(avg_agg(partition, date_attribute_index, surface_temp_attribute_index))

    # Result is union of all local aggregations
    final_result = {}
    for result in results:
        final_result.update(result)
    
    print(len(final_result))


task4_q2(get_csv_data("FireData.csv"))


