import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from PIL import Image
import time

#Load Model
filename = 'finalized_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))


#Initial Variables
#Static Variables Selection
#These Variables get the values of frequency depend like (Không bao giờ, Đôi khi, Thường Xuyên, Luôn Luôn)
Age = 0
#Frequency of consumption of vegetables (1-3)
FCVC = 1
#Height
Height = 1.73
#Weight
Weight = 103
#Number of main meals (1-4)
NCP = 1
#Consumption of water daily (1-3)
CH2O = 1
#Physical activity frequency (0-3)
FAF = 0
#Time using technology devices (0-2)
TUE = 0
#Gender Female (0-1)
Gender_Female = 0
#Gender Male (0-1)
Gender_Male = 0
#History overweight no (0-1)
family_history_with_overweight_no = 0
#History overweight yes (0-1)
family_history_with_overweight_yes = 0
#Frequent consumption of high caloric food no (0-1)
FAVC_no = 0
#Frequent consumption of high caloric food yes (0-1)
FAVC_yes = 0
#Consumption of food between meals (0-1) Ăn vặt giữa các bữa ăn
CAEC_Always = 0
#Consumption of food between meals (0-1) Ăn vặt giữa các bữa ăn
CAEC_Frequently = 0
#Consumption of food between meals (0-1) Ăn vặt giữa các bữa ăn
CAEC_Sometimes = 0
#Consumption of food between meals (0-1) Ăn vặt giữa các bữa ăn
CAEC_no = 0
#Smoke no (0-1)
SMOKE_no = 0
#Smoke yes (0-1)
SMOKE_yes = 0
#Calories consumption monitoring no (0-1) Thường xuyên theo dõi lượng calo tiêu thụ
SCC_no = 0
#Calories consumption monitoring yes (0-1) Thường xuyên theo dõi lượng calo tiêu thụ
SCC_yes = 0
#Consumption of alcohol (0-1)
CALC_Always = 0
#Consumption of alcohol (0-1)
CALC_Frequently = 0
#Consumption of alcohol (0-1)
CALC_Sometimes = 0
#Consumption of alcohol (0-1)
CALC_no = 0
#Transportation used (0-1)
MTRANS_Automobile = 0
#Transportation used (0-1)
MTRANS_Bike = 0
#Transportation used (0-1)
MTRANS_Motorbike = 0
#Transportation used (0-1)
MTRANS_Public_Transportation = 0
#Transportation used (0-1)
MTRANS_Walking = 0
#Activity Level
Activity_Level = ['SEDENTARY', 'LIGHTLY ACTIVE', 'MODERATE ACTIVE', 'HARD ACTIVE', 'EXTREME ACTIVE']
#Are you Vegan? (0-1)
type = 'anything'




#----------------------GUI for input variables----------------------
print("----------------------MEALS PREPARATION FOR SPECIFIC TYPE OF BODY----------------------")
print("\nPLEASE ENTER THESE FOLLOWING QUESTIONS ABOUT YOUR DAILY ROUTINE")
print("----------------------")
#Gender
while True:
  Gender = input("What is your gender? (0:Male, 1:Female): ")
  if Gender == '0':
      Gender_Male = 1
      Gender_Female = 0
      break
  elif Gender == '1':
      Gender_Male = 0
      Gender_Female = 1
      break
  else:
      print("Please enter valid option")

#Age
while True:
  try:
    Age = int(input("How old are you: "))
    break
  except ValueError:
    print("Please enter only digit number")

#Height
while True:
  try:
    Height = float(input("What is your height (in meter): "))
    if Height > 0:
        break
    else:
        print("Please enter valid number of heights")
  except ValueError:
    print("Please enter only digit number")

#Weight
while True:
  try:
    Weight = float(input("What is your weight (in kilogram): "))
    if Weight > 0:
        break
    else:
        print("Please enter valid number of weights")
  except ValueError:
    print("Please enter only digit number")


#History of obesity
while True:
  opt = input("Do your family have history of obesity?(y/n): ")
  if opt == 'y' or opt == 'Y':
    family_history_with_overweight_no = 0
    family_history_with_overweight_yes = 1
    break
  elif opt == 'n' or opt == 'N':
    family_history_with_overweight_no = 1
    family_history_with_overweight_yes = 0
    break
  else:
    print("Please enter valid option")

#High caloric consumption
while True:
  opt = input("Do you often consume high caloric food (about 3-4 days a week)?(y/n): ")
  if opt == 'y' or opt == 'Y':
    FAVC_no = 0
    FAVC_yes = 1
    break
  if opt == 'n' or opt == 'N':
    FAVC_no = 1
    FAVC_yes = 0
    break
  else:
    print("Please enter valid option")

#Monitoring caloric consumption
while True:
  opt = input("Do you often monitor your caloric consumption?(y/n): ")
  if opt == 'y' or opt == 'Y':
    SCC_no = 0
    SCC_yes = 1
    break
  if opt == 'n' or opt == 'N':
    SCC_no = 1
    SCC_yes = 0
    break
  else:
    print("Please enter valid option")

