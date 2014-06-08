This is a simple test runner for learning datastructures. The output is in the following format

100       16191
1000      111517
10000     1012842
100000    10017391

Each line is the size of the data and the time it takes to run n test cases (n = 100, but that can be changed).
The way it works is as follows.

First, it talks to the tester module to generate test data. For example,
if you wanted to test search datastructures, test data would be an unsorted list
of numbers.

Then it talks to the solution module to generate the datastructure corresponding to the
n elements. This time is not reported today, but is recorded and can be reported by
changing the runner

Then it actually computes the number shown above by running n (= 100) instances of
  1. generate testcase
  2. run testcase
  3. verify result

It prints the time for the above loop for various sizes of data. See examplerunner for
example which uses the runner for various kinds of testcases
