# By Milton Molina

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
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
       Method updates key/value pair in the hash map.
       Replaces value if key exists
       Adds new key/value pair when key not in hash map
        """
        # if table load greater than 0.5, need to resize table
        if self.table_load() >= 0.50:
            self.resize_table(self._capacity * 2)

        # computes value based on key
        hash_result = self._hash_function(key)

        # uses mod to assign value to an index in the array
        hash_index = hash_result % self._capacity

        # get key/value at index and save to variable
        bucket = self._buckets.get_at_index(hash_index)

        # save entry (tuple) as a variable
        pair = HashEntry(key, value)

        # typically initial insert
        # or if empty or a tombstone, fill in with new HashEntry
        if bucket is None or bucket.is_tombstone:
            self._buckets.set_at_index(hash_index, pair)
            self._size += 1

        else:
            # search for empty position using quadratic probing
            for ind in range(self._buckets.length()):
                quad = hash_index + ind ** 2
                index = quad % self._capacity
                bucket = self._buckets.get_at_index(index)

                # take tombstones into account
                if bucket is None or bucket.is_tombstone:
                    self._buckets.set_at_index(index, pair)
                    self._size += 1
                    return

                # when key matches, replace the value
                elif bucket.key == key:
                    bucket.value = value
                    return

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes capacity of the underlying table and copies all current elements into a new table
        """
        # checks if new capacity is less than current hash map size, doesn't continue resizing
        if new_capacity < self._size:
            return

        # if new capacity not a prime, change it to next highest prime number
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # create with hashmap with new capacity
        new_da = HashMap(new_capacity, self._hash_function)

        # copy over active elements to new hash map
        for ind in range(self._buckets.length()):
            bucket = self._buckets.get_at_index(ind)
            if bucket is not None and not bucket.is_tombstone:
                new_da.put(bucket.key, bucket.value)

        # set new references
        self._buckets = new_da._buckets
        self._capacity = new_capacity

        # resize again if load factor becomes greater than allowed threshold
        if self.table_load() >= 0.5:
            self._capacity = self._next_prime(self._capacity * 2)

    def table_load(self) -> float:
        """
        returns hash table load factor
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns number of empty buckets in the hash table
        """
        count = 0

        # iterate through array
        for ind in range(self._buckets.length()):
            bucket = self._buckets.get_at_index(ind)
            # check if none or tombstone, inc count if so
            if bucket is None or bucket.is_tombstone:
                count += 1

        # returns # of empty buckets
        return count

    def get(self, key: str) -> object:
        """
        Returns value associated with the given key
        If key is not in hash map, return None
        """
        # computes value based on key
        hash_result = self._hash_function(key)

        # uses mod to assign value to an index in the array
        hash_index = hash_result % self._capacity

        # get key/value at index and save to variable
        bucket = self._buckets.get_at_index(hash_index)

        # when not empty, key matches, and not a tombstone, save value to a variable and return
        if bucket is not None and bucket.key == key:
            if bucket.is_tombstone is False:
                return bucket.value

        # use quadratic probing to search for key
        for ind in range(hash_index, self._buckets.length()):
            quad = hash_index + ind ** 2
            index = quad % self._capacity
            bucket = self._buckets.get_at_index(index)

            # key found, and if not a tombstone, return the value
            if bucket is not None and bucket.key == key:
                if bucket.is_tombstone is False:
                    return bucket.value

        # if loop ends, this means key is not present
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if given key is in the hash map, otherwise returns False
        """
        # computes value based on key
        hash_result = self._hash_function(key)

        # uses mod to assign value to an index in the array
        hash_index = hash_result % self._capacity

        # get key/value at index and save to variable
        bucket = self._buckets.get_at_index(hash_index)

        # when not empty, key matches, and not a tombstone, return True
        # when not empty, key matches, and a tombstone, return False
        if bucket is not None and bucket.key == key:
            if bucket.is_tombstone:
                return False
            return True

        # otherwise, empty and needs quadratic probing
        for ind in range(self._buckets.length()):
            quad = hash_index + ind ** 2
            index = quad % self._capacity
            bucket = self._buckets.get_at_index(index)

            if bucket is not None and bucket.key == key:
                if bucket.is_tombstone:
                    return False
                return True

        # key not found, return False
        return False

    def remove(self, key: str) -> None:
        """
        Removes given key and its value from the hash map
        If key not found, does nothing
        """
        # computes value based on key
        hash_result = self._hash_function(key)

        # uses mod to assign value to an index in the array
        hash_index = hash_result % self._capacity

        # get key/value(HashEntry) at index and save to variable
        bucket = self._buckets.get_at_index(hash_index)

        # initial removal when not empty and key matches on first try
        if bucket is not None and bucket.key == key:
            if bucket.is_tombstone is False:
                bucket.is_tombstone = True
                self._size -= 1
                return

        # use quadratic probing to search for key
        for ind in range(self._buckets.length()):
            quad = hash_index + ind ** 2
            index = quad % self._capacity
            bucket = self._buckets.get_at_index(index)

            # key found
            if bucket is not None and bucket.key == key:
                if bucket.is_tombstone is False:
                    bucket.is_tombstone = True
                    self._size -= 1
                    return

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns DynamicArray object with keys/values from hash map as a tuple
        """
        # initialize new DynamicArray object
        hash_tuples = DynamicArray()

        # iterate through HashMap
        for ind in range(self._buckets.length()):
            # get key/value at index and save to variable
            bucket = self._buckets.get_at_index(ind)
            if bucket is not None:
                if bucket.is_tombstone is False:
                    # when not empty and not a tombstone, save key/value pair to variable
                    pair = bucket.key, bucket.value
                    # append variable to DynamicArray object created
                    hash_tuples.append(pair)

        # return DynamicArray with key/values as tuples
        return hash_tuples

    def clear(self) -> None:
        """
        Clears hash map contents
        """
        # save capacity to a variable to keep capacity the same
        cap = self._capacity

        # creates empty HashMap object with current capacity
        new_hash = HashMap(cap, self._hash_function)

        # updates references
        self._buckets = new_hash._buckets
        self._size = 0

    def __iter__(self):
        """
        Enables hash map to iterate across iterself
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        """
        try:
            while self._index < self._capacity:
                bucket = self._buckets[self._index]
                self._index += 1
                if bucket is not None:
                    return bucket
            raise StopIteration
        except DynamicArrayException:
            raise StopIteration


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 3")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    m.remove('key2')
    m.put('key2', 20)
    #
    # print("\nPDF - resize example 1")
    # print("----------------------")
    # m = HashMap(20, hash_function_1)
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    # m.resize_table(111)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    # print("\nPDF - resize example 2")
    # print("----------------------")
    # m = HashMap(75, hash_function_2)
    # keys = [i for i in range(25, 1000, 13)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    #
    # for capacity in range(111, 1000, 117):
    #     m.resize_table(capacity)
    #     if m.table_load() > 0.5:
    #         print(f"Check that the load factor is acceptable after the call to resize_table().\n"
    #               f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")
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
    #
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
    # m = HashMap(11, hash_function_1)
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
    # m.resize_table(2)
    # print(m.get_keys_and_values())
    #
    # m.put('20', '200')
    # m.remove('1')
    # m.resize_table(12)
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
    #
    # print("\nPDF - __iter__(), __next__() example 1")
    # print("---------------------")
    # m = HashMap(10, hash_function_1)
    # for i in range(5):
    #     m.put(str(i), str(i * 10))
    # print(m)
    # for item in m:
    #     print('K:', item.key, 'V:', item.value)
    #
    # print("\nPDF - __iter__(), __next__() example 2")
    # print("---------------------")
    # m = HashMap(10, hash_function_2)
    # for i in range(5):
    #     m.put(str(i), str(i * 24))
    # m.remove('0')
    # m.remove('4')
    # print(m)
    # for item in m:
    #     print('K:', item.key, 'V:', item.value)
