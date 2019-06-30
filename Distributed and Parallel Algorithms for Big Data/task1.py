"""
Author: Jithya Nanayakkara (21329281)
"""

import csv
import math
from multiprocessing import Pool
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


def get_csv_data(filename):
    """
        Returns a list of records loaded from a CSV file, without the headers.
    """
    csv_file = open(filename)
    csv_data = csv.reader(csv_file, delimiter=",")
    return list(csv_data)[1:]


def h6(date, n):
    """
        Adds all the individual components of a date, and returns the mod of that with n.

        Arguments:
            record -- record with the date attribute at index 1
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


def hash_partition(data, n, h):
    """
    This strategy uses the hash of a particular attribute to determine which processor a record is allocated to.
    
    Arguments:
        data -- List of records
        n -- number of processors
        h -- hashing function that takes two arguments
    """
    partitions = {}
    for record in data:
        hash_val = h(record, n)
        if (hash_val not in partitions):
            partitions[hash_val] = []

        partitions[hash_val].append(record)
    
    return partitions


def binary_search(data, attribute_index, key_str):
    """
    Perform binary search on SORTED data for the given key.
    This terminates upon finding the first match.
    
    Arguments:
        data -- an input dataset which is a list of records and sorted in ascending order
        key -- the item to find ( a date string in the form "dd/mm/yyyy")
        
    Return:
        result -- the matched record in a list
    """
    results = []
    lower = 0
    middle = 0
    upper = len(data) - 1
    key = time.strptime(key_str, "%d/%m/%Y")

    while (lower <= upper):
        middle = int((lower + upper)/2)
        date = time.strptime(data[middle][attribute_index], "%d/%m/%Y")

        if key == date:
            results.append(data[middle])
            break

        elif key > date:
            lower = middle + 1
        else:
            upper = middle - 1

    return results


def task1_search_q1(data, query, n_processor):
    """
        The algorithm we chose to perform the search is outlined below:

        1. Partition the data using hash partitioning. 
           The attribute used for the hash is the date.
           The hash sums the day, month and year and returns the modulus of n (where n is the number of processors).
        
        2. Perform parallel search:
            a. Generate the hash of the query
            b. This hash locates which partition to perform local search in (processor activation)
            c. The local search performed is binary search
            d. The first record matched is returned
        
        Reasoning:
        Analysing the data, we noted that it all the records had unique dates, and the records
        were already sorted by date.

        Therefore, hash partitioning was chosen as it is suitable for exact match search.
        In this algorithm, the parallelism comes in knowing which partition to search for
        (reduced search space), so speed up is obtained.

        Furthermore, the ordering of the records is maintained in our implementation
        of the partitioning algorithm.
        This allows us to perform the more efficient binary search.
        As the records have unique dates, we can terminate on finding the first match.

        Advantages:
         - As the partitioning is based on the search attribute, only the required processor
           needs to be activated, freeing up other processors to do other tasks.
        
         - Binary search has a complexity of O(log n), which is better than linear search's O(n).
        
        Disadvantages:
         - All processors need to be activated if we have to search using a non-partitioning attribute.

         - It's difficult to load balance using hash partitioning. We came up with a total of 6 hashing
           methods, and the one we used partitioned the dataset the best for our values of n.
           However this even distribution isn't guaranteed for all values of n or as the data set grows.

         - Hash partitioning is unsuitable for range searches, as you'd have to hash every possible 
           value of the query within the range.        
    """
    partitions = hash_partition(data, n_processor, h6)

    dummy_record = ["dummy", query] # this is because the hash function expects a record
    query_hash = h6(dummy_record, n_processor)

    return binary_search(partitions[query_hash], 1, query)


def fragment_data(rows, attribute_index):
    """
        Splits a list of records into a list of fragments,
        where each fragment has approximately 50 records and is ordered
        in ascending order.

        The fragmentation assumes the that average number of records returned by the query
        is 100, and that the optimal number of processors to use is 2.

        Arguments:
            rows -- a list of records
            attribute_index -- the index of the attribute to sort the records in the fragments
        
        Returns:
            A list of fragments
    """
    Qn = 400
    M = 2
    FC = (int) (Qn/M)
    num_fragments = (int) (math.ceil(len(rows)/FC))
    fragments = []

    for i in range(num_fragments):
        fragments.append([])
    
    sorted_rows = sorted(rows, key=lambda r : int(r[attribute_index]))

    j = 0
    i = 0
    for row in sorted_rows:
        if (i < FC):
            i += 1
        else:
            i = 1
            j += 1

        fragments[j].append(row)
    
    return fragments



def hrps_parallel_search(partition, start, end):
    """
        Searches each fragment in the partition for records that
        match the given range.
    """
    results = []
    
    for fragment in partition:
        results.append(hrps_binary_search(fragment, 7, start, end))
    
    return flatten_list(results)


def hrps_round_robin(fragments, n_processors, attribute_index):
    """
    Allocates fragments to a processor in a round robin fashion.

    Arguments:
        fragments -- a list of all fragments
        n_processors -- the number of processors to allocate
        attribute_index -- the partitioning attribute of the record in the fragment

    Returns:
        A nested list of length n_processors, with an even distribution of fragments
        in each sublist.
    """
    partitions = []
    grid = {"start":{}, "end": {}}

    for i in range(n_processors):
        partitions.append([])
    
    i = 0
    for fragment in fragments:
        i = i % n_processors
        start = int(fragment[0][attribute_index])
        end = int(fragment[len(fragment) - 1][attribute_index])
        
        if start not in grid["start"]:
            grid["start"][start] = set()
        
        if end not in grid["end"]:
            grid["end"][end] = set()
        
        grid["start"][start].add(i)
        grid["end"][end].add(i)

        partitions[i].append(fragment)
        i += 1
    
    return (partitions, grid)

def hrps_binary_search(data, attribute_index, start_str, end_str):
    """
    Perform a ranged binary search on SORTED data for the given key.
    Does not stop on the first match.        
    
    Arguments:
        data -- an input dataset which is a list and sorted in ascending order
        attribute_index -- search attribute index in the record
        start_str -- start range
        end_str -- end range
        
    Return:
        result -- list of all found records in the range start <= end
    """
    results = []

    start_position = -1
    end_position = -1
    
    start = int(start_str)
    end = int(end_str)

    middle = 0
    lower = 0
    upper = len(data) - 1
    while (lower <= upper):
        middle = int((lower + upper)/2)
        temperature = int(data[middle][attribute_index])

        if (temperature >= start) and (temperature <= end):
            start_position = middle
            upper = middle - 1

        elif start > temperature:
            lower = middle + 1
            
        else:
            upper = middle - 1

    middle = 0
    lower = 0
    upper = len(data) - 1
    while (lower <= upper):
        middle = int((lower + upper)/2)
        temperature = int(data[middle][attribute_index])

        if (temperature >= start) and (temperature <= end):
            end_position = middle
            lower = middle + 1

        elif end > temperature:
            lower = middle + 1
            
        else:
            upper = middle - 1
    
    if (start_position == -1) and (end_position == -1):
        return results        
    elif (start_position == -1):
        return data[0:]
    elif (end_position == -1):
        return data[start_position:]
    else:
        return data[start_position: end_position + 1]


def task1_search_q2(data, start, end, n_processors):
    """
    Implementation of the Hybrid-Range Partitioning Strategy (HRPS).
    Assumes the start and end is inclusive.

    The algorithm works as follows:
        1. Break the data set into fragments, with approximately 50 records per fragment.
           It is assumed that the average query returns 100 records, and the optimal
           number of processors to use is 2 (M).

        2. Allocate each fragment to a processor in a round robin fashion.
           Build a grid of the ranges held in each partition, to know which processors
           to search whenever n_processors > M.           

        3. If M <= N:
            Use ALL processors.
           Else:
             Use only processors that are likely to have the records.
        
        4. Binary range search is performed on each partition.
           Search does not stop when a match is found.

    Reasoning:
        Hash partitioning is unsuitable for range search.

        Round robin partitioning is good for load balancing, but activates all processors
        when performing search, as it has no idea which processors have access to the
        records. While search is performed in parallel, the startup and consolidation
        costs of unnecessary processors can impact performance.

        Range partitioning partitions based on the attribute, so processors don't need
        to be unnecessarily activated. However even load balancing cannot be achived.
        Furthermore, if a system has many processors available, often only 1 or 2 processors
        are activated to perform the range search, thereby not utilizing the spare capacity.

        Hybrid-Range Partitioning combines round robin and range partitioning, by 
        ordering the data and splitting it into fragments that are distributed to each
        processor - ensuring that M adjacent fragments are distributed to different processors
        (where M is the optimal number of processors to perform the search).

        This method is good when you know the number of records returned in an average query
        and the optimum number of processors to use (M), as it only activates processors that
        are needed and close to M and maintains even load balancing across them.
        
        However it should be noted that in my implementation of the algorithm, the 
        number of processors activated isn't optimal when N > M, but it can be improved.
        (For e.g., when M = 2, N = 100, 54 processors are activated to seach in the range
        65 - 100).

        Advantages:
        - Better load balancing for tables with non-uniform distribution of the paritioning attribute
          (as adjacent fragments are in different processors).
        - Ensures close to the optimal number of processors are activated in the search.

        Disadvantages:
         - Only works with a single partitioning attribute.
         - Need to know the resource requirements of the system to come up with good values of M
           and the size of fragments (FC).
    """
    M = 2
    fragments = fragment_data(data, 7)
    allocations = hrps_round_robin(fragments, n_processors, 7)
    partitions =allocations[0]
    grid = allocations[1]
    results = []
    pool = Pool(processes=n_processors)

    if (M < n_processors):
        partition_ids = set()

        for s_key, values in grid["start"].items():
            if s_key <= end:
                partition_ids.update(values)
        
        for e_key, values in grid["end"].items():
            if e_key >= start:
                partition_ids.update(values)

        
        print("Number of processors activated: " + str(len(partition_ids)))

        for pid in partition_ids:            
            #result = pool.apply_async(hrps_parallel_search, [partitions[pid], start, end])
            #output = result.get()
            #results.append(output)
            for fragment in partitions[pid]:
                results.append(hrps_binary_search(fragment, 7, start, end))
        
    else:
        for partition in partitions:
            #result = pool.apply_async(hrps_parallel_search, [partition, start, end])
            #output = result.get()
            #results.append(output)
            for fragment in partition:
                results.append(hrps_binary_search(fragment, 7, start, end))

    results = flatten_list(results)

    final_result = []
    for result in results:
        final_result.append((result[0], result[1], result[5]))

    #return results
    return final_result

climate_data = get_csv_data("ClimateData.csv")
fire_data = get_csv_data("FireData.csv")
print(task1_search_q1(climate_data, "21/10/2017", 5))
print(len(task1_search_q2(fire_data, 65, 100, 32)))






