# -*- coding: gbk -*-
import logging

import pinyin
import sys
import os


# 测试文件在同级目录下，名称为testFiledeal5.py

class Area:
    def __init__(self, name, num=0):
        self.name = name
        self.num = num

    # 重载大于号和小于号，方便后面sort函数的调用，就不用自己写排序算法了(*^_^*)
    def __lt__(self, other):
        if self.num != other.num:
            return self.num < other.num
        else:
            # 使用pinyin库就不用写枚举了o(*￣▽￣*)ブ
            return pinyin.get(self.name) < pinyin.get(other.name)

    def __gt__(self, other):
        if self.num != other.num:
            return self.num > other.num
        else:
            return pinyin.get(self.name) > pinyin.get(other.name)


class City(Area):

    def __init__(self, name, num, province):
        super().__init__(name, num)
        self.province = province

    def __str__(self):
        return '城市名：' + self.name + '\t感染人数：' + str(self.num)


class Province(Area):

    def __init__(self, name, cities=None, num=0):
        super().__init__(name, num)
        self.city_Num = 0
        if cities is None:
            self.cities = []

    def addCity(self, city):
        self.num += city.num
        self.cities.append(city)

    def __str__(self):
        outs = self.name + '\t感染人数：' + str(self.num) + '\n'
        for i in self.cities:
            outs += '城市名：' + i.name + '\t感染人数：' + str(i.num) + '\n'
        return outs


class Core:
    # 调用者自行选择是否要自动排好序，如果传入isSorted=False表示不需要自动排序，可以再调用sortCities和sortProvince来完成排序
    def __init__(self, readFilename, isSorted=True):
        self.provinces = []
        cities = []
        f = open(readFilename, 'r')
        line = f.readline()
        while line:
            line = line.split('\t')
            province = line[0]
            city = line[1]
            num = line[2]
            cities.append(City(name=city, num=int(num), province=province))
            line = f.readline()
        f.close()

        # 定义一个列表来存储省份对象
        self.provinces = []
        # 这里用列表的原因是对象是在循环里面创建的，使用容器（此处为列表）能保证数据不丢失
        province_temps = [Province(name=None, num=0)]
        for i in cities:
            if i.province == province_temps[0].name:
                province_temps[0].cities.append(i)
                province_temps[0].num += i.num
                province_temps[0].city_Num += 1
            else:
                if province_temps[0].name is not None:
                    self.provinces.append(province_temps[0])
                province_temps[0] = Province(name=i.province, num=i.num)
                province_temps[0].cities.append(i)

        if isSorted:
            self.sortCities()
            self.sortProvince()

    # 对省份实现排序
    def sortProvince(self):
        self.provinces.sort(reverse=True)

    # 对各个市实现排序
    def sortCities(self):
        for i in self.provinces:
            i.cities.sort(reverse=True)

    # 获取所有省的对象，以一个列表的形式返回
    def getAllProvince(self):
        return self.provinces

    # 通过省份名来获取该省的全部信息
    def getProvinceByName(self, name):
        for i in self.provinces:
            if i.name == name:
                return i
        return None

    # 将统计好的信息写入文件，调用者可以选择输出的文件名，该名称默认是output.txt
    # 调用者也可以选择是输出单个省的信息还是输出所有省的信息，默认输出所有省的信息由province参数决定
    def writeInTxt(self, newFilename="output.txt", province=None):
        if os.path.exists(newFilename):
            os.remove(newFilename)
        f = open(newFilename, 'a')

        if province is not None:
            for i in self.provinces:
                if i.name == province:
                    f.write(i.name + '\t' + str(i.num) + '\n')
                    for j in i.cities:
                        f.write(j.name + '\t' + str(j.num) + '\n')
        else:
            for i in self.provinces:
                f.write(i.name + '\t' + str(i.num) + '\n')
                for j in i.cities:
                    f.write(j.name + '\t' + str(j.num) + '\n')
                f.write('\n')
        f.close()


if __name__ == '__main__':
    args = sys.argv
    argsLen = len(args)
    logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logger.warning("请勿直接运行本文件，请运行测试文件（testFiledeal5.py）")
