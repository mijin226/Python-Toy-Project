import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, ScalarFormatter

# csv 파일
# 지하철 통행량 파일
subway_file_path = {
    "01" : "CARD_SUBWAY_MONTH_202401.csv", 
    "04" : "CARD_SUBWAY_MONTH_202404.csv", 
    "08" : "CARD_SUBWAY_MONTH_202408.csv", 
    "10" : "CARD_SUBWAY_MONTH_202410.csv"
    }

# 2024년 기온 파일
weather_file_path = "weather_day_2024.csv"

# 년도
year = "2024"

# 일 배열
# 컴프리헨션을 사용하여 생성
# 01, 02 방식으로 작성하기 위해 zfill 사용
day_31 = [str(i).zfill(2) for i in range(1, 32)]
day_30 = [str(i).zfill(2) for i in range(1, 31)]

# 딕셔너리
# 통행량 데이터
# 딕셔너리 컴프리헨션를 사용해 생성
# 특정 위치의 값을 넣어주기 위해 미리 을 넣어줌
day_person = {
    "01" : [0 for i in range(1, 32)], 
    "04" : [0 for i in range(1, 31)], 
    "08" : [0 for i in range(1, 32)], 
    "10" : [0 for i in range(1, 32)]
    }

# 기온 데이터
weather = {
    "01" : [], 
    "04" : [], 
    "08" : [], 
    "10" : []
    }


# 파일을 읽어옴
# 월별로
# 통행량 데이터 가공 및 리스트 형태로 딕셔너리에 넣음
for month in subway_file_path:
    # 공통 부분
    # 키 값 확인용
    print("key :", month)
    print("value :", subway_file_path[month])
    
    with open(subway_file_path[month], mode='r', encoding="utf-8") as file:
        reader = csv.reader(file)
        print("파일 읽어옴")
    
        # 첫 줄을 읽음
        next(reader)
        print("첫 줄 읽음")
    
        for row in reader :   
            # 월을 판단하기 쉽게 데이터 가공
            #print(year+month)
            date = row[0].replace(year + month, "")
            #print(date)
            
            # 해당 일별 승차 승객 수 취합
            day_person[month][int(date)-1] += int(row[3])
            
print("---------------------------------------------------------")
print("day_person : ")
print(day_person)
print("통행량 01 길이 :", len(day_person["01"]))
print("통행량 04 길이 :", len(day_person["04"]))
print("통행량 08 길이 :", len(day_person["08"]))
print("통행량 10 길이 :", len(day_person["10"]))
print("---------------------------------------------------------")

# 기온 데이터 가공 및 리스트 형태로 딕셔너리에 넣음
with open(weather_file_path, mode='r') as file:
    reader = csv.reader(file)
    print("파일 읽어옴")

    # 첫 줄을 읽음
    next(reader)
    print("첫 줄 읽음")
    
    for row in reader : 
        # 기온 데이터의 날짜는 "2024-01-01" 방식으로 되어있음
        # 인덱스 : 2
        # 사용할 월은 weather 딕셔너리에 있는 월만 사용                
        # 앞쪽의 년도 데이터 + "-" 삭제        
        date = row[2].replace(year+"-", "")
       # print(date)
        
        for month in weather:
            # 만약 앞 쪽의 데이터가 month와 같다면
            #print("weather_month :", month)
            if date.startswith(month):
                # 해당 키의 리스트에 값을 넣음
                # 평균 기온 인덱스 : 3
                # 실수형으로 변환
                weather[month].append(float(row[3]))

print("---------------------------------------------------------")
print("weather : ")
print(weather)
print("계절 01 길이 :", len(weather["01"]))
print("계절 04 길이 :", len(weather["04"]))
print("계절 08 길이 :", len(weather["08"]))
print("계절 10 길이 :", len(weather["10"]))
print("---------------------------------------------------------")


# 그래프 출력

# title, 데이터 변경을 위한 리스트
title = {"01" : "January", "04" : "Aprill", "08" : "August", "10" : "October"}

# y축 범위 설정 (필요에 맞게 값 수정)
y_axis_left_min = -15   # 왼쪽 y축 최소값
y_axis_left_max = 40    # 왼쪽 y축 최대값
y_axis_right_min = 3000000    # 오른쪽 y축 최소값
y_axis_right_max = 9000000  # 오른쪽 y축 최대값

for month in title:
    # 하나 이상의 그래프 출력
    # fig : 전체 그래프 영역, ax : 데이터 출력 영역
    fig, ax1 = plt.subplots(figsize=(12, 8))

    print("month :", month)

    # day 크기 변경
    if month == "01" or month == "08" or month == "10":
        day = day_31
    else:
        day = day_30

    print("day :", day)

    # 왼쪽 y축에 대한 꺾은선 그래프 (Line plot)
    print("weather["+month+"] :", weather[month])
    ax1.plot(day, weather[month], color='#228B22', label=title[month]+" Weather", marker='o')

    # 왼쪽 y축 레이블 설정
    ax1.set_xlabel("Day")
    ax1.set_ylabel(title[month]+" Weather", color='#228B22')
    
    # 왼쪽 y축 범위 고정
    ax1.set_ylim(y_axis_left_min, y_axis_left_max)

    # 오른쪽 y축을 추가하여 막대 그래프를 그리기 위해 twin
    ax2 = ax1.twinx()

    # 오른쪽 y축에 대한 막대 그래프 (Bar plot)
    print("day_person["+month+"] :", day_person[month])
    ax2.bar(day, day_person[month], color='#FFD700', alpha=0.3, label=title[month]+" Subway Traffic")

    # 오른쪽 y축 레이블 설정
    ax2.set_ylabel("Subway Traffic", color='#FFD700')
    
    # 오른쪽 y축 범위 고정
    ax2.set_ylim(y_axis_right_min, y_axis_right_max)
    
    # y축 레이블 숫자 형식 설정
    ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
    # 지수 표기법을 방지하고, 0을 온전히 표시
    ax2.yaxis.set_major_formatter(ScalarFormatter())

    # 타이틀 추가
    plt.title(title[month]+" Subway Traffic in 2024 (Daily Data)")

    # 레전드 설정
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    # 그래프 출력 (여기서 한 번만 호출)
    plt.show()
            
    
            