#Smoking
while True:
  opt = input("Do you smoke?(y/n): ")
  if opt == 'y' or opt == 'Y':
    SMOKE_no = 0
    SMOKE_yes = 1
    break
  if opt == 'n' or opt == 'N':
    SMOKE_no = 1
    SMOKE_yes = 0
    break
  else:
    print("Please enter valid option")

#Frequent of using device
while True:
  opt = input("Time of using technology device a day?(0:Never, 1:1-2 hours, 2:over 3 hours): ")
  if opt == '0' or opt == '1' or opt == '2':
    TUE = int(opt)
    break
  else:
    print("Please enter valid option")

#Amount of meals
while True:
  opt = input("How many meals do you have a day?(1->4): ")
  if opt == '1' or opt == '2' or opt == '3' or opt == '4':
    NCP = int(opt)
    break
  else:
    print("Please enter valid option")

#Food consumption between meals
CAEC_Always = 0
CAEC_Frequently = 0
CAEC_Sometimes = 0
CAEC_no = 0
while True:
  opt = input("How often do you consume food between meals?(0:Never, 1:Sometimes, 2:Frequently, 3:Always): ")
  if opt == '0':
    CAEC_no = 1
    break
  if opt == '1':
    CAEC_Sometimes = 1
    break
  if opt == '2':
    CAEC_Frequently = 1
    break
  if opt == '3':
    CAEC_Always = 1
    break
  else:
    print("Please enter valid option")

#Water daily consumption
while True:
  opt = input("How many litters of water do you consume a day?(1:under 1.5l, 2:1.5-2l, 3:over 2l): ")
  if opt == '1' or opt == '2' or opt == '3':
    CH2O = int(opt)
    break
  else:
    print("Please enter valid option")

#Vegetable consumption
while True:
  opt = input("How often do you consume vegetable?(1:Rarely, 2:Sometimes, 3:Usually): ")
  if opt == '1' or opt == '2' or opt == '3':
    FCVC = int(opt)
    break
  else:
    print("Please enter valid option")

#Alcohol consumption
CALC_Always = 0
CALC_Frequently = 0
CALC_Sometimes = 0
CALC_no = 0
while True:
  opt = input("How often do you use alcohol?(0:Never, 1:Sometimes, 2:Frequently, 3:Always): ")
  if opt == '0':
    CALC_no = 1
    break
  if opt == '1':
    CALC_Sometimes = 1
    break
  if opt == '2':
    CALC_Frequently = 1
    break
  if opt == '3':
    CALC_Always = 1
    break
  else:
    print("Please enter valid option")

#Exercise frequency
while True:
  opt = input("How often do you exercise a week?(0:Never, 1:1-2 days, 2:3-4 days, 3:everyday): ")
  if opt == '0' or opt == '1' or opt == '2' or opt == '3':
    FAF = int(opt)
    break
  else:
    print("Please enter valid option")

#Transportation using
MTRANS_Automobile = 0
MTRANS_Bike = 0
MTRANS_Motorbike = 0
MTRANS_Public_Transportation = 0
MTRANS_Walking = 0
while True:
  opt = input("What kind of transportation do you use the most?(0:Walking, 1:Public Transportation, 2:Motorbike, 3:Bike, 4:Automobile): ")
  if opt == '0':
    MTRANS_Walking = 1
    break
  if opt == '1':
    MTRANS_Public_Transportation = 1
    break
  if opt == '2':
    MTRANS_Motorbike = 1
    break
  if opt == '3':
    MTRANS_Bike = 1
    break
  if opt == '4':
    MTRANS_Automobile = 1
    break
  else:
    print("Please enter valid option")

#Job level Description
print("Job Level Description")
print("0: Sedentary (student, teacher, desk job,...)")
print("1: Lightly Active (housewife, cook,...)")
print("2: Moderate Active (construction worker or physically demanding job)")
print("3: Hard Active (agricultural worker or physically demanding job with 5-7 times of intense exercise a week)")
print("4: Extreme Active (professional athlete, competitive cyclist, fitness professional or engage in intense exercise for at least 2 hours per day)")
Activity_Level = ['SEDENTARY', 'LIGHTLY ACTIVE', 'MODERATE ACTIVE', 'HARD ACTIVE', 'EXTREME ACTIVE']
while True:
  opt = input("Choose: ")
  if opt == '0' or opt == '1' or opt == '2' or opt == '3' or opt == '4':
    Activity = Activity_Level[int(opt)]
    break
  else:
    print("Please enter valid option")

#Vegan?
while True:
  opt = input("Are you vegan?(y/n): ")
  if opt == 'y' or opt == 'Y':
    type = 'vegan'
    break
  if opt == 'n' or opt == 'N':
    type = 'anything'
    break
  else:
    print("Please enter valid option")


#Predict
#results = loaded_model.predict([[21,2,3,2,0,1,0,1,1,0,1,0,1,0,0,1,1,0,1,0,0,0,0,1,1,0,0,0,0]]) #Sample

