import pandas as pd
from QualtricsData import QualtricsData
from liwc import Liwc

# -- init -- #
liwc = Liwc()
df_proc = pd.read_csv('../../data/proc/reappraisal_text_110320_proc_export012421.csv')

df_situations = df_proc.filter(regex='^pid|^situation|^rethink|^na_|^pa_', axis=1)

df_long = pd.wide_to_long(df_situations,
                          ['situation', 'rethink', 'na_pre', 'na_post', 'pa_pre', 'pa_post'],
                          sep='_',
                          i='pid',
                          j='situation_num')


# -- create liwc dataframe -- #
df_liwc_situation = pd.concat([pd.DataFrame({'pid': [x[0] for x in df_long.index],
                                   'situation_num': [x[1] for x in df_long.index]}),
                               pd.DataFrame(df_long['situation'].map(lambda x: liwc.parse(x.split(' '))).tolist()),
                               pd.DataFrame({'text_type': pd.Series('situation').repeat(df_long.shape[0])}).reset_index(drop=True)], axis=1)
df_liwc_rethink = pd.concat([pd.DataFrame({'pid': [x[0] for x in df_long.index],
                                           'situation_num': [x[1] for x in df_long.index]}),
                             pd.DataFrame(df_long['rethink'].map(lambda x: liwc.parse(x.split(' '))).tolist()),
                             pd.DataFrame({'text_type': pd.Series('situation').repeat(df_long.shape[0])}).reset_index(drop=True)], axis=1)

df_liwc = pd.concat([df_liwc_situation, df_liwc_rethink], axis=0)

# -- export liwc dataframe -- #
df_liwc.to_csv('../../data/proc/situation_rethink_liwc.csv', index=False)