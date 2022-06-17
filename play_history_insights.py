import pickle
from datetime import datetime

from joblib import Parallel, delayed
from pandas.tseries.offsets import BDay
from tqdm import tqdm


def loadHistory():
    with open('suggested_play_history', 'rb') as pickle_in:
        return pickle.load(pickle_in)


history_df = loadHistory()

# for date in history_df.index.get_level_values('date').tolist():


potential_plays = potential_plays.append(Parallel(n_jobs=num_cores)(delayed(checkGap)(ticker)
                                                                    for ticker in tqdm(tickers)))

potential_plays.min_volume_day.plot().show()

today = datetime.today().date()
previous_two_months = (today - BDay(250)).date()

# with open('suggested_play_history', 'rb') as pickle_in:
#     df = pickle.load(pickle_in)
#
# df.plot
# plt.show()
