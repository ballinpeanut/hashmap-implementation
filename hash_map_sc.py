# By Milton Molina

from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        """
        return self._capacity

    # ^ SKELETON CODE PROVIDED BY INSTRUCTOR ^
    # ------------------------------------------------------------------ #
    # Anything below the line is my own code

    def put(self, key: str, value: object) -> None:
        """
        Updates key/value pair in hash map
        If given key exists, the value is replaced with the new value
        If key not in hash map, a new key/value pair must be added

        :param key: key being inserted
        :param value: value being inserted
        """
        # when table is full, double the capacity
        if self.table_load() >= 1:
            self.resize_table(self._capacity * 2)

        # computes value based on key
        hash_result = self._hash_function(key)

        # uses mod to assign value to an index in the array
        hash_index = hash_result % self._capacity

        # use the linked list at the calculated index
        bucket = self._buckets.get_at_index(hash_index)

        # search for node in linked list containing the key
        node = bucket.contains(key)

        # when empty or value not found, insert new node with key/value
        if node is None:
            bucket.insert(key, value)
            self._size += 1
        # otherwise, key matched and value is replaced
        else:
            node.value = value

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes capacity of the DynamicArray object when max capacity is reached
        All existing key-value pairs are copied over to new table

        :param new_capacity:
        """
        if new_capacity < 1:
            return

        # takes care of resize_table(2)
        if new_capacity == 2:
            new_capacity *= 2

        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # create empty hash with new capacity
        new_da = HashMap(new_capacity, self._hash_function)

        # copy buckets from old hash map to new hash map
        for ind in range(self._buckets.length()):
            bucket = self._buckets.get_at_index(ind)
            for node in bucket:
                new_da.put(node.key, node.value)

        # update capacity after potential resize from indirect recursion (?)
        # used to pass resize_table(1)
        new_capacity = new_da._capacity

        # update buckets reference and capacity
        self._buckets = new_da._buckets
        self._capacity = new_capacity

    def table_load(self) -> float:
        """
        Returns current hash table load factor
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns number of empty buckets in hash table
        """
        count = 0
        # iterate through array
        for ind in range(self._buckets.length()):
            # get the "bucket" (linked list) at the index
            bucket = self._buckets.get_at_index(ind)
            # check if empty, if so, increment count by 1
            if bucket is None or bucket.length() == 0:
                count += 1

        return count

    def get(self, key: str):
        """
        Returns value associated with the given key
        If not in hash map, returns None
        """
        # computes bucket using hash function
        hash_result = self._hash_function(key)

        # uses mod to arrive at correct index
        hash_index = hash_result % self._capacity

        # use the linked list at the calculated index
        bucket = self._buckets.get_at_index(hash_index)

        # search for node in linked list containing the key
        node = bucket.contains(key)

        # when empty or value not found:
        if node is None:
            return None
        # otherwise, key matched and value returned
        else:
            return node.value

    def contains_key(self, key: str) -> bool:
        """
        Returns True if key is in hash map. Otherwise, returns False

        :param key: what is being searched for
        """
        # computes bucket based on key
        hash_result = self._hash_function(key)

        # uses mod operator to navigate to index
        hash_index = hash_result % self._capacity

        # use the linked list at the calculated index
        bucket = self._buckets.get_at_index(hash_index)

        # search for node in linked list containing the key
        node = bucket.contains(key)

        # when empty or value not found
        if node is None:
            return False
        # otherwise, key matched
        else:
            return True

    def remove(self, key: str) -> None:
        """
        Removes given key and its value from hash map
        If key not in hash map, nothing happens
        """
        # computes bucket based on key
        hash_result = self._hash_function(key)

        # uses mod operator to navigate to index
        hash_index = hash_result % self._capacity

        # use the linked list at the calculated index
        bucket = self._buckets.get_at_index(hash_index)

        # search for node in linked list containing the key
        node = bucket.contains(key)

        # when empty, key can't be removed
        if node is None:
            return
        # otherwise, remove key and its value
        else:
            bucket.remove(key)
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns dynamic array object where each index contains a tuple of a key/value pair from the hash map
        Order is irrelevant
        """
        # initialize dynamic array object
        tuple_da = DynamicArray()

        for ind in range(self._buckets.length()):
            bucket = self._buckets.get_at_index(ind)
            # when not empty, iterate thru the linked list
            for node in bucket:
                node_key = node.key
                node_val = node.value

                # save tuple to variable
                pair = node_key, node_val

                # append pair to dynamic array object
                tuple_da.append(pair)

        # returns dynamic array with key/values as tuples
        return tuple_da

    def clear(self) -> None:
        """
        Clears hash map contents
        """
        cap = self._capacity
        new_da = HashMap(cap, self._hash_function)
        self._buckets = new_da._buckets
        self._size = 0


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Receives sorted or unsorted array and finds the mode.
    Use hashmap to get frequency of keys

    :param da: DynamicArray object being used

    :returns: A tuple consisting of the mode and frequency.
    """
    map = HashMap()

    # iterate through input array
    for ind in range(da.length()):
        key = da.get_at_index(ind)
        # when key is in hashmap, get and incr. val
        if map.contains_key(key):
            val = map.get(key)
            val += 1
            map.put(key, val)
        # otherwise, add to hashmap with value of 1
        else:
            map.put(key, 1)

    # places keys and values in dynamic array
    new_da = map.get_keys_and_values()

    # used to place mode, create frequency counter
    mode_arr = DynamicArray()
    freq = 1

    # iterate through keys/values array
    for ind in range(new_da.length()):
        curr = new_da.get_at_index(ind)

        # set frequency and append mode array with new mode
        # clears mode array when new mode is found
        if curr[1] > freq:
            freq = curr[1]
            new_mode = DynamicArray()
            mode_arr = new_mode
            mode_arr.append(curr[0])

        # append values with same frequency
        elif curr[1] == freq:
            mode_arr.append(curr[0])

    return mode_arr, freq

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    # print("\nPDF - put example 1")
    # print("-------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('str' + str(i), i * 100)
    #     if i % 25 == 24:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - put example 2")
    # print("-------------------")
    # m = HashMap(41, hash_function_2)
    # for i in range(50):
    #     m.put('str' + str(i // 3), i * 100)
    #     if i % 10 == 9:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - resize example 1")
    # print("----------------------")
    # m = HashMap(20, hash_function_1)
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    # m.resize_table(30)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    # print("\nPDF - resize example 2")
    # print("----------------------")
    # m = HashMap(75, hash_function_2)
    # keys = [i for i in range(1, 1000, 13)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    #
    # for capacity in range(111, 1000, 117):
    #     m.resize_table(capacity)
    #
    #     m.put('some key', 'some value')
    #     result = m.contains_key('some key')
    #     m.remove('some key')
    #
    #     for key in keys:
    #         # all inserted keys must be present
    #         result &= m.contains_key(str(key))
    #         # NOT inserted keys must be absent
    #         result &= not m.contains_key(str(key + 1))
    #     print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - resize example 3")
    print("----------------------")
    m = HashMap()
    m.put('key551', -591)
    m.put('key654', -117)
    m.put('key116', 464)
    m.put('key893', 476)
    m.put('key361', -494)
    m.resize_table(1)
    print(m.get_capacity(), m.get_size())

    print("\nPDF - resize example 4")
    print("----------------------")
    m = HashMap(47, hash_function_2)
    m.put('key60', -364)
    m.put('key454', 195)
    m.put('key672', 503)
    m.put('key862', -668)
    m.put('key99', -557)
    m.put('key294', 86)
    m.put('key502', 548)
    m.put('key196', -468)
    m.put('key106', -33)
    m.put('key441', -506)
    m.put('key433', 721)
    m.put('key76', -86)
    m.put('key325', -439)
    m.put('key696', -30)
    m.put('key210', -224)
    m.resize_table(2)
    print(m.get_capacity(), m.get_size())

    m = HashMap(2)
    print(m.get_capacity(), m.get_size())
    #
    # print("\nPDF - table_load example 1")
    # print("--------------------------")
    # m = HashMap(101, hash_function_1)
    # print(round(m.table_load(), 2))
    # m.put('key1', 10)
    # print(round(m.table_load(), 2))
    # m.put('key2', 20)
    # print(round(m.table_load(), 2))
    # m.put('key1', 30)
    # print(round(m.table_load(), 2))
    #
    # print("\nPDF - table_load example 2")
    # print("--------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(50):
    #     m.put('key' + str(i), i * 100)
    #     if i % 10 == 0:
    #         print(round(m.table_load(), 2), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - empty_buckets example 1")
    # print("-----------------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 30)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key4', 40)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - empty_buckets example 2")
    # print("-----------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - get example 1")
    # print("-------------------")
    # m = HashMap(31, hash_function_1)
    # print(m.get('key'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    # #
    # print("\nPDF - get example 2")
    # print("-------------------")
    # m = HashMap(151, hash_function_2)
    # for i in range(200, 300, 7):
    #     m.put(str(i), i * 10)
    # print(m.get_size(), m.get_capacity())
    # for i in range(200, 300, 21):
    #     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
    #     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)
    #
    # print("\nPDF - contains_key example 1")
    # print("----------------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.contains_key('key1'))
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key3', 30)
    # print(m.contains_key('key1'))
    # print(m.contains_key('key4'))
    # print(m.contains_key('key2'))
    # print(m.contains_key('key3'))
    # m.remove('key3')
    # print(m.contains_key('key3'))
    #
    # print("\nPDF - contains_key example 2")
    # print("----------------------------")
    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 20)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    # result = True
    # for key in keys:
    #     # all inserted keys must be present
    #     result &= m.contains_key(str(key))
    #     # NOT inserted keys must be absent
    #     result &= not m.contains_key(str(key + 1))
    # print(result)
    #
    # print("\nPDF - remove example 1")
    # print("----------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get('key1'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    # m.remove('key1')
    # print(m.get('key1'))
    # m.remove('key4')
    #
    # print("\nPDF - get_keys_and_values example 1")
    # print("------------------------")
    # m = HashMap(11, hash_function_2)
    # for i in range(1, 6):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys_and_values())
    #
    # m.put('20', '200')
    # m.remove('1')
    # m.resize_table(2)
    # print(m.get_keys_and_values())
    #
    # print("\nPDF - clear example 1")
    # print("---------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key1', 30)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())
    #
    # print("\nPDF - clear example 2")
    # print("---------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.get_size(), m.get_capacity())
    # m.resize_table(100)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())

    # print("\nPDF - find_mode example 1")
    # print("-----------------------------")
    # da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    # mode, frequency = find_mode(da)
    # print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")
    #
    # print("\nPDF - find_mode example 2")
    # print("-----------------------------")
    # test_cases = (
    #     ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
    #     ["one", "two", "three", "four", "five"],
    #     ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    # )
    #
    # for case in test_cases:
    #     da = DynamicArray(case)
    #     mode, frequency = find_mode(da)
    #     print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
