import pytest


class Solution:
    @staticmethod
    def quick_sort(array):

        @staticmethod
        def twoSum(nums, target):
            """
            两数之和
            :type nums: List[int]
            :type target: int
            :rtype: List[int]
            """
            for i in range(len(nums)):
                for j in range(len(nums)):
                    if i != j and nums[i] + nums[j] == target:
                        return [i, j]

    @staticmethod
    def reverse(x):
        """
        整数反转
        :type x: int
        :rtype: int
        """
        s = str(x)
        if s[0] == '-':
            x = int(s[0] + s[1:][::-1])
        else:
            x = int(s[::-1])
        return x if -2 ** 31 <= x <= 2 ** 31 - 1 else 0

    @staticmethod
    def isPalindrome(x):
        """
        回文数
        :type x: int
        :rtype: bool
        """
        array = list(str(x))
        for i in range(len(array) // 2):
            if array[i] == array[len(array) - i - 1]:
                continue
            else:
                return False
        return True
        # return str(x)==str(x)[::-1]

    @staticmethod
    def romanToInt(s):
        """
        罗马数字转整数
        :type s: str
        :rtype: int
        """
        adict = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000,
                 'IV': 4, 'IX': 9, 'XL': 40, 'XC': 90, 'CD': 400, 'CM': 900}
        alist = ['IV', 'IX', 'XL', 'XC', 'CD', 'CM']
        s += ' '
        res, i = 0, 0
        while i < len(s) - 1:
            if s[i] + s[i + 1] in alist:
                res += adict[s[i] + s[i + 1]]
                i += 2
            else:
                res += adict[s[i]]
                i += 1
        return res

    @staticmethod
    def longestCommonPrefix(strs):
        """
        最长公共前缀
        :type strs: List[str]
        :rtype: str
        """
        if len(strs) == 1:
            return strs[0]
        elif len(strs) == 0:
            return ''
        else:
            result = ''
            for i in range(len(strs[0])):
                flag = 0
                for temp in strs[1:]:
                    if strs[0][:i + 1] not in temp[:i + 1]:
                        break
                    else:
                        flag += 1
                if flag == len(strs) - 1:
                    result = strs[0][:i + 1]
                else:
                    break
            return result

    @staticmethod
    def isValid(s):
        """
        有效的括号
        :type s: str
        :rtype: bool
        """
        if len(s) % 2 == 1 or len(s) == 0:
            return False
        else:
            dicts = {"(": ")", "[": "]", "{": "}"}
            stack = []
            for i in s:
                if i in dicts:
                    stack.append(i)
                elif dicts[stack.pop()] != i:
                    return False
            if len(stack) != 0:
                return False
            else:
                return True

    # Definition for singly-linked list.
    # class ListNode(object):
    #     def __init__(self, val=0, next=None):
    #         self.val = val
    #         self.next = next
    @staticmethod
    def mergeTwoLists(l1, l2):
        """
        合并两个有序列表
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        if not (l1 and l2):
            return l1 if l1 else l2
        p = ListNode(None)
        head = p
        while l1 and l2:
            if l1.val < l2.val:
                p.next, l1 = l1, l1.next
            else:
                p.next, l2 = l2, l2.next
            p = p.next
        p.next = l1 if l1 else l2
        return head.next

    @staticmethod
    def removeDuplicates(nums):
        """
        删除排序数组中的重复项
        :type nums: List[int]
        :rtype: int
        """
        if not nums:
            return 0
        fast, slow = 1, 1
        while fast < (len(nums)):
            if nums[fast] in nums[:slow]:
                fast += 1
            else:
                nums[slow] = nums[fast]
                slow += 1
                fast += 1
        return slow

    @staticmethod
    def removeElement(nums, val):
        """
        移除元素
        :type nums: List[int]
        :type val: int
        :rtype: int
        """
        i, j = 0, 0
        while i < len(nums):
            if nums[i] != val:
                nums[j] = nums[i]
                j += 1
            i += 1
        return j

    @staticmethod
    def strStr(haystack, needle):
        """
        实现 strStr()
        :type haystack: str
        :type needle: str
        :rtype: int
        """
        # 字串比较法
        # for i in range(len(haystack) - len(needle) + 1):
        #     if haystack[i:len(needle) + i] == needle:
        #         return i
        # return -1
        # 双指针法
        if len(needle) == 0:
            return 0
        elif len(needle) > len(haystack):
            return -1
        i, j = 0, 0
        while i < len(haystack):
            pn = i + 1
            while haystack[i] == needle[j]:
                if j == len(needle) - 1:
                    return pn - 1
                i, j = i + 1, j + 1
                if i >= len(haystack):
                    return -1
            i, j = pn, 0
        return -1

    @staticmethod
    def searchInsert(nums, target):
        """
        搜索插入位置
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        left, right = 0, len(nums)
        while left < right:
            mid = (left + right) // 2
            if nums[mid] < target:
                left = mid + 1
            else:
                right = mid
        return left

    @staticmethod
    def countAndSay(n):
        """
        外观数列
        :type n: int
        :rtype: str
        """
        integer = '1'   # 初始化
        for i in range(n-1):
            count = []
            star, end = 0, 0
            while end < len(integer):
                if integer[end] == integer[star]:
                    end += 1
                else:
                    count.append(str(end - star))
                    count.append(integer[star])
                    star = end
            count.append(str(end - star))
            count.append(integer[star])
            star = end
            integer = ''.join(count)
        return integer


if __name__ == '__main__':
    Solution().countAndSay(n=4)
