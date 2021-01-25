import pandas as pd
from QualtricsData import QualtricsData
from liwc import Liwc

# -- init -- #
qd = QualtricsData('../../data/raw/reappraisal_text_110320_January+24%2C+2021_19.10.csv')

# -- preproc qualtrics -- #
qd.rename_vars('../../lib/var_codebook.csv')
qd.recode_values('../../lib/value_codebook.csv')

qd.df_proc = qd.df_proc.dropna(subset=['pid']).copy().reset_index()
qd.df_proc = qd.df_proc.dropna(subset=['ac_text']).copy().reset_index()

failed_ac_pids = qd.df_proc.loc[(qd.df_proc['ac_1']!='pass') | (qd.df_proc['ac_2']!='pass'), 'pid']
qd.df_proc = qd.df_proc[~qd.df_proc['pid'].isin(failed_ac_pids)]

# -- export dataframe -- #
qd.df_proc.to_csv('../../data/proc/reappraisal_text_110320_proc_export012421.csv', index=False)