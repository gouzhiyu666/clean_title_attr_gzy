# data_comparison.py
import pandas as pd
import time
from clean_title_attr_gzy import clean_res_jixing_20109

def compare_ingredient_columns(old_file_path, new_file_path):
    """
    比较两个 CSV 文件中的 '适用人群' 列是否一致。

    参数:
        old_file_path (str): 旧数据文件的路径。
        new_file_path (str): 新数据文件的路径。

    返回:
        pd.DataFrame: 如果两列不一致，返回不一致的行数据；否则返回 None。
    """
    # 读取数据
    data_old = pd.read_csv(old_file_path)
    data_new = pd.read_csv(new_file_path)

    # 填充空值
    data_new['sku_name'].fillna('', inplace=True)
    data_new['attrs'].fillna('', inplace=True)
    data_old['剂型_attr'].fillna('', inplace=True)

    # 转换为字典列表
    data_new0 = data_new.to_dict(orient='records')

    # 清洗数据
    print("开始清洗数据...")
    t_start = time.time()
    res0 = [clean_res_jixing_20109(['20109'], x.get('title'), x.get('attrs')) for x in data_new0]
    t_end = time.time()
    print(f"清洗完成，耗时: {t_end - t_start:.2f} 秒")

    # 提取 '剂型_attr' 字段
    data_new['剂型_attr'] = [x[1] for x in res0]

    # 按 sku_sales 排序
    data_new = data_new.sort_values(by='sku_sales', ascending=False)
    data_old = data_old.sort_values(by='sku_sales', ascending=False)

    # 重置索引
    data_old = data_old.reset_index(drop=True)
    data_new = data_new.reset_index(drop=True)

    # 比较两列是否一致
    is_equal = data_old['剂型_attr'].equals(data_new['剂型_attr'])
    
    if is_equal:
        print("两列结果完全一致！")
        return None
    else:
        print("两列结果不一致！")
        # 逐行比较
        diff_rows = data_old['剂型_attr'] != data_new['剂型_attr']
        diff_count = diff_rows.sum()
        print(f"两列结果有 {diff_count} 行不一致。")
        # 输出不一致的行
        diff_data = pd.DataFrame({
            'old': data_old.loc[diff_rows, '剂型_attr'],
            'new': data_new.loc[diff_rows, '剂型_attr']
        })
        print("不一致的行数据：")
        print(diff_data)
        return diff_data


if __name__ == "__main__":
    # 示例文件路径
    old_file_path = '叶子类目qa验证准确率_20109_0.csv'
    new_file_path = '叶子类目qa验证准确率_20109_0.csv'

    # 调用方法并比较数据
    diff_data = compare_ingredient_columns(old_file_path, new_file_path)

    # # 如果有不一致的数据，可以进一步处理
    # if diff_data is not None:
    #     # 例如：将不一致的数据保存到新的 CSV 文件中
    #     diff_data.to_csv('不一致的数据.csv', index=False)
    #     print("不一致的数据已保存到 '不一致的数据.csv'")