import os
import os.path as osp

import pandas as pd
import numpy as np

from rlylutils.configs.cfg import Cfg
from rlylutils.decorators.decorators import Decorator
from rlylutils.files_op import Filesop

__all__ = ['Excop']


@Decorator.cdec(Cfg.default['param'])
class Excop(Filesop):
    """
    未完成：filter,mask,where,shift
    """
    def __new__(cls, *args, **kw):
        ob = super().__new__(cls, *args, **kw)
        ob.default = cls.default
        ob.default.update({'Primarykey': ''})
        return ob

    def __init__(self):
        super().__init__()
        self.__dict__.update(self.default)
    
    def __iter__(self):
        ...

    @staticmethod
    def create_df(rows, cols):
        return pd.DataFrame(np.arange(rows*cols).reshape(rows, cols))

    @staticmethod
    def read(path, header=None, sheet_name='Sheet1', engine='openpyxl'):
        '''
        
        '''
        if osp.splitext(path)[-1] in ['.csv', '.tsv']:
            print('csv has no sheetname(pandas)')
            df = pd.read_csv(path, header=header)
        else:
            df = pd.read_excel(path, sheet_name=sheet_name, engine=engine, header=header)  # 旧平台表路径
        return df

    @staticmethod
    def write(df, path, header=True, index=False, sheet_name='Sheet1'):
        '''
        关键是csv不能手动打开，要用python，编码utf-8_sig保存，另存为xlsx格式就可以解决断行和中文乱码问题
        '''
        if osp.splitext(path)[-1] == '.csv':
            
            # index参数设置为False表示不保存行索引,header设置为False表示不保存列索引
            print('csv has no sheetname(pandas)')
            df.to_csv(path,  index=index, header=header, encoding='utf-8-sig')
        else:
            with pd.ExcelWriter(path) as xlsx:
                df.to_excel(xlsx, sheet_name=sheet_name, header=header, index=index, encoding='utf-8')

    @staticmethod
    def colname_list(df):
        """
        R
        :param df:
        :return:
        """
        return df.columns.tolist()

    @staticmethod
    def vlookup(df, other_df, df_key_col_name, other_df_key_col_name, how='left'):
        return pd.merge(df, other_df, left_on=df_key_col_name, right_on=other_df_key_col_name, how=how)

    @staticmethod
    def filter(df, col_name, condition, val):
        """
        筛选
        :param col_name:
        :param condition:
        :param val:
        :return:
        """
        ...

    @staticmethod
    def sorted(df, colname_list: list, ascending: list or bool):
        """
        R
        :param df:
        :param colname_list:
        :param ascending:
        :return: df
        """
        return df.sort_values(by=colname_list, ascending=ascending)

    @staticmethod
    def cell_modify(df, row, colname, value):
        df.loc[row, colname] = value
        return df

    @staticmethod
    def cell_val(df, row, colname):
        return df.loc[row, colname]

    @staticmethod
    def row_stack(df1, df2):
        """
        按行拼接 R
        :param df1:
        :param df2:
        :return:
        """
        return pd.concat([df1, df2], axis=0)


    @staticmethod
    def df_info(df):
        # R
        df.info()

    @staticmethod
    def col_datetime(df):
        # dates = pd.to_datetime(pd.Series(['2022-7-10 13:14:55', '2022-7-20']), format='%Y-%m-%d %H:%M:%S')
        # print("返回日期值：", dates.dt.date)
        # print("返回时间：", dates.dt.time)
        # print("返回第几季度：", dates.dt.quarter)
        # print("返回年份：", dates.dt.year)
        # print("返回年中的第几天：", dates.dt.dayofyear)
        # print("返回年中的第几周：", dates.dt.isocalendar().week)
        # print("返回周几（0-6）：", dates.dt.dayofweek)
        # print("返回具体的周几名称，如Friday：", dates.dt.day_name())
        # print("返回日期所在的月份总天数：", dates.dt.days_in_month)
        ...

    @staticmethod
    def col_astype(df, colname, new_type):
        """
        列数据改变数据类型 R
        """
        df[colname] = df[colname].astype(new_type)
        return df

    @staticmethod
    def col_drop_duplicates(df, colname_list: list, keep='first'):
        """
        按列数据去重 R
        :param df:
        :param colname_list:
        :param keep: first、last、False 默认为 first，表示只保留第一次出现的重复项，删除其余重复项，last 表示只保留最后一次出现的重复项，False 则表示删除所有重复项
        :return:
        """
        df.drop_duplicates(subset=colname_list, keep=keep, inplace=True)

    @staticmethod
    def col_float2int(df, colname):
        """
        R
        :param df:
        :param colname:
        :return:
        """
        df[colname] = df[colname].apply(lambda x: int(x) if x == x else "")
        return df

    @staticmethod
    def col_function_singlecol(df, tar_colname, func, src_colname):
        """
        按单变量函数处理指定列数据 R
        """
        df[tar_colname] = df[src_colname].apply(lambda x: func(x) if not pd.isnull(x) else "")
        return df

    @staticmethod
    def col_function_muticol(df, tar_colname, func, src_colname_list: list):
        """
        按多变量函数处理指定列数据 R
        df['col3'] = df.apply(lambda x: x['col1'] + 2 * x['col2'], axis=1)
        """
        def new_lambda(x, func, src_colname_list):
            colnames_var = [x[colname] for colname in src_colname_list]
            colnames_var = tuple(colnames_var)
            return func(*colnames_var)

        df[tar_colname] = df.apply(lambda x: new_lambda(x, func, src_colname_list), axis=1)
        return df

    @staticmethod
    def df_groupby(df,
                   groupby_colname_list: list,
                   cal_colname_list: list,
                   cal_method: 'sum,mean,std,min,max' = 'sum'):
        """
        分类汇总 R
        :param df:
        :param groupby_colname_list:
        :param cal_colname_list:
        :param cal_method:
        :return:
        """
        df = df.groupby(groupby_colname_list)[cal_colname_list]
        if cal_method == 'sum':
            df = df.sum()
        elif cal_method == 'mean':
            df = df.mean()
        elif cal_method == 'std':
            df = df.std()
        elif cal_method == 'min':
            df = df.min()
        elif cal_method == 'max':
            df = df.max()

        return df

    @staticmethod
    def row_reset_index(df):
        """
        重置索引
        :param df:
        :return:
        """
        return df.reset_index()

    @staticmethod
    def col_strip(df, colname):
        """
        列数据去首尾空格 R
        """
        df[colname] = df[colname].str.strip()
        return df


    @staticmethod
    def column_add(df, insert_col_num, addcol_name, fill_value):
        """
        被插入位置的原列会往右移 R
        :param df:
        :param insert_col_num:
        :param addcol_name:
        :param fill_value:
        :return:
        """
        df.insert(loc=insert_col_num, column=addcol_name, value=fill_value)

    @staticmethod
    def column_remove(df, del_column_name) -> pd.DataFrame:
        """
        R
        :param del_column_name:
        :return:
        """
        return df.drop([del_column_name], axis=1)

    @staticmethod
    def row_remove(df, del_row) -> pd.DataFrame:
        """
        R
        :param del_row:
        :return:
        """
        return df.drop(index=del_row, axis=0)

    @staticmethod
    def col_val_replace(df, colname, ori_val, new_val):
        """
        指定列替换值 R
        """
        df.replace({colname: {ori_val: new_val}}, inplace=True)

    @staticmethod
    def fillna(df, fill_val) -> pd.DataFrame:
        """
        NAN值填充为指定值  R
        :param fill_val:
        :return:
        """
        return df.fillna(value=fill_val)

    @staticmethod
    def df2numpy(df) -> np.array:
        """
        R
        :param df:
        :return:
        """
        return df.to_numpy()

    @staticmethod
    def numpy2df(np_array, rowname_list: list or None = None, colname_list: list or None = None) -> pd.DataFrame:
        """
        R
        :param np_array:
        :param rowname_list:
        :param colname_list:
        :return:
        """
        return pd.DataFrame(np_array, index=rowname_list, columns=colname_list)

