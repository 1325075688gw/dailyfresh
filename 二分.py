# 作者     ：gw
# 创建日期 ：2019-08-30  下午 12:03
# 文件名   ：二分.py

def func_left(arr,k):
    left, right = 0, len(arr)

    while left < right:
        mid = (left+right)//2
        if arr[mid] == k:
            right = mid
        elif k>arr[mid]:
            left = mid+1
        elif k<arr[mid]:
            right = mid
    return left

def func_right(arr,k):
    left, right = 0, len(arr)

    while left < right:
        mid = (left+right)//2
        if arr[mid] == k:
            left = mid+1
        elif k>arr[mid]:
            left = mid+1
        elif k<arr[mid]:
            right = mid
    return left


arr = [1,2,3,3,3,4,5,6]
k = 3
res_left = func_left(arr, k)
res_right = func_right(arr, k)
print(res_left,res_right)