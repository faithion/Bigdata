import re
class Job:
    __job_name = ""  # 职位名称
    __company_name = ""  # 公司名称

    __create_time = ""  # 发布时间
    __salary_fr = ""  # 薪资范围
    __high_salary = 0  # 最高薪资
    __low_salary = 0  # 最低薪资
    __experience = ""  # 工作经验
    __diploma = ""  # 学历

    __position = ""  # 工作地点
    __city = ""  # 城市

    def __init__(self, job_name, company_name, create_time, salary_fr, experience, diploma, position):
        self.__job_name = job_name
        self.__company_name = company_name
        self.__salary_fr = salary_fr
        self.__create_time = create_time
        self.__experience = experience
        self.__diploma = diploma
        self.__position = position


    def process(self):
        position=self.get_position()
        pattern=re.compile(r".*-")#拉钩和猎职点和杠
        citys=re.findall(pattern,position)
        if bool(citys):
            self.__city=citys[0].replace("-","")#拉钩和猎职点和杠
        else:
            self.__city=position
        salary=self.get_salary_fr()
        pattern=re.compile(r"\d+")
        salarys=re.findall(pattern,salary)
        if bool(salarys):
            #self.__low_salary=int(salarys[0])
            self.__low_salary=int(int(salarys[0])*10/12)
            #self.__high_salary=int(salarys[1])
            self.__high_salary=int(int(salarys[1])*10/12)
        else:
            pass


    def set_job_name(self, job_name):
        self.__job_name = job_name

    def set_company_name(self, company_name):
        self.__company_name = company_name

    def set_create_time(self, create_time):
        self.__create_time = create_time

    def set_salary_fr(self, salary_fr):
        self.__salary_fr = salary_fr

    def set_experience(self, experience):
        self.__experience = experience

    def set_diploma(self, diploma):
        self.__diploma = diploma

    def set_position(self, position):
        self.__position = position

    def get_job_name(self):
        return self.__job_name

    def get_company_name(self):
        return self.__company_name

    def get_create_time(self):
        return self.__create_time

    def get_salary_fr(self):
        return self.__salary_fr

    def get_high_salary(self):
        return self.__high_salary

    def get_low_salary(self):
        return self.__low_salary

    def get_experience(self):
        return self.__experience

    def get_diploma(self):
        return self.__diploma

    def get_position(self):
        return self.__position

    def get_city(self):
        return self.__city


class Company:
    name = ""  # 公司名称
    type = ""  # 行业领域
    process = ""  # 融资阶段
    number = ""  # 公司规模
    address = ""  # 公司地址

    def __init__(self, name, type, process, number, address):
        self.name = name
        self.type = type
        self.process = process
        self.number = number
        self.address = address
