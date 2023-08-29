import pandas as pd
from lightgbm import LGBMClassifier
from m2cgen import export_to_python
data = pd.read_csv('./uci_credit.csv')
features = [x for x in data.columns.tolist() if x not in ['ID','default.payment.next.month']]
data['y'] = data['default.payment.next.month']
model = LGBMClassifier(max_depth=3,n_estimators=10)
model.fit(data[features],data['y'])
isinstance(model,LGBMClassifier)
code = export_to_python(model)
with open('./code_gen_sample/lgbclassifier.py','w') as f:
    f.write(code)

# from tests.code_gen_sample.xgbclassifier import score
# print(score(data.loc[0,features].values)[1])