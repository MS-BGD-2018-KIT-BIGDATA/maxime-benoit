import unittest


# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.

def string_times(string, n):
    return n*string

# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.
def array_front9(nums):
    #longueur=min(len(nums) & 4)
    length = len(nums)
    for i in range(0,length):
      if i <=3 and nums[i] == 9:
        return True
    return False


# Given a string, return the count of the number of times
# that a substring length 2 appears  in the string and also as
# the last 2 chars of the string, so "hixxxhi" yields 1 (we won't count the end substring).
def last2(string):
  if len(string) < 2:
    return ''
  pattern = string[-2:]
  count = 0
  for i in range(0,len(string) - 3):
    if string[i:i+2] == pattern:
      count += 1
  return count


def toto(x):
  return len(x)

#Write a program that maps a list of words into a list of
#integers representing the lengths of the correponding words.
def length_words(array):

  return [len (x) for x in array]

#write fizbuzz programm
def fizbuzz():
    return ''

#Write a function that takes a number and returns a list of its digits.
def number2digits(number):
  return [x for x in str(number)]

#Write function that translates a text to Pig Latin and back.
#English is translated to Pig Latin by taking the first letter of every word,
#moving it to the end of the word and adding 'ay'
def pigLatin(text):
  return ' '.join([ x[1:] + x[0]+'ay' for x in text.split(' ') ])

#Write a proramm that returna dictionary of occurences of the alphabet for a given string.
# Test it with the Lorem upsuj
#"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
def occurences(text):
  result = {}
  #[result[i]  if i in result else result[i] = 1 for i in text]
  return result

# Here's our "unit tests".
class Lesson1Tests(unittest.TestCase):
    fizbuzz()
    def testArrayFront9(self):
        self.assertEqual(array_front9([1, 2, 9, 3, 4]) , True)
        self.assertEqual(array_front9([1, 2, 3, 4, 9]) , False)
        self.assertEqual(array_front9([1, 2, 3, 4, 5]) , False)



def main():
    unittest.main()

if __name__ == '__main__':
    main()

