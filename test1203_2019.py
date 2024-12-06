import csv                                                              ## CSV 파일 처리를 위한 모듈
import matplotlib.pyplot as plt                                         ## 데이터 시각화를 위한 모듈
import seaborn as sns       # 고급화된 그래프

## 월별 기온 데이터 파일
temps_file_path = "ta_20241130204917.csv"        
subway_file_path = "2019_월별 승하차인원.csv"

years = list(range(1, 13))                                              ## 1부터 12까지의 숫자(1월~12월)
avg_temps = []                                                          ## 평균 기온(왼쪽 y축 꺾은선 그래프)
months_sum_subways = [0] * 12


## 1. 기온데이터 확인
## CSV 파일을 읽기
with open(temps_file_path, mode='r') as file:
    reader = csv.reader(file)                                           ## CSV 파일의 내용을 읽어오는 reader 객체 생성

    ## 첫 8행은 헤더로 처리하여 건너뛰기
    for _ in range(8):  
        next(reader)  

    ## 파일의 각 행을 순회하며 데이터 처리
    for row in reader:
        ## 월별 기온 데이터 추출하기(2022년도)
        if row[0].startswith('19-'):                                   ## '19-'(2020년도)으로 시작하는 데이터 추출
            avg_temp = float(row[2])                                   ## 3열에서의 실수형태 데이터 변수 선언
            avg_temps.append(avg_temp)                                 ## 3열 데이터 추출

## 데이터 출력
print("\n월별 평균기온↓")
for temp in avg_temps:
    print(temp)                    


## 2. 승하차인원 데이터 확인 및 요청사항 처리
with open(subway_file_path, mode='r') as file:
    reader = csv.reader(file)
    header = next(reader)  ## 첫 번째 행 건너뛰기
     
    for row in reader:
        for i in range(12):  # 1월부터 12월까지의 데이터 처리
            try:
                person_subway = int(row[3 + i])  ## 월별 승하차인원 데이터
                months_sum_subways[i] += person_subway  ## 각 월별 승하차 인원 합산
            except ValueError:
                print(f"ValueError: '{row[4 + i]}' 값을 숫자로 변환할 수 없습니다.")
                continue

## i번째 인덱스에 i열의 총 합을 i-1번째 인덱스에 넣기
for i in range(1, 12):  # 1번 인덱스부터 11번까지 순회
    months_sum_subways[i - 1] = months_sum_subways[i]

print("\n월별 승하차 인원 데이터 (수정 후)↓")
for i, total in enumerate(months_sum_subways):
    print(f"{i+1}월: {total}")


## 데이터 시각화 그래프 설정
sns.set(rc={"figure.figsize":(12,8)})                                 ## 그래프 크기 설정: 가로 12, 세로 8인치
plt.rcParams['lines.linewidth'] = 4.0                                 ## 그래프 선 두께
sns.set_style("white")                                                ## 그래프 배경 흰색

## 1. 왼쪽 Y축에 평균 기온을 점으로 표시하고, 선 색상과 레이블을 설정
fig, ax1 = plt.subplots()

ax1.plot(years, avg_temps, marker='o', color='tab:red', label='Avg Temperature')
ax1.set_xlabel('Month (2021)')
ax1.set_ylabel('Average Temperature (°C)', color='tab:red')
ax1.tick_params(axis='y', labelcolor='tab:red')

## 각 데이터 포인트 위에 평균 기온 값 표시
for i, temp in enumerate(avg_temps):
    ax1.text(
        years[i],
        temp + 1,
        f'{temp:.1f}',
        ha='center',
        va='bottom', fontsize=10
    )

## x축 레이블 설정
plt.xticks(years, rotation=5)

## 왼쪽 y축의 주간격 설정
min_temp = int(min(avg_temps))                                          ## 최저 기온
main_ticks = range(max(0, min_temp - 5), int(max(avg_temps)) + 5, 5)    ## 기온에 맞는 주간격 설정
sub_ticks = range(int(min(avg_temps)), int(max(avg_temps)) + 1)         ## 기온에 맞는 보조 간격 설정

## 왼쪽 Y축 주 간격을 숫자로 표시
ax1.set_yticks(main_ticks)

## 왼쪽 Y축 보조 간격에 '-' 표시 추가
for tick in sub_ticks:
    ax1.hlines(tick, xmin=0.5, xmax=12.5, color='black', linestyle='--', linewidth=0.5)


## 2. 오른쪽 Y축에 승하차인원 데이터를 표시
ax2 = ax1.twinx()  ## 두 번째 y축 생성 (오른쪽 y축)

bars = ax2.bar(years, months_sum_subways, alpha=0.6, color='tab:green', label='Subway Passengers', width=0.8)  ## 막대 그래프 폭 증가
ax2.set_ylabel('Subway Passengers (Millions)', color='tab:green')          ## 단위 수정
ax2.tick_params(axis='y', labelcolor='tab:green')

## 승하차인원의 데이터는 1백만 단위로 표시
months_sum_subways_million = [x / 1000000 for x in months_sum_subways]    ## 1백만 단위로 변환

## 오른쪽 Y축 주간격 설정: 최소 2백만, 최대 2.8백만, 1백만 단위
min_subway = 2  ## 200만
max_subway = 2.8  ## 280만
main_ticks_subway = range(int(min_subway), int(max_subway) + 1, 1)        ## 1백만 단위로 설정
ax2.set_yticks(main_ticks_subway)

## 승하차인원 주간격을 1백만 단위로 설정
ax2.set_yticklabels([f'{tick}M' for tick in main_ticks_subway])

## 각 막대 그래프 위에 승하차인원 값 표시 (백만 단위로 반올림)
for bar in bars:
    height = bar.get_height()
    rounded_value = round(height / 1000000, 2)                            ## 백만 단위로 반올림
    ax2.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.6,                                           ## 막대 위에 값을 조금 위에 표시
        f'{rounded_value}M',                                              ## 1백만 단위로 표시
        ha='center',
        va='bottom',
        fontsize=10
    )

## 왼쪽 Y축 범위 설정
ax1.set_ylim(-5, 30)
print("왼쪽 Y축:", ax1.get_ylim())

## 오른쪽 Y축 범위 설정
ax2.set_ylim(180_000_000, 350_000_000)
print("오른쪽 Y축:", ax2.get_ylim())

## 그래프 제목 설정
plt.title('Monthly Average Temperature and Subway Passengers in 2019')

## 범례 표시
fig.tight_layout()

## 그래프 화면 출력
plt.show()