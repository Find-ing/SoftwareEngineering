
import pinyin
import sys
import os


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


class Province(Area):

    def __init__(self, name, cities=None, num=0):
        super().__init__(name, num)
        if cities is None:
            self.cities = []

    def addCity(self, city):
        self.num += city.num
        self.cities.append(city)


class City(Area):

    def __init__(self, name, num, province):
        super().__init__(name, num)
        self.province = province

    def __str__(self):
        return '城市名：' + self.name + '\t感染人数：' + str(self.num)


def main():
    cities = []
    filename = "./yq_in.txt"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    # filename = sys.argv[1]
    f = open(filename, 'r', encoding='gbk')
    line = f.readline()
    while line:
        oneline = line.split('\t')
        province = oneline[0]
        city = oneline[1]
        num = oneline[2]
        cities.append(City(name=city, num=int(num), province=province))
        line = f.readline()
    f.close()

    # 定义一个列表来存储省份对象
    provinces = []
    # 这里用列表的原因是对象是在循环里面创建的，使用容器（此处为列表）能保证数据不丢失
    province_temps = [Province(name=None, num=0)]
    for i in cities:
        if i.province == province_temps[0].name:
            province_temps[0].cities.append(i)
            province_temps[0].num += i.num
        else:
            if province_temps[0].name is not None:
                provinces.append(province_temps[0])
            province_temps[0] = Province(name=i.province, num=i.num)
            province_temps[0].cities.append(i)

    provinces.sort(reverse=True)

    for i in provinces:
        # print(i.name + "\t 感染人数合计: " + str(i.num))
        i.cities.sort(reverse=True)
        # for j in i.cities:
        #     print('\t', j)

    # 以上，所有所需数据都已结构化存储完毕，并排好序，接下来是输出到文件中

    # 统计命令行参数个数
    num_argv = len(sys.argv)

    if num_argv <= 2:
        new_filename = filename.replace("in", "out")
    else:
        new_filename = sys.argv[2]
    # 如果有同名文件就删除
    if os.path.exists(new_filename):
        os.remove(new_filename)
    f = open(new_filename, 'a', encoding='gbk')

    for i in provinces:
        if num_argv > 3:
            if i.name != sys.argv[3]:
                continue
        f.write(i.name + '\t' + str(i.num) + '\n')
        for j in i.cities:
            f.write(j.name + '\t' + str(j.num) + '\n')
        f.write('\n')


if __name__ == '__main__':
    main()