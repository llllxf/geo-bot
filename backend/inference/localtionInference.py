# @Language: python3
# @File  : localtionInference.py
# @Author: LinXiaofei
# @Date  : 2020-06-17
"""
位置推理模块
"""
import sys
import os
project_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(project_path)

from data.data_process import read_file
from nlu.formWords import formWords
from graphSearch.graphSearch import graphSearch

class localtionInfernce(object):
    def __init__(self):
        self.search_util = graphSearch()

    def getLocation(self,entity):
        f = open("lake.txt","a")
        city_list = []
        province_list = []
        country_list = []
        state_list = []
        area_list = []
        city_list += self.search_util.getObjectBySAPLimitType(entity,'位于','城市')
        province_list += self.search_util.getObjectBySAPLimitType(entity,'位于','省')
        country_list += self.search_util.getObjectBySAPLimitType(entity,'位于','国家')
        state_list += self.search_util.getObjectBySAPLimitType(entity,'位于','洲')
        area_list += self.search_util.getObjectBySAPLimitType(entity,'位于','区域')
        if len(city_list)>0:
            for city in city_list:
                province_list += self.search_util.getObjectBySAPLimitType(city, '位于', '省')
                country_list += self.search_util.getObjectBySAPLimitType(city, '位于', '国家')
                state_list += self.search_util.getObjectBySAPLimitType(city, '位于', '洲')
                area_list += self.search_util.getObjectBySAPLimitType(city, '位于', '区域')

        if len(province_list) > 0:
            for province in province_list:
                country_list += self.search_util.getObjectBySAPLimitType(province, '位于', '国家')
                area_list += self.search_util.getObjectBySAPLimitType(province, '位于', '区域')

        if len(country_list)>0:
            for country in country_list:
                state_list += self.search_util.getObjectBySAPLimitType(country, '位于', '洲')
                area_list += self.search_util.getObjectBySAPLimitType(country, '位于', '区域')

        if len(area_list)>0:
            for area in area_list:
                state_list += self.search_util.getObjectBySAPLimitType(area, '位于', '洲')
                country_list += self.search_util.getObjectBySAPLimitType(area, '位于', '国家')

        city_list = list(set(city_list))
        province_list = list(set(province_list))
        country_list = list(set(country_list))
        area_list = list(set(area_list))
        state_list = list(set(state_list))

        location = city_list+province_list+country_list+area_list+state_list


        """
        print("================="+entity+"=================")
        print("所在城市: "+",".join(city_list))
        print("所在省: " + ",".join(province_list))
        print("所在国家: "+",".join(country_list))
        print("所在地区: "+",".join(area_list))
        print("所在洲: "+",".join(state_list))
        """
        """
        if len(country_list)<1 or len(state_list)<1:
            f.writelines(entity+"\n")
            f.writelines("所在城市: "+",".join(city_list))
            f.writelines("\n")
            f.writelines("所在省: " + ",".join(province_list))
            f.writelines("\n")
            f.writelines("所在地区: "+",".join(area_list))
            f.writelines("\n")
            f.writelines("所在洲: "+",".join(state_list))
            f.writelines("\n")
            f.writelines("======================================")
        """
        return location

    def getLocationByLimit(self,entityType,location):
        formed_ent = []


        son_list = self.search_util.getEntityByType(entityType)

        for son in son_list:
            son_location = self.getLocation(son)
            if location in son_location:
                formed_ent.append(son)
        return formed_ent



if __name__ == '__main__':
    l = localtionInfernce()
    river = read_file(project_path+"/data/compare/river.csv")
    ans = l.getLocationByLimit('湖泊', '美国')
    print(ans)
    """
    while(1):
        r = input()
        ans = l.getLocationByLimit('湖泊','美国')
        print(ans)
    """










