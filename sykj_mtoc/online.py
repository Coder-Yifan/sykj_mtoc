import requests
from pandas import DataFrame


class RequstModel():
    def __init__(self, url, modelUuid, version, modelType='P'):
        """

        :param url: string
            模型平台url
        :param modelUuid: string
            模型uuid
        :param version: string
            模型版本
        :param modelType: string
            模型类型，默认值为P
        """
        self.url = url
        self.modelUuid = modelUuid
        self.version = version
        self.modelType = modelType

    def request_json(self, json):
        """

        :param json: dict
            单条数据请求
        :return: json
            接口返回结果
        """
        if not isinstance(json, dict):
            raise Exception('json shoule be a dict!!')
        id_col = {'modelUuid': self.modelUuid, 'version': self.version, 'modelType': self.modelType, 'seqId': '2023'}
        id_col.update(json)
        r_reg = requests.post(url=self.url, json=id_col)
        return r_reg.json()

    def request_data(self, data, features_online=None):
        """

        :param data: DataFrame
            批量数据的dataframe
        :param features_online: string list
            线上模型的变量名称，默认值为传入数据的列名
        :return: DataFrame
            接口返回结果
        """
        if not isinstance(data, DataFrame):
            raise Exception('data shoule be a DataFrame!!')
        features_online = data.columns.tolist()
        results = []
        acc_index = []
        id_col = {'modelUuid': self.modelUuid, 'version': self.version, 'modelType': self.modelType,
                  'seqId': '2023'}
        for index in data.index:
            request_json = dict(zip(features_online, [str(x) for x in data.loc[index, :].values]))
            id_col.update(request_json)
            r_reg = requests.post(url=self.url, json=id_col)
            response = r_reg.json().get('data')
            try:
                if not response:
                    raise Exception('{} index error'.format(index) + r_reg.json().get('message'))
                results.append(r_reg.json().get('data'))
                acc_index.append(index)
            except:
                print('{} index error'.format(index) + r_reg.json().get('message'))
                continue
        result_df = DataFrame.from_dict(results)
        result_df['index'] = acc_index
        result_df.set_index('index', drop=True, inplace=True)
        return result_df
