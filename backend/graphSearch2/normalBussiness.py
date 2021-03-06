# @Language: python3
# @File  : normalBussiness.py
# @Author: LinXiaofei
# @Date  : 2020-06-22
"""



"""

import sys
import os
import numpy as np

project_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(project_path)

from graphSearch2.graphSearch3 import graphSearch
from nlu.formWords import formWords


class normalBussiness(object):

    def __init__(self):
        self.graph_util = graphSearch()
        self.form_util = formWords()




    def seacrchAll(self,longWords,shortWords):
        """

        :param longWords: 问句和属性值中较长的一方
        :param shortWords: 较短的一方
        :return: 较短的那方匹配情况
        """
        count = 0.
        for sw in shortWords:
            if sw in longWords:
                count = count+1
        return count

    def matchFuzzySearch(self, words, triple):
        """
        匹配三元组的o和句子
        """

        form_words = self.form_util.preProcessWords(words)

        ans_con = []
        count_rate = []

        for name,key,value in triple:

            value = self.form_util.preProcessWords(value)
            while (name in form_words):
                form_words = form_words.replace(name, '')
            while (name in value):
                value = value.replace(name, '')
            count = self.seacrchAll(value, form_words)
            c_len = len(form_words)
            if float(count) / float(c_len) >= 0.65:
                ans_con.append([name,key,value])
                count_rate.append(count / c_len)

        if ans_con != []:

            max_index = np.argmax(np.array(count_rate))
            return ans_con[max_index]
        return None


    def matchProConWithPro(self, words, deal_entity,property):
        """
        根据实体携带的属性信息和问句原文匹配得到与答案相符的属性信息
        该函数制定了属性名字
        1. 遍历实体所有的属性信息
        2. 按字符匹配问句和属性信息
        3. 2得到空则按向量相似度得到匹配信息
        4. 2,3均空则返回空

        这个没有答案二次reverse匹配
        :param words: 问句
        :param deal_entity: 实体及其信息
        :return: 答案或空
        """

        form_words = self.form_util.preProcessWords(words)
        ans_con = []
        count_rate = []


        for name, content in deal_entity.items():
            """
            抽取出的实体的属性
            """
            pro = np.array(content['p'])

            """
            去掉问题中的实体方便匹配
            """
            while (name in form_words):
                form_words = form_words.replace(name, '')

            for p in pro:
                if p[0] != property[0]:
                    continue
                con = self.form_util.preProcessWords(p[1])

                while (name in con):
                    con = con.replace(name, '')

                if len(con) > len(form_words):
                    c_len = len(form_words)
                    count = self.seacrchAll(con, form_words)

                else:

                    c_len = len(con)
                    count = self.seacrchAll(form_words, con)
                if float(count) / float(c_len) >= 0.65:
                    ans_con.append([name, p[0], p[1]])
                    count_rate.append(count / c_len)
        if ans_con != []:

            max_index = np.argmax(np.array(count_rate))
            return ans_con[max_index]
        return None


    def matchByProACon(self, words, deal_entity):
        """
        根据实体携带的属性信息和问句原文匹配得到与答案相符的属性信息
        1. 遍历实体所有的属性信息
        2. 按字符匹配问句和属性信息
        3. 2得到空则按向量相似度得到匹配信息
        4. 2,3均空则返

        有答案二次reverse匹配
        :param words: 问句
        :param deal_entity: 实体及其信息
        :return: 答案或空
        """

        form_words = self.form_util.preProcessWords(words)

        ans_con = []
        count_rate = []

        for name, content in deal_entity.items():

            """
            抽取出的实体的属性
            """
            pro = np.array(content['p'])

            """
            去掉问题中的实体方便匹配
            """
            while (name in form_words):
                form_words = form_words.replace(name, '')

            for p in pro:

                con = self.form_util.preProcessWords(p[1])

                while (name in con):
                    con = con.replace(name, '')

                if len(con) > len(form_words):
                    c_len = len(form_words)
                    count = self.seacrchAll(con, form_words)
                else:
                    c_len = len(con)
                    count = self.seacrchAll(form_words, con)
                if c_len == 0:
                    continue
                if float(count) / float(c_len) >= 0.65:
                    ans_con.append([name, p[0], p[1]])
                    count_rate.append(count / c_len)
        if ans_con != []:
            revers_count = []

            for ans in ans_con:
                if len(form_words) >= len(ans[2]):
                    revers_count.append(self.seacrchAll(form_words, ans[2]) / len(form_words))
                else:
                    revers_count.append(self.seacrchAll(ans[2], form_words) / len(ans[2]))
            max_index = np.argmax(np.array(revers_count))
            return ans_con[max_index]
        return None


    #======================================================================

    def matchByProName(self,entity, property):
        """
        匹配抽出的属性名称和实体具有的属性名称

        :param find_pro: 抽取的属性
        :param find_rel: 抽取的关系
        :param entity_deal: 携带信息的实体
        :return:字典，形式入{实体:{属性名:属性值}}
        """
        entity_deal = self.graph_util.dealWithEnitity(entity)

        ans = {}

        for name, content in entity_deal.items():
            name_dict = {}
            pro = np.array(content['p'])


            for p in pro:
                if p[0] in property:

                    if p[0] in name_dict.keys():
                        name_dict[p[0]].append(p[1])
                    else:
                        name_dict[p[0]] = [p[1]]

            if name_dict != {}:
                ans[name]=name_dict

        if ans == {}:
            return None
        else:
            return ans

    def matchByRelName(self,entity, property):
        """
        匹配抽出的关系名称和实体具有的关系名称，返回形式如matchByProName

        :param find_pro: 抽取的属性
        :param find_rel: 抽取的关系
        :param entity_deal: 携带信息的实体
        :return:
        """
        entity_deal = self.graph_util.dealWithEnitity(entity)


        ans = {}

        for name, content in entity_deal.items():

            name_dict = {}

            rel = np.array(content['r'])
            for r in rel:
                if r[0] in property:
                    if r[0] in name_dict.keys():
                        name_dict[r[0]].append(r[1])
                    else:
                        name_dict[r[0]] = [r[1]]
            if name_dict != {}:
                ans[name]=name_dict

        if ans == {}:
            return None
        else:
            return ans

    """
    def downFindAnsByRel(self, entity,property,keyword):
        
        给定谓词和宾语，并限制了主语的类型，得到主语列表
        :param entity: 宾语
        :param property: 谓词
        :param keyword: 主语类型
        :return:
        
        ans = self.graph_util.getEntityByRel(keyword[0],property[0],entity[0])
        if ans != None:
            return ans
        return None
    """
    """
    def downFindAnsByWords(self, words, entity, property):
        
        给出实体类型，指定属性，根据该属性值与句子的匹配程度得到对应的三元组
        :param words:
        :param entity:
        :param property:
        :return:
        

        son_list = self.graph_util.getEntityByType(entity[0])
        if son_list == None:
            return None
        deal_entity = self.graph_util.dealWithEnitity(son_list)
        ans = self.matchProConWithPro(words, deal_entity, property)
        return ans
    """

    """
    def downFindAnsByEnt(self, words, entity):
        
        根据实体携带属性的信息和句子信息的匹配程度得到最匹配的实体
        :param words:
        :param entity:
        :return:
        
        deal_entity = self.graph_util.dealWithEnitity(entity)
        ans = self.matchByProACon(words, deal_entity)

        if ans != None:
            return ans
        son_list = self.graph_util.getEntityByType(entity[0])
        if son_list == None:
            return None
        deal_entity = self.graph_util.dealWithEnitity(son_list)
        ans = self.matchByProACon(words, deal_entity)
        return ans
    """

    def taskNormalPro(self, entity, property):
        ans = self.matchByProName(entity, property)
        return ans



    def taskNormalRel(self, entity, property):
        """
        根据实体和关系名称得到三元组
        :param entity:
        :param property:
        :return:
        """
        ans = self.matchByRelName(entity, property)

        return ans

    def taskTAPAO(self, words, entity, property):
        """
        给出属性和实体类型以及问句，匹配得到精度最高的实体（闽是哪个省的简称）

        :param words:
        :param entity:
        :param property:
        :return:
        """

        son_list = self.graph_util.getEntityByType(entity[0])
        if son_list == None:
            return None
        deal_entity = self.graph_util.dealWithEnitity(son_list)
        ans = self.matchProConWithPro(words, deal_entity, property)
        return ans

        #ans = self.downFindAnsByWords(words, entity, property)


    """
    delete

    def taskProMatch(self,words,entity,property):
        ans = self.downFindAnsByWords(words,entity,property)
        #print("taskSonMatch",ans)
        return ans
    """

    def taskTARAO(self, entity, property, keyword):
        """
        给出关系和宾语，得到主语，并限制主语的类型
        :param entity: 实体类型
        :param property: 关系
        :param keyword: 宾语
        :return:
        """

        ans = self.graph_util.getEntityByRelLimitType(keyword[0], property[0], entity[0])
        if ans != None:
            return ans
        return None
        #ans = self.downFindAnsByRel(entity, property, keyword)

        return ans

    def taskSTAO(self, words, entity):
        """
        给出主语和宾语，得出谓词
        给出主语类型和宾语，确定主语和谓词


        :param words: 问句（代表宾语）
        :param entity: 实体或实体类型（主语）
        :return: 三元组
        """

        deal_entity = self.graph_util.dealWithEnitity(entity)
        ans = self.matchByProACon(words, deal_entity)

        if ans != None:
            return ans
        son_list = self.graph_util.getEntityByType(entity[0])
        if son_list == None:
            return None
        deal_entity = self.graph_util.dealWithEnitity(son_list)
        ans = self.matchByProACon(words, deal_entity)
        return ans


    def taskReverse(self, words, key_words):
        """
        从属性关键词找到对应实体及三元组，然后得到与句子最匹配的三元组
        :param words:
        :param key_words:
        :return:
        """
        triple = self.graph_util.getEntByfuzzySearch(key_words[0])
        ans = self.matchFuzzySearch(words, triple)
        return ans


    #==================================================================
    def doNormal(self,words,task_type,entity,property,keywords):


        if task_type == 'task_normal_pro':


            ans = self.taskNormalPro(entity,property)

            if ans != None:
                return entity[0], "ans_items", ans

        if task_type == 'task_normal_rel':
            ans = self.taskNormalRel(entity,property)
            if ans != None:
                return entity[0], "ans_items", ans

        if task_type == 'task_son_kw_match':
            ans = self.taskTARAO(entity, property,keywords)
            if ans != None:
                return keywords[0], "ans_list", ans
            else:
                return keywords[0],None,None

        if task_type == 'task_son_match':
            ans = self.taskTAPAO(keywords,entity,property)
            if ans != None:
                return entity[0], "ans_triple", ans
        """
        已经取消了
        if task_type == 'task_pro_match':
            ans = self.graph_util.taskProMatch(keywords,entity,property)
            if ans != None:
                return entity[0], "ans_triple", ans
        """

        if task_type == 'task_singal_entity':
            ans = self.taskSTAO(words,entity)
            if ans != None:
                return entity[0], "ans_triple", ans

        if task_type == 'task_reverse' and len(entity)>0:
            ans = self.taskReverse(words,entity)
            if ans != None:
                return entity[0], "ans_triple", ans
        """
        暂时取消
        if task_type == 'task_limit_sub':

            ans = self.graph_util.taskLimitSub(keywords,entity)
            if ans != None:
                return entity[0], "ans_list", ans
        """

        if len(entity)==0 or entity == None:

            return None,None,None

        return entity[0], None, None