results = loaded_model.predict([[Age, FCVC, NCP, CH2O, FAF, TUE, Gender_Female, Gender_Male, family_history_with_overweight_no,
family_history_with_overweight_yes, FAVC_no, FAVC_yes, CAEC_Always, CAEC_Frequently, CAEC_Sometimes, CAEC_no,
  SMOKE_no, SMOKE_yes, SCC_no, SCC_yes, CALC_Always, CALC_Frequently, CALC_Sometimes, CALC_no, MTRANS_Automobile,
  MTRANS_Bike, MTRANS_Motorbike, MTRANS_Public_Transportation, MTRANS_Walking]])


print("\n----------------------\nRESULT\n----------------------\n")
result = results[0].split('_')[0]
print("Physical Condition: " + result)

#II. BMR to TDEE Calculate
#1. BMR by Mifflin-St Jeor Equation
def BMR_Calculator(Gender_Male, Height, Weight, Age, Activity):
  BMR = 0
  if Gender_Male == 1:
    print("Gender: Male")
    BMR = (10 * Weight) + (6.25 * Height * 100) - (5 * Age) + 5
  else:
    print("Gender: Female")
    BMR = (10 * Weight) + (6.25 * Height * 100) - (5 * Age) - 161
  return BMR

#2. TDEE Calculator
def TDEE_Calculator(Gender_Male, Height, Weight, Age, Activity, result):
  #TDEE
  TDEE = BMR_Calculator(Gender_Male, Height, Weight, Age, Activity)
  print('BMR: ' + str(TDEE))
  if Activity == 'SEDENTARY':
    TDEE *= 1.2
  elif Activity == 'LIGHTLY ACTIVE':
    TDEE *= 1.375
  elif Activity == 'MODERATE ACTIVE':
    TDEE *= 1.55
  elif Activity == 'HARD ACTIVE':
    TDEE *= 1.725
  elif Activity == 'EXTREME ACTIVE':
    TDEE *= 1.9

  #TDEE by physical condition
  #500-1000 is safety deficit calories for cutting or bulking with 0.5 kg difference per week
  if result == 'Insufficient':
    TDEE += 500
  elif result == 'Overweight':
    TDEE -= 500
  elif result == 'Obesity':
    TDEE -= 600
  print("TDEE: " + str(TDEE))

  return TDEE


TDEE = round(TDEE_Calculator(Gender_Male, Height, Weight, Age, "SEDENTARY", result))
#Token
tk = "https://www.eatthismuch.com/?generate=2&diet_type=" + type + "&cals=" + str(TDEE)





class Scraping:
  def __init__(self):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    self.options = webdriver.ChromeOptions()
    self.options.headless = True
    self.options.add_argument(f'user-agent={user_agent}')
    self.options.add_argument("--window-size=1920,1080")
    self.options.add_argument('--ignore-certificate-errors')
    self.options.add_argument('--allow-running-insecure-content')
    self.options.add_argument("--disable-extensions")
    self.options.add_argument("--proxy-server='direct://'")
    self.options.add_argument("--proxy-bypass-list=*")
    self.options.add_argument("--start-maximized")
    self.options.add_argument('--disable-gpu')
    self.options.add_argument('--disable-dev-shm-usage')
    self.options.add_argument('--no-sandbox')
    self.driver = webdriver.Chrome(executable_path="chromedriver.exe", options=self.options)
    self.driver.get(tk)
    time.sleep(2)
    total_height = self.driver.execute_script("return document.body.parentNode.scrollHeight") + 1000
    time.sleep(2)
    self.driver.set_window_size(1920, total_height)
    time.sleep(5)
    ls = self.driver.find_elements_by_class_name("food_units_selector")
    time.sleep(2)
    for lnk in ls:
      select = Select(lnk)
      select.select_by_value("0")
    time.sleep(2)

    image = self.driver.find_element(By.CLASS_NAME, "single_day_view")
    screenshot_as_bytes = image.screenshot_as_png
    with open('result/meals.png', 'wb') as f:
      f.write(screenshot_as_bytes)

    time.sleep(2)

    #Get nutrition details of meals
    self.driver.find_element_by_class_name("view_nutrition").click()
    time.sleep(2)
    image = self.driver.find_element(By.CLASS_NAME, "popover-body")
    screenshot_as_bytes = image.screenshot_as_png
    with open('result/nutrition_details.png', 'wb') as f:
      f.write(screenshot_as_bytes)


while True:
  Scraping()

  #Show meals image
  #meals = Image.open('result/meals.png')
  #meals.show()

  #Show nutrition details image
  #detail = Image.open('result/nutrition_details.png')
  #detail.show()

  opt = input("Do you want to regenerate the menu?(y/n): ")
  if opt == 'y' or opt == 'Y':
    continue
  elif opt == 'n' or opt == 'N':
    print("Terminated")
    break
  else:
    print("Please enter the valid option")



