import pytest
from fun.function import Solution as Solute


class TestCase(Solute):
    def test_twoSum(self):
        nums = [2, 7, 11, 15]
        target = 9
        result = self.twoSum(nums=nums, target=target)
        assert result == [0, 1]

    def test_reverse(self):
        x = -123
        result = self.reverse(x)
        assert result == -321

    def test_isPalindrome(self):
        x = 12321
        result = self.isPalindrome(x)

    def test_isValid(self):
        t = "([)]"
        result = self.isValid(s=t)
        assert result is False

    def test_removeDuplicates(self):
        nums = [1, 5, 3, 6, 5, 5, 2, 1, 0, 2]
        result = self.removeDuplicates(nums)
        print(result)
        assert result == 6

    def test_removeElement(self):
        nums = [1, 5, 3, 6, 5, 5, 2, 1, 0, 2]
        val = 5
        result = self.removeElement(nums, val)
        assert result == 7

    def test_strStr(self):
        haystack = "mississippi"
        needle = "issipi"
        result = self.strStr(haystack, needle)
        assert result == -1

    def test_searchInsert(self):
        nums = [1, 2, 5, 9, 10, 15, 16, 18]
        target = 1
        res = 0
        result = self.searchInsert(nums, target)
        assert result == 0

    def test_countAndSay(self):
        result = self.countAndSay(n=4)
        assert result == '1211'
        

