def kidsWithCandies(candies, extraCandies):
        """
        :type candies: List[int]
        :type extraCandies: int
        :rtype: List[bool]
        """
        max = 0
        for i in candies:
            if i > max:
                max = i
        
        greatest_numbers = []
        for i in candies:
            if (i+extraCandies) >= max:
                greatest_numbers.append("true")
            else:
                greatest_numbers.append("false")       

        return greatest_numbers


if __name__ == "__main__":
    #print(kidsWithCandies([2,3,5,1,3], 3))
    thingy = "hello"
    thingy[1] = 'a'
    print(thingy)