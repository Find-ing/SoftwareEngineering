# -*- coding: gbk -*-
import logging

import pinyin
import sys
import os


# �����ļ���ͬ��Ŀ¼�£�����ΪtestFiledeal5.py

class Area:
    def __init__(self, name, num=0):
        self.name = name
        self.num = num

    # ���ش��ںź�С�ںţ��������sort�����ĵ��ã��Ͳ����Լ�д�����㷨��(*^_^*)
    def __lt__(self, other):
        if self.num != other.num:
            return self.num < other.num
        else:
            # ʹ��pinyin��Ͳ���дö����o(*������*)��
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
        return '��������' + self.name + '\t��Ⱦ������' + str(self.num)


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
        outs = self.name + '\t��Ⱦ������' + str(self.num) + '\n'
        for i in self.cities:
            outs += '��������' + i.name + '\t��Ⱦ������' + str(i.num) + '\n'
        return outs


class Core:
    # ����������ѡ���Ƿ�Ҫ�Զ��ź����������isSorted=False��ʾ����Ҫ�Զ����򣬿����ٵ���sortCities��sortProvince���������
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

        # ����һ���б����洢ʡ�ݶ���
        self.provinces = []
        # �������б��ԭ���Ƕ�������ѭ�����洴���ģ�ʹ���������˴�Ϊ�б��ܱ�֤���ݲ���ʧ
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

    # ��ʡ��ʵ������
    def sortProvince(self):
        self.provinces.sort(reverse=True)

    # �Ը�����ʵ������
    def sortCities(self):
        for i in self.provinces:
            i.cities.sort(reverse=True)

    # ��ȡ����ʡ�Ķ�����һ���б����ʽ����
    def getAllProvince(self):
        return self.provinces

    # ͨ��ʡ��������ȡ��ʡ��ȫ����Ϣ
    def getProvinceByName(self, name):
        for i in self.provinces:
            if i.name == name:
                return i
        return None

    # ��ͳ�ƺõ���Ϣд���ļ��������߿���ѡ��������ļ�����������Ĭ����output.txt
    # ������Ҳ����ѡ�����������ʡ����Ϣ�����������ʡ����Ϣ��Ĭ���������ʡ����Ϣ��province��������
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
    logger.warning("����ֱ�����б��ļ��������в����ļ���testFiledeal5.py��")
