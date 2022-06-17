import pickle

with open('Q3000US.txt', 'r') as file_in:
    lines = file_in.readlines()

    # All tradeable stock tickers
    unformatted_tickers = lines[0].split('Equity(')
    all_tickers = []
    for unformatted_ticker in unformatted_tickers:
        formatted_ticker = unformatted_ticker[unformatted_ticker.find('[') + 1:unformatted_ticker.find(']')]
        all_tickers.append(formatted_ticker)
    all_tickers.pop(0)

    # Index points of Q3000US
    unformatted_indexes = lines[1].split('], [')[1].split(", ")
    unformatted_indexes[-1] = unformatted_indexes[-1][:unformatted_indexes[-1].find(']')]
    ticker_indexes = [int(x) for x in unformatted_indexes]

    # top 3000 tradeable stocks
    q3000us = []
    for index in ticker_indexes:
        q3000us.append(all_tickers[index])

    q3000us.sort()

with open('tickers', 'wb') as pickle_out:
    pickle.dump(q3000us, pickle_out)
