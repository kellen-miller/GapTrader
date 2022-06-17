import multiprocessing
import pandas as pd
import pandas_datareader as pdr
import pickle
import smtplib
import ssl
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from joblib import Parallel, delayed
from pandas.tseries.offsets import BDay
from tqdm import tqdm


def loadTickers():
    with open('tickers', 'rb') as pickle_in:
        return pickle.load(pickle_in)


def checkGap(ticker):
    try:
        today = datetime.today().date()
        previous_two_months = (today - BDay(40)).date()

        daily_data = pdr.DataReader(ticker, start=previous_two_months, end=today, data_source='yahoo')

        avg_volume = daily_data.Volume.mean()
        gap_percent = (daily_data.High[-1] - daily_data.Close[-2]) / daily_data.High[-1]

        df = pd.DataFrame([[daily_data.index[-1], ticker, gap_percent, avg_volume]],
                          columns=['date', 'ticker', 'gap_percent', 'avg_volume']).set_index(['date', 'ticker'])
        df = df[((df.gap_percent > .1) | (df.gap_percent < -.1)) & (df.avg_volume > 1000000)]
        return df
    except:
        pass


def exportResults(plays):
    with open('suggested_play_history', 'rb') as pickle_in:
        df = pickle.load(pickle_in)

    df = df.append(plays)

    with open('suggested_play_history', 'wb') as pickle_out:
        pickle.dump(df, pickle_out)


def emailResults(results):
    recipients = ['kellen.miller12@gmail.com']
    emaillist = [elem.strip().split(',') for elem in recipients]

    msg = MIMEMultipart()
    datetime = str(results.index[0][0])
    msg['Subject'] = "Daily Plays - " + datetime[:datetime.find(" ")]
    msg['From'] = 'kellen.dev.email@gmail.com'
    password = "esB46*CpkqJuZqrM"

    results['url'] = "https://finance.yahoo.com/quote/" + results.index.get_level_values('ticker')
    html = """\
    <html>
      <head>Potential Plays</head>
      <body>
        {0}
      </body>
    </html>
    """.format(results.to_html(justify='center'))
    part1 = MIMEText(html, 'html')
    msg.attach(part1)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(msg['From'], password)
        server.sendmail(msg['From'], emaillist, msg.as_string())
        print("\nEmail sent successfully!")


potential_plays = pd.DataFrame(columns=['date', 'ticker', 'gap_percent', 'avg_volume']).set_index(['date', 'ticker'])
num_cores = multiprocessing.cpu_count()
tickers = loadTickers()

potential_plays = potential_plays.append(Parallel(n_jobs=num_cores)(delayed(checkGap)(ticker)
                                                                    for ticker in tqdm(tickers)))
potential_plays.drop(columns='avg_volume', inplace=True)
potential_plays = potential_plays.iloc[(-potential_plays['gap_percent'].abs()).argsort()]

print("\n", potential_plays)
exportResults(potential_plays)
emailResults(potential_plays)
