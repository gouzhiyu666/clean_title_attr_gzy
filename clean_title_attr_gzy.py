# encoding:utf-8
import os
DIR_CURRENT = os.path.dirname(os.path.abspath(__file__))
import pandas as pd
import time
import json
import glob
import re
from collections import defaultdict

pd.set_option('display.max_rows', 500)


#with open('%s/entity_dic.json' % DIR_CURRENT, 'r', encoding='utf-8') as f:
#    entity_dic = json.load(f)
#with open('%s/entity_xiangshui_danpin.json' % DIR_CURRENT, 'r', encoding='utf-8') as f:
#    entity_dic1 = json.load(f)
#with open('%s/addition_dic.json' % DIR_CURRENT, 'r', encoding='utf-8') as f:
#    add_dic = json.load(f)
#with open('%s/ggmap.json' % DIR_CURRENT, 'r', encoding='utf-8') as f:
#    ggmap = json.load(f)
#entity_dic.extend(entity_dic1)


def get_attrs0(attr_str: str, key_list: list):
    """
    重写了get_attrs,严格匹配属性的key。
    原来的get_attrs为模糊匹配，存在问题。
    比如，匹配`适宜人群`时,会把`不适宜人群`也放进去
    :param attr_str: 属性字符串，格式为 'key1:value1||key2:value2||....'
    :param key_list: 需要匹配的属性的key
    :return: dict,对应属性键值的字典
    """
    if not attr_str:
        return {}
    attrs = attr_str.split('||')
    attrs = {x[0]: x[1] for x in map(lambda x: x.split(':'), attrs) if x[0] in key_list}
    return attrs

#def clean_res_jixing_20109(cpath, sku_name, title, attrs):
def clean_res_jixing_20109(cpath, title, attrs):
    """获取剂型信息，用于类目20109，优先级：attrs->title"""

    key_list = ['产品剂型', '剂型']
    cat1 = cpath[0]
    if cat1 in ['20109']:
        attrs = get_attrs0(attrs, key_list=key_list)
        #value = get_jixing(cat1, sku_name, attrs, title)
        value = get_jixing(cat1, attrs, title)
        return '剂型', value
    else:
        return '剂型', ''

#def get_jixing(cat1, sku_name, attrs, title):
def get_jixing(cat1,  attrs, title):
    """在属性、标题里去找剂型相关"""
    #sku = str(sku_name)
    attr = str(attrs)
    title = str(title)
    #res = clean_jixing(cat1, 'sku', '剂型', sku)
    res = clean_jixing(cat1, 'attr', '剂型', attr)
    if res == '':
        #res = clean_jixing(cat1, 'attr', '剂型', attr)
    #if res == '':
        res = clean_jixing(cat1, 'title', '剂型', title)
    return res


def clean_jixing(cat1,_from, k, v):
    res_list = []
    normal_rule = ['滴剂', '胶囊', '口服液', '片剂', '丸剂', '固体饮料', '口服散剂', '咀嚼片', '茶', '膏剂']
    for jx in normal_rule:
        if jx in v:
            res_list.append(jx)
    if _from == 'title':
        if '粉' in v and ('宠粉' or '片' or '粉丝') not in v:
            res_list.append('粉剂')
        if '凝胶糖果' in v or '软糖' in v:
            res_list.append('软糖')
        if '颗粒' in v or '冲剂' in v:
            res_list.append('颗粒/冲剂')
        if '果冻' in v:
            res_list.append('果冻型')
        if '压片糖' in v or '润喉糖' in v:
            res_list.append('压片糖')
        if '钙片' in v or '银片' in v or '护肝片' in v or '含片' in v or '咀嚼片' in v or ('片' in v and '素' in v) or '硒片' in v or '丁酸片' in v or '净肝片' in v or ('片' in v and '维' in v) :
            res_list.append('片剂')
        if '阻断饮' in v or '功能饮' in v or ('饮' in v and '固体' not in v) or '液态饮' in v or '口服饮' in v or '净斑饮' in v or '辛酸饮' in v or '代谢饮' in v:
            res_list.append('口服液')
        if '喷雾' in v:
            res_list.append('喷雾剂')
        if '丸' in v:
            res_list.append('丸剂')
        if '贴' in v and '补贴' not in v:
            res_list.append('透皮贴剂')

    if _from == 'attr':
        if '粉剂' in v or '粉末' in v:
            res_list.append('粉剂')
        if '凝胶糖' in v or '软糖' in v:
            res_list.append('软糖')
        if '颗粒' in v or '冲剂' in v:
            res_list.append('颗粒/冲剂')
        if '果冻型' in v:
            res_list.append('果冻型')
        if '压片糖' in v:
            res_list.append('压片糖')
        if '压片' not in v and '片' in v:
            res_list.append('片剂')
        if '饮料' in v and '固体饮料' not in v:
            res_list.append('口服液')
        if '喷雾剂' in v:
            res_list.append('喷雾剂')
        if '丸' in v and '片' not in v:
            res_list.append('丸剂')

    res_list = list(set(res_list))
    res_list.sort()
    res = '\x02'.join(res_list)
    return res


