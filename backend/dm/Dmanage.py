# @Language: python3
# @File  : Dmanage.py
# @Author: LinXiaofei
# @Date  : 2020-05-01
"""

"""
import sys
import os
project_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
# print(project_path)
sys.path.append(project_path)

from nlu.processNLU import processNLU
from nlg.generateAns import generateAns



from graphSearch.calculateBussiness import calculateBussiness
from graphSearch.compareBussiness import compareBussiness
from graphSearch.normalBussiness import normalBussiness


from data.data_process import read_file
import requests, json

"""
问答引擎
"""

class DialogManagement(object):
    def __init__(self):
        self.nlu_util = processNLU()

        self.nlg_util = generateAns()

        self.normal_bussiness = normalBussiness()
        self.compare_bussiness = compareBussiness()
        self.calculate_bussiness = calculateBussiness()

        self.last_sentence = []
        self.wether = []

    def doNLU(self,words):

        ans_str = ""

        ask_words,ans_ent = self.nlu_util.formAsking(words)


        if ask_words is not None:
            words = ask_words
            self.wether = []
            self.wether.append(ans_ent)

        ans_dict = self.nlu_util.differentWordsType(words,self.last_sentence)



        words_type = ans_dict['words_type']

        if words_type == 'task_compare':

            entity_array = ans_dict['entity']
            property = ans_dict['property']
            task_type = ans_dict['task_type']


            compare_dict = self.normal_bussiness.taskNormalPro(entity_array, [property])

            #compare_dict = self.dealCompare(entity_array,[property])

            ans_str += self.doNLG(None, "ans_items", compare_dict,self.wether)
            if 'less' in task_type:
                ans_str += self.nlg_util.compareLessNLG(task_type, compare_dict)
            else:
                ans_str += self.nlg_util.compareMoreNLG(task_type, compare_dict)
            return ans_str,words_type


        if 'task_calculate' in words_type:

            if ans_dict['task_type'] == 'task_calculate_ask':
                self.last_sentence.append(words)
                return [ans_dict['ask']]
            if 'most' in ans_dict['task_type']:

                ans,task_type = self.calculate_bussiness.doMostCalculate(ans_dict)
                self.last_sentence = []
                ans = self.nlg_util.ansMost(ans,self.wether)
                self.wether = []

                return ans,task_type
            elif 'least' in ans_dict['task_type']:
                ans, task_type = self.calculate_bussiness.doLeastCalculate(ans_dict)
                self.last_sentence = []
                ans = self.nlg_util.ansMost(ans,self.wether)
                self.wether = []
                return ans,task_type
            elif 'dist' in ans_dict['task_type']:
                ans, task_type = self.calculate_bussiness.doDistCalculate(ans_dict)
                self.last_sentence = []
                return ans,task_type


        if words_type == 'task_normal':
            ask_words = ans_dict['ask_words']
            entity_array = ans_dict['entity_array']
            coo = ans_dict['coo']
            coo_index = ans_dict['coo_index']
            property_array = ans_dict['property_array']
            keywords_array = ans_dict['keywords_array']
            task_type_array = ans_dict['task_type_array']
            ask_ent = ans_dict['ask_ent']
            print("抽取的实体: ",entity_array[0])
            print("抽取的属性: ", property_array[0])
            key_ent, ans_type, ans = self.normal_bussiness.doNormal(ask_words, task_type_array[0], entity_array[0],
                                                                    property_array[0],
                                                                    keywords_array[0])
            if ans != None and ans != "":
                ans_str = ans_str + self.doNLG(key_ent, ans_type, ans, self.wether)
                return ans_str, task_type_array[0]
            """
            for i in range(3):
                key_ent, ans_type, ans = self.normal_bussiness.doNormal(ask_words, task_type_array[i], entity_array[i], property_array[i],
                                                      keywords_array[i])

                if ans != None and ans != "":
                    ans_str = ans_str + self.doNLG(key_ent, ans_type, ans,self.wether)
                    return ans_str, task_type_array[i]

            for i in range(3):
                if task_type_array[i] != 'task_singal_entity' and task_type_array[i] != None:
                    key_ent, ans_type, ans = self.normal_bussiness.doNormal(ask_words, "task_singal_entity", entity_array[i],
                                                          property_array[i], keywords_array[i])
                if ans != None and ans != "":
                    ans_str = ans_str + self.doNLG(key_ent, ans_type, ans, self.wether)
                    self.wether = []
                    return ans_str, "task_singal_entity"

            task_type = "task_reverse"
            key_ent, ans_type, ans = self.normal_bussiness.doNormal(ask_words, task_type, entity_array[0], property_array[0],
                                                  keywords_array[0])
            if ans != None and ans != "":
                ans_str = ans_str + self.doNLG(key_ent, ans_type, ans, self.wether)
                self.wether = []
                return ans_str, "task_reverse"
            """

            return "", None

    """
    def dealCompare(self,entity,property):

        compare_dict = self.normal_bussiness.taskNormalPro(entity,property)

        return compare_dict
    """


    def doNLG(self,entity,ans_type,ans,wether):

        ans_str = self.nlg_util.getAns(entity, ans_type, ans,wether)
        return ans_str



if __name__ == '__main__':
    a = DialogManagement()
    while(1):
        s = input("user: ")
        if s == "":
            continue
        ans = a.doNLU(s)
        if ans[0] == '':
            print("无法回答")
        else:
            print(ans[0])