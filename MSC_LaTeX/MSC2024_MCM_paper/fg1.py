import  random
import  matplotlib.pyplot  as  plt
from  math  import  sin

class  Lamprey:
    def  __init__(self,  population,  resource):
        self.population  =  population
        self.resource  =  resource
        self.parasite_population  =  0

    def  increase_population(self,  amount):
        self.population  +=  amount

    def  decrease_population(self,  amount):
        self.population  -=  amount

    def  consume_resource(self,  amount):
        self.resource  -=  amount

    def  get_parasitized(self,  parasite_population_increase):
        impact  =  min(parasite_population_increase,  self.population)
        self.population  -=  impact
        self.parasite_population  +=  parasite_population_increase  -  impact

class  Parasite:
    def  __init__(self,  population):
        self.population  =  population

    def  increase_population(self,  amount):
        self.population  +=  amount

    def  decrease_population(self,  amount):
        self.population  -=  amount

class  Resource:
    def  __init__(self,  amount):
        self.amount  =  amount

    def  update_amount(self):
        elastic_factor  =  0.1
        self.amount  =  max(0,  self.amount  -  elastic_factor  *  self.amount)

    def  get_available_amount(self):
        self.update_amount()
        return  self.amount

class  Prey:
    def  __init__(self,  population):
        self.population  =  population

    def  increase_population(self,  amount):
        self.population  +=  amount

    def  decrease_population(self,  amount):
        self.population  =  max(0,  self.population  -  amount)

class  Disaster:
    def  __init__(self,  year):
        self.year  =  year

class  EnvironmentalFactor:
    def  __init__(self,  value):
        self.value  =  value

#  初始化生态系统的各个组成部分
lamprey  =  Lamprey(1000,  10000)
parasite  =  Parasite(100)
resource  =  Resource(10000)
prey  =  Prey(5000)
disaster  =  Disaster(5)   #  添加了一个  Disaster  类
environmental_factor  =  EnvironmentalFactor(0.1)   #  添加了一个  EnvironmentalFactor  类

#  设置模拟的时间跨度
years  =  100

#  初始化用于绘图的数据列表
lamprey_population_change  =  [lamprey.population]
parasite_population_change  =  [parasite.population]
available_resource_change  =  [resource.get_available_amount()]
prey_population_change  =  [prey.population]
stability_index  =  []

#  模拟多个年份的生态系统变化
for  year  in  range(years):
    available_resource  =  resource.get_available_amount()
    lamprey.consume_resource(available_resource)

    resource_increase  =  random.randint(100,  500)
    resource.amount  +=  resource_increase

    prey_increase  =  random.randint(100,  500)
    prey.decrease_population(prey_increase)
    lamprey.increase_population(prey_increase  //  10)

    parasite_increase  =  random.randint(10,  50)
    parasite.increase_population(parasite_increase)

    lamprey.get_parasitized(parasite_increase)

    lamprey_population_change.append(lamprey.population)
    parasite_population_change.append(parasite.population)
    available_resource_change.append(available_resource)
    prey_population_change.append((prey.population  +  100  *  sin(year)))
    #prey_population_change.append(prey.population)
