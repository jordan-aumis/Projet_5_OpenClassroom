def fizzBuzz(number):
  index = 0
  while index <= number:
    if index % 2 == 0:
      result ="{}fizz".format(index)
      print(result)
    else:
      result ="{}buzz".format(index)
      print(result)
    index +=1

fizzBuzz(16)