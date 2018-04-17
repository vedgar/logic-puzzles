import itertools, collections, pdb
nums = collections.Counter([1, 1, 5, 8])

def anptgf(nums):
    if len(nums) == 1:
        num, = nums
        yield num
    ne = list(nums.elements())
    for k in range(1, len(ne)):
        for left in itertools.combinations(ne, k):
            left = collections.Counter(left)
            right = nums - left
            for a in anptgf(left):
                for b in anptgf(right):
                    for c in a + b, a - b, a * b, a / b:
                        yield c
                        if c == 10:
                            pdb.set_trace()
print(len(list(anptgf(nums))))
