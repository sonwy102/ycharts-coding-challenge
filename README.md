# YCharts Coding Challenge

Completed by Wooyang Son

## Problem Summary

Write a program that performs unit reconciliation (i.e. Does the transaction
history add up to the number of shares/cash value queried from the account
in bank?)

## Quickstart

Clone repo to your dev environment:

`$ git clone https://github.com/sonwy102/ycharts-coding-challenge.git`

Run python script (make sure you have Python 3+ installed in your dev environment!)

`$ python3 reconciliation.py`

Then, access the recon.out file (`recon_out.txt`) inside the `/data` directory

## Notes/Discussion
### Use of Python Libraries
I considered importing and using the `pandas` library for my solution. Processing
and analyzing data using pandas could improve the runtime of the solution if we are dealing with larger data
and/or much more complex data manipulation.

However, given a small dataset in this case, I went with a simple, straightforward
solution. Additionally, I decided against using pandas so that I could implement
all of the logic myself with the intention of writing a solution that demonstrates
my problem-solving skills from scratch more explicitly for the reader.

### Use of Database
Another way to solve this problem is to utilize a relational
database to store the account's positions and transaction histories. This
would be especially helpful if we are working with a much larger dataset and
we need to consider memory management.

This approach keeps the data organized in one place and offers a
convenient way of querying, updating, and checking data across all accounts. 
Calculating discrepancies would also become more convenient when we leverage 
relationships between positions and transactions defined in the database. 