def test1():
    cpath = ['20109']
    attrs = '''颜色分类:1盒 基础装||颜色分类:保密发货 超长售后||颜色分类:4盒 周期装【买3送1】||颜色分类:4盒 周期装【买3送1】||颜色分类:2盒 调理装【9折】||颜色分类:12盒 奢享装【买8送4】||颜色分类:7盒 巩固装【买5送2】||生产日期:2024年04月10日 至 2024年04月20日||厂名:德国进口HerLiyConway||厂址:德国进口HerLiyConway||配料表:饮用水，赤藓糖醇，木瓜，葛根，紫云英花粉，针叶 樱桃果浓缩汁，大豆，枸杞子，牛油果，茶树花，山药，柠檬酸， 阿萨伊果，金顶侧耳浓缩粉，三氯蔗糖。||储藏方法:请存放在阴凉干燥处，密封并避免阳光直射。||保质期:900天||品牌:Herliyconway||品名:赫丽康维木瓜葛根饮||适用人群:成人女性||产地:德国||包装方式:盒装||产品剂型:口服液||用法:建议每天饮用1瓶(25毫升)||食用提示:打开盖子立即饮用，使用前摇匀。||适用性别:女||有效期:24个月以上'''
    title = '德国进口木瓜葛根粉姿部胶原蛋白肽天然植物麦角硫因液态饮新剂型'
    #sku_name = ''
    #res = clean_res_jixing_20109(cpath,sku_name,title,attrs)
    res = clean_res_jixing_20109(cpath,title,attrs)
    print(res)

def test2():
    cpath = ['20109']
    attrs = '''套餐详情:Bloomage Health动能丸30粒/瓶年轻高纯度麦角硫因50mg亚精胺口服-单盒x1'''
    title = 'Bloomage Health动能逆龄丸30粒/瓶年轻高纯度麦角硫因50mg亚精胺'
    res = clean_res_jixing_20109(cpath,title,attrs)
    print(res)

def test3():
    cpath = ['20109']
    attrs = '''保质期:24月||产地:中国大陆||产品名称:花旗参茶固体饮料||品牌:EAGLE’S/鹰牌||生产企业名称:健康药业（中国）有限公司||食品生产许可证编号:SC12744030500626'''
    title = '【年货节】鹰牌1盒/2盒/3盒/4盒可选择装花旗参茶固体冲调饮料'
    res = clean_res_jixing_20109(cpath,title,attrs)
    print(res)

def test4():
    cpath = ['20109']
    attrs = '''保质期:24月||产品名称:虾青素凝胶糖果||产地:中国大陆||品牌:五个女博士||生产企业名称:纽斯葆广赛（广东）生物科技股份有限公司||食品生产许可证编号:SC11344018400184||规格（粒/袋/ml/g）:30粒/瓶'''
    title = '【宠粉专属】五个女博士12mg专利左旋虾青素凝胶糖果'
    res = clean_res_jixing_20109(cpath,title,attrs)
    print(res)

def test5():
    cpath = ['20109']
    attrs = '''套餐详情:Nature'sKey褪黑素小金瓶晚安片3mg/粒升级版(添加B6)60粒-默认x2'''
    title = '【到手2瓶】美国Natures Key褪黑素小金瓶晚安片3mg/粒60粒'
    res = clean_res_jixing_20109(cpath,title,attrs)
    print(res)

def test6():
    cpath = ['20109']
    attrs = '''保质期:1095天||产地:中国大陆||是否属于消字号:否||产品名称:褪黑素晚安贴||生产企业名称:优微(珠海)生物科技有限公司企业||规格:9片/盒||适用对象:成人'''
    title = '【晚安超人】Unice可溶性微晶褪黑素晚安贴睡眠成人1.25mg/贴'
    res = clean_res_jixing_20109(cpath,title,attrs)
    print(res)

def test7():
    cpath = ['20109']
    attrs = '''套餐详情:【秦岚推荐】SWISSE斯维诗浓缩奶蓟草提取物净化片120片/瓶-默认x1'''
    title = '【细胞级养护】Swisse净肝片120片/瓶奶蓟草净化片熬夜加班澳洲进口'
    res = clean_res_jixing_20109(cpath,title,attrs)
    print(res)

def test8():
    cpath = ['20109']
    attrs = '''套餐详情:【达播FB】SWISSE斯维诗柠檬酸钙维D迷你片娘娘钙300片/瓶进口-默认x3、【达播FB】Swisse/斯维诗儿童DHA深海鱼油胶囊60粒/瓶-默认x1'''
    title = '【春节送礼】Swisse柠檬酸钙维D钙迷你片300片/瓶-zYY'
    res = clean_res_jixing_20109(cpath,title,attrs)
    print(res)

def test9():
    cpath = ['20109']
    attrs = '''保质期:24月||产品名称:多维小蓝片||产地:中国大陆||品牌:白云山||生产企业名称:山东凝善堂生物科技有限公司||食品生产许可证编号:SC13037150100941||规格（粒/袋/ml/g）:0.6g*30粒'''
    title = '【拍一发八】白云山 L-精氨酸锌硒多维小蓝片 CS-A4'
    res = clean_res_jixing_20109(cpath,title,attrs)
    print(res)

def test10():
    cpath = ['20109']
    attrs = '''粉丝福利 无糖型南极磷虾油 海洋磷脂和Omega-3 63g/盒 YH'''
    title = '保质期:24月||产地:中国大陆||净含量:63g||生产企业名称:安徽感喻药业有限公司||品牌:润龄堂||食品生产许可证编号:SC10734122230595||贮存条件:常温||包装方式:包装'
    res = clean_res_jixing_20109(cpath,title,attrs)
    print(res)

if __name__ == '__main__':
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    test7()
    test8()
    test9()
    test10()