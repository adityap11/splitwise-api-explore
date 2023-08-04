import numpy as np
import splitwise
import pandas as pd
from datetime import datetime as dt, timedelta
from credentials import CONSUMER_KEY, CONSUMER_SECRET, SPLITWISE_API_KEY
from helper.references import exp_cols

sw = splitwise.Splitwise(CONSUMER_KEY, CONSUMER_SECRET, api_key=SPLITWISE_API_KEY)


def extract_user_details(curr_user):
    """

    :param curr_user:
    :return:
    """
    details = {}
    user = sw.getUser(curr_user)
    details['user_id'] = curr_user
    details['first_name'] = user.first_name
    details['last_name'] = user.last_name
    details['email'] = user.email

    return details


def extract_expense_details(exp, curr_user):
    """

    :param exp:
    :return:
    """

    d = {}
    d['user_id'] = curr_user

    try:
        d['expense_id'] = exp.id
    except Exception as e:
        print(e)
        d['expense_id'] = "0"

    try:
        d['group_id'] = exp.group_id
    except Exception as e:
        print(e)
        d['group_id'] = "0"

    try:
        d['group_name'] = sw.getGroup(exp.group_id).name
    except Exception as e:
        print(e)
        d['group_name'] = "0"

    try:
        d['description'] = exp.description
    except Exception as e:
        print(e)
        d['description'] = "0"

    try:
        d['total_cost'] = exp.cost
    except Exception as e:
        print(e)
        d['total_cost'] = np.nan

    try:
        d['user_cost'] = next((user.getNetBalance() \
                              for user in exp.getUsers() if user.id == curr_user), 0)
    except Exception as e:
        print(e)
        d['user_cost'] = np.nan

    # try:
    #     d['involved_users'] = ', '.join(sorted([user.getFirstName() + " " + user.getLastName() for user in exp.getUsers() if user.id != curr_user]))
    # except Exception as e:
    #     print(e)
    #     d['involved_users'] = "0"
    #
    # try:
    #     d['involved_user_ids'] = ', '.join(sorted([user.id for user in exp.getUsers() if user.id != curr_user]))
    # except Exception as e:
    #     print(e)
    #     d['involved_user_ids'] = "0"

    try:
        d['person'] = ', '.join(sorted([user.getFirstName() + " " + user.getLastName() for user in exp.getUsers() if user.id != curr_user]))
    except Exception as e:
        print(e)
        d['person'] = "0"
    try:
        d['currency'] = exp.currency_code
    except Exception as e:
        print(e)
        d['currency'] = "0"

    try:
        d['date'] = exp.date
    except Exception as e:
        print(e)
        d['date'] = "0"

    try:
        d['category'] = exp.category.name
    except Exception as e:
        print(e)
        d['category'] = "0"

    return d


def get_all_expense_data():
    """

    :param sw: splitwise.Splitwise object
    :return: list of all expenses for the current user
    """
    print('in function')
    offset = 0
    lim = 100
    max_date = dt.now()
    min_date = dt(2022,12,31)
    exp_all = []
    while True:
        print(f'offset {offset}')
        exp = sw.getExpenses(offset=offset, limit=lim, dated_after=min_date, dated_before=max_date)
        if not exp:
            break
        offset += lim
        exp_all.extend(exp)

    curr_user = sw.getCurrentUser().getId()
    users = [curr_user]
    print(f'total expense items: {len(exp_all)}')

    data = []
    i = 0
    for exp in exp_all:
        if not i % 100:
            print(f'extracted details for {i} expense items')
        for user in exp.users:
            if user.id not in users:
                users.append(user.id)
            if user.id == curr_user and exp.deleted_at is None and exp.description != "Payment":
                # filter only current user expenses
                data.append(extract_expense_details(exp, curr_user))
        i += 1

    df = pd.DataFrame(data)

    return df
