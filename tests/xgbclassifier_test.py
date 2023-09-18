import pandas as pd
from xgboost import XGBClassifier
from sykj_mtoc import export_to_python
data = pd.read_csv('./uci_credit.csv')
features = [x for x in data.columns.tolist() if x not in ['ID','default.payment.next.month']]
data['y'] = data['default.payment.next.month']
model = XGBClassifier(max_depth=3,n_estimators=10)
model.fit(data[features],data['y'])
isinstance(model,XGBClassifier)
code = export_to_python(model)
# with open('./code_gen_sample/xgbclassifier.py','w') as f:
#     f.write(code)
#
# from tests.code_gen_sample.xgbclassifier import score
# print(score(data.loc[0,features].values)[1])
# print(model.predict_proba(data[features])[0,1])