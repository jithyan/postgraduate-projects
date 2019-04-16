"""
Author: Jithya Nanayakkara (21329281)
"""

import csv
import sys

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


def qsort(arr, attribute_index):
    """
    Sort a list using the quicksort algorithm.

    Arguments:
        arr -- the input list to be sorted
    Return:
        result -- the sorted arr
    """

    if len(arr) <= 1:
        return arr
    else:
        return qsort([x for x in arr[1:] if int(x[attribute_index]) < int(arr[0][attribute_index])], attribute_index) + [arr[0]] + qsort([x for x in arr[1:] if int(x[attribute_index]) >= int(arr[0][attribute_index])], attribute_index)


def find_min(records, attribute_index):
    """
    Find the smallest record

    Arguments:
        records -- the input record set
    Return:
        result -- the smallest record's index
    """

    m = int(records[0][attribute_index])
    index = 0
    for i in range(len(records)):
        if (int(records[i][attribute_index]) < m):
            index = i
            m = int(records[i][attribute_index])

    return index


def k_way_merge(record_sets, attribute_index):
    """
    K-way merging algorithm
    Arguments:
    record_sets -- the set of mulitple sorted sub-record sets
    Return:
    result -- the sorted and merged record set
    """
    # indexes will keep the indexes of sorted records in the given buffers
    indexes = []
    for x in record_sets:
        indexes.append(0) # initialisation with 0

    
    result = [] # final result will be stored in this variable
    t = [] # the merging unit (i.e. # of the given buffers)
    

    while(True):
        t = []

        # This loop gets the current position of every buffer
        for i in range(len(record_sets)):
            if(indexes[i] >= len(record_sets[i])):
                dummy = [0,1,2,3,4,5,6,sys.maxsize]
                t.append(dummy)
            else:
                t.append(record_sets[i][indexes[i]])

        smallest = find_min(t, attribute_index)
        # if we only have sys.maxsize on the tuple, we reached the end of every record set
        if(t[smallest][attribute_index] == sys.maxsize):
            break

        # This record is the next on the merged list
        result.append(record_sets[smallest][indexes[smallest]])
        indexes[smallest] +=1

    return result


def serial_sorting(dataset, buffer_size, attribute_index):
    """
    Perform a serial external sorting method based on sort-merge
    The buffer size determines the size of eac sub-record set

    Arguments:
        dataset -- the entire record set to be sorted
        buffer_size -- the buffer size determining the size of each sub-record
        set
    Return:
        result -- the sorted record set
    """
    if (buffer_size <= 2):
        print("Error: buffer size should be greater than 2")
        return

    result = []

    # --- Sort Phase ---
    sorted_set = []
    # Read buffer_size pages at a time into memory and
    # sort them, and write out a sub-record set (i.e. variable: subset)
    start_pos = 0
    N = len(dataset)
    while True:
        if ((N - start_pos) > buffer_size):
            # read B-records from the input, where B = buffer_size
            subset = dataset[start_pos:start_pos + buffer_size]
            # sort the subset (using qucksort defined above)
            sorted_subset = qsort(subset, attribute_index)
            sorted_set.append(sorted_subset)
            start_pos += buffer_size
        else:
            # read the last B-records from the input, where B is less than
            buffer_size
            subset = dataset[start_pos:]
            # sort the subset (using qucksort defined above)
            sorted_subset = qsort(subset, attribute_index)
            sorted_set.append(sorted_subset)
            break
    
    # --- Merge Phase ---
    merge_buffer_size = buffer_size - 1
    dataset = sorted_set
    while True:
        merged_set = []
        N = len(dataset)
        start_pos = 0

        while True:
            if ((N - start_pos) > merge_buffer_size):
                # read C-record sets from the merged record sets, where C = merge_buffer_size
                subset = dataset[start_pos:start_pos + merge_buffer_size]
                merged_set.append(k_way_merge(subset, attribute_index)) # merge lists in subset
                start_pos += merge_buffer_size
            else:
                # read C-record sets from the merged sets, where C is less than merge_buffer_size
                subset = dataset[start_pos:]
                merged_set.append(k_way_merge(subset, attribute_index)) # merge lists in subset
                break
                
        dataset = merged_set
        if (len(dataset) <= 1): # if the size of merged record set is 1, then stop
            result = merged_set
            break

    return flatten_list(result)


def ranged_partition_for_redistribution(fire_data, ranges):
    partitions = {}

    for processor_id in range(4):
        partitions[processor_id] = []

    # Assign each record to a processor depending on the range.
    for record in fire_data:
        s_temp = int(record[7])

        if (s_temp - ranges[0]) <= 0:
            partitions[0].append(record)

        elif (s_temp - ranges[1]) <= 0:
            partitions[1].append(record)

        elif (s_temp - ranges[2]) <= 0:
            partitions[2].append(record)

        else:
            partitions[3].append(record)

    return partitions


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


def redistribute_data(processors):
    new_distribution = {}

    for processor_id in range(4):
        for pid, partition in processors[processor_id].items():
            if pid not in new_distribution:
                new_distribution[pid] = [partition]
            else:
                new_distribution[pid].append(partition)

    for pid, partition in new_distribution.items():
        new_distribution[pid] = flatten_list(new_distribution[pid])
    
    return new_distribution


def task_3(fire_data):
    """
    In this task, we use a Parallel Partitioned Sort, with
    sort-merge as the serial external sort-merge method
    and quicksort as the in-memory sorting method.

    We assume that the fire data has been already partitioned and allocated
    to processing elements using a random-unequal method.

    Using parallel partitioned sort, there are two major phases:
        1. Partitioning of the data
        2. Local sort
    
    Between 1 and 2, there is a redistribution of the partitioned data.
    Otherwise phases 1 and 2 are done in parallel by the processors.

    The partitioning of the data is done in such a way that each processor 
    is allocated a certain non-overlapping range of data.
    Each processor returns partitions of its own data that is meant for 
    other processors.
    A redistribution step occurs, where all the data within a range is sent
    to their respective processors.

    Then a local sort takes place. The results produced by the local sort are already the
    final results. Each processor will have produced a sorted list, and all processors
    in the order of the range partitioning method used in this process are also sorted. 

    An important distinction between this and other parallel algorithms is that
    the first phase isn't sorting.

    The biggest benefit of this method is that there is no merging, which is an expensive 
    bottleneck in other methods.  Furthermore it better incorporates parallelism as both
    the partitioning and sorting phases are done in parallel.

    However a significant drawback is the skew that arises from range partitioning.
    Workarounds to limit this drawback is to create more buckets of data than processors
    and try to distribute the load this way. However this was not implemented in our
    algorithm.
    """
    # Random unequal partitioned fire data
    fire_data_partitioned = [fire_data[0:500], fire_data[500: 1000], fire_data[1000:1500], fire_data[1500:]]
    
    # The ranges we're going to assign to each processor
    ranges = [33, 66, 99]   
    processors = {}

    for processor_id in range(4):
        processors[processor_id] = []
  
    # Perform parallel partitioning
    for processor_id in range(4):
        processors[processor_id] = ranged_partition_for_redistribution(fire_data_partitioned[processor_id], ranges)
    
    # Perform redistribution
    partitions = redistribute_data(processors)

    # Perform parallel sort    
    result = []
    buffer_size = 17
    for i in range(4):
        result.append(serial_sorting(partitions[i], buffer_size, 7))
    
    # The final result is just the union of all the processor results in order
    return flatten_list(result)