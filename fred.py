from fredapi import Fred

fred = Fred(api_key='fc9c1f99dc7de6c6a975905a22097433')
unemployment = fred.get_series('UNRATE')  # US unemployment rate
interest = fred.get_series('FEDFUNDS')    # Federal Funds Rate

unemployment_df = unemployment.reset_index()
unemployment_df.columns = ['date', 'unemployment']

interest_df = interest.reset_index()
interest_df.columns = ['date', 'interest_rate']
