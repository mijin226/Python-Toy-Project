import csv
import matplotlib.pyplot as plt
import numpy as np

# csv 파일
file_path = {
    "2020" : "2020_월별 승하차인원.csv", 
    "2021" : "2021_월별 승하차인원.csv", 
    "2022" : "2022_월별 승하차인원.csv", 
    "2023" : "2023_월별 승하차인원.csv"
    }

# 월별 리스트
# 20~21년은 월이 열로 있으므로                
# 열 4 ~ 15
row_month = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 4, 5]
# 22~23년은 월이 행으로 있으므로
month = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]

# 계절 리스트
seanson = ["spring", "summer", "fall", "winter"]

# 계절별 변수
spring = {
    "2020" : 0,
    "2021" : 0,
    "2022" : 0,
    "2023" : 0
    }
summer = {
    "2020" : 0,
    "2021" : 0,
    "2022" : 0,
    "2023" : 0
    }
fall = {
    "2020" : 0,
    "2021" : 0,
    "2022" : 0,
    "2023" : 0
    }
winter = {
    "2020" : 0,
    "2021" : 0,
    "2022" : 0,
    "2023" : 0
    }

# 파일을 읽어옴
# 20~21년과 22~23년 csv 데이터 형식이 다르므로
for year in file_path:
    # 공통 부분
    # 키 값 확인용
    print("key :", year)
    print("value :", file_path[year])
    
    with open(file_path[year], mode='r') as file:
        reader = csv.reader(file)
        print("파일 읽어옴")
    
        # 첫 줄을 읽음
        next(reader)
        print("첫 줄 읽음")
    
        for row in reader :
            # 20~21년 부분
            if(year == "2020" or year == "2021"):
                # 월이 열로 있으므로                
                
                # 중간에 빈 값들이 있어서 그것을 제외하는 if문도 추가
                # spring
                for i in row_month[0:3]:
                    if row[i] != '':
                        spring[year] += int(row[i])
                # summer
                for i in row_month[3:6]:
                    if row[i] != '':
                        summer[year] += int(row[i])
                # fall
                for i in row_month[6:9]:
                    if row[i] != '':
                        fall[year] += int(row[i])
                # winter
                for i in row_month[9:]:
                    if row[i] != '':
                        winter[year] += int(row[i])
            
            # 22~23년 부분
            if(year == "2022" or year == "2023"):
                # 월을 판단하기 쉽게 데이터 가공
                date = row[-2].strip(year+"-")
                print(date)
        
                # 만약 -2 위치의 열 값 앞이 3, 4, 5 중 하나라면
                if date.startswith(month[2]) or date.startswith(month[3]) or date.startswith(month[4]):
                    # print("spring :", row)
                    spring[year] += int(row[-1])
                    # 만약 -2 위치의 열 값 앞이 6, 7, 8 중 하나라면
                elif date.startswith(month[5]) or date.startswith(month[6]) or date.startswith(month[7]):
                    #print("summer :", row)
                    summer[year] += int(row[-1])
                    # 만약 -2 위치의 열 값 앞이 9, 10, 11 중 하나라면
                elif date.startswith(month[8]) or date.startswith(month[9]) or date.startswith(month[10]):
                    # print("fall :", row)
                    fall[year] += int(row[-1])
                    # 만약 -2 위치의 열 값 앞이 1, 2, 12 중 하나라면
                elif date.startswith(month[0]) or date.startswith(month[1]) or date.startswith(month[11]):
                    # print("winter :", row)
                    winter[year] += int(row[-1])
                
# 연도, 계절 별 결과 출력
for year in file_path:
    print(year+"년도 계절별 통행량 -----------------------")
    print("spring("+year+") 합계 :", spring[year])
    print("summer("+year+") 합계 :", summer[year])
    print("fall("+year+") 합계 :", fall[year])
    print("winter("+year+") 합계 :", winter[year])
 
    
# 그래프를 그리기 쉬운 데이터 형식으로 변경
year_chart_data = {
    "2020" : [],
    "2021" : [],
    "2022" : [],
    "2023" : []
    }

# 각 년도에 데이터를 넣는 작업
for year in year_chart_data:
    year_chart_data[year].append(spring[year])
    year_chart_data[year].append(summer[year])
    year_chart_data[year].append(fall[year])
    year_chart_data[year].append(winter[year])
    print(year+"년도 배열 :",year_chart_data[year])
    
    
# 그래프 출력
# 출력할 데이터의 가로, 세로 길이 설정
plt.figure(figsize=(12,8))

# 막대의 너비와 x축 위치
bar_width = 0.15
x = np.arange(len(seanson))

# 그래프 색
colors = ['#98FB98', '#90EE90', '#32CD32', '#006400']

# 막대 그래프는 plt.bar을 사용
plt.bar(x-bar_width, year_chart_data["2020"], width=bar_width, label="2020", color=colors[0])
plt.bar(x, year_chart_data["2021"], width=bar_width, label="2021", color=colors[1])
plt.bar(x+bar_width, year_chart_data["2022"], width=bar_width, label="2022", color=colors[2])
plt.bar(x+(2*bar_width), year_chart_data["2023"], width=bar_width, label="2023", color=colors[3])

# 범례 표시
# 왼쪽 위에 표시
plt.legend(loc='upper left')

# y축 범위 설정 (높이를 줄임)
plt.ylim(0, 1000000000)

# x값 라벨 붙임
# 위치, 붙일 라벨
plt.xticks(x + bar_width / 2, seanson)

# 타이틀
plt.title("Seasonal Subway Traffic")

# 출 라벨
plt.xlabel("season", fontsize = 10)
plt.ylabel("traffic", fontsize = 10)

