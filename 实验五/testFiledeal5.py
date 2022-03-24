import logging
import random
import unittest

import exp5


class TestCore(unittest.TestCase):

    # def __init__(self):
    #
    #     super().__init__()
    #
    #     logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
    #                         format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    #     self.logger = logging.getLogger(__name__)

    def test_init(self):
        # 本次测试一并将sortCities和sortProvince测试了
        core1 = exp5.Core("./yq_in.txt")
        core2 = exp5.Core('./yq_in.txt', isSorted=False)
        # 感染人数最多的是广东省
        self.assertEqual(core1.provinces[0].name, '广东省')
        # 文件第一个默认是浙江省
        self.assertEqual(core2.provinces[0].name, '浙江省')

    def test_getAllProvinces(self):
        core = exp5.Core("./yq_in.txt")
        province_objs = core.getAllProvince()
        province_name_list = []
        province_num_list = []
        for i in province_objs:
            province_name_list.append(i.name)
            province_num_list.append(i.num)
        # 所有省份按照感染人数排序后的列表
        real_province_name_list = ['广东省', '河南省', '浙江省', '湖南省', '安徽省', '江西省', '江苏省', '陕西省']
        real_province_num_list = [1347, 1272, 1205, 1017, 989, 934, 631, 245]
        # 判断省份名字和顺序是否正确
        self.assertEqual(province_name_list, real_province_name_list)
        # 判断省份人数和顺序是否正确
        self.assertEqual(province_num_list, real_province_num_list)
        # 若这两项正确，则基本可以判定这个方法没有大问题

    def test_getProvinceByName(self):
        core = exp5.Core("./yq_in.txt")
        real_province_name_list = ['广东省', '河南省', '浙江省', '湖南省', '安徽省', '江西省', '江苏省', '陕西省']
        real_province_num_list = [1347, 1272, 1205, 1017, 989, 934, 631, 245]
        real_province_map_list = []
        for i in range(len(real_province_name_list)):
            real_province_map = {'province': real_province_name_list[i], 'num': real_province_num_list[i]}
            real_province_map_list.append(real_province_map)

        # 随机从省里面随机取五个出来，测试getProvinceByName这个方法的稳定性
        for i in range(5):
            rdm = random.randint(0, len(real_province_map_list) - 1)
            self.assertEqual(real_province_map_list[rdm]['num'],
                             core.getProvinceByName(real_province_map_list[rdm]['province']).num)

    def test_writeInTxt(self):
        core = exp5.Core("./yq_in.txt")
        # 打开事先准备好的测试文件（全部省的测试文件）
        test_all_file = open('testfile_all.txt', 'r', encoding='UTF-8')
        # 浙江省的测试文件
        test_zhejiang_file = open('testfile_zhejiang.txt', 'r', encoding='UTF-8')
        core.writeInTxt(newFilename='all_province.txt')
        output_all_province = open('all_province.txt', 'r', encoding='GBK')
        core.writeInTxt(newFilename='zhejiang_province', province='浙江省')
        output_zhejiang_province = open('zhejiang_province', 'r', encoding='GBK')
        # 测试writeInTxt的输出效果（输出全部省）
        self.assertEqual(test_zhejiang_file.read(), output_zhejiang_province.read())
        # 测试writeInTxt的输出效果（输出单个省）
        self.assertEqual(test_all_file.read(), output_all_province.read())

        test_all_file.close()
        test_zhejiang_file.close()
        output_all_province.close()
        output_zhejiang_province.close()


