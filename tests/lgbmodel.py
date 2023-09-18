import pandas as pd
import lightgbm as lgb

from sykj_mtoc import export_to_python
data = pd.read_csv('./uci_credit.csv')
features = [x for x in data.columns.tolist() if x not in ['ID','default.payment.next.month']]
data['y'] = data['default.payment.next.month']
dbtrain = lgb.Dataset(data[features],label=data['y'])
params = {
    'eta':0.01,
    'max_depth':3
}
model = lgb.train(params,train_set=dbtrain)
code = export_to_python(model)
# with open('./code_gen_sample/xgbclassifier.py','w') as f:
#     f.write(code)
