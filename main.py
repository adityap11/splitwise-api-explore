import splitwise
from datetime import datetime as dt
# from credentials import CONSUMER_KEY, CONSUMER_SECRET, SPLITWISE_API_KEY
from helper.functions import *

# sw = splitwise.Splitwise(CONSUMER_KEY, CONSUMER_SECRET, api_key=SPLITWISE_API_KEY)
expenses = get_all_expense_data()
expenses.to_csv('output/expenses.csv')
print()