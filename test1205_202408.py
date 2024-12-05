import csv
import matplotlib.pyplot as plt
import seaborn as sns

# 파일 경로
temps_file_path = "202408_기온데이터.csv"

# 데이터 초기화
month_dates = []  # 날짜 데이터(key값)
avg_temps = []    # 평균기온
high_temps = []   # 최고기온
low_temps = []    # 최저기온

# 1. 기온 데이터 처리
# 읽기모드 기온 CSV 파일 file 별칭 선언
with open(temps_file_path, mode='r') as file:
    
    # CSV 파일 읽기
    reader = csv.reader(file)
    # 헤더 건너뛰기
    for _ in range(8):  
        next(reader)
        
    # 한 행씩 읽기
    for row in reader:
        try:
            # 날짜 데이터(문자열)에서 '2024-' 제거
            date = row[0][5:]  # 'YYYY-MM-DD'에서 'MM-DD'만 추출
            month_dates.append(date)

            # 평균, 최저, 최고 기온 데이터 추가 (빈 값은 0.0으로 대체)
            avg_temps.append(float(row[2]) if row[2] else 0.0)
            low_temps.append(float(row[3]) if row[3] else 0.0)
            high_temps.append(float(row[4]) if row[4] else 0.0)
            
        # 값이 없으면 無 표시
        except ValueError as e:
            print(f"Error converting row: {row}, error: {e}")
            continue

# 2. 데이터 시각화
plt.figure(figsize=(10, 6)) # 가로 10, 세로 6인치 설정
plt.ylim([-20,40])          # y축(기온데이터) 최저값 -20도, 최고값 40도

# 평균/최고/최저 데이터 라벨 및 마커 표시
sns.lineplot(x=month_dates, y=avg_temps, label='avg_temps', marker='o')
sns.lineplot(x=month_dates, y=high_temps, label='high_temps', marker='o')
sns.lineplot(x=month_dates, y=low_temps, label='low_temps', marker='o')

# 그래프 제목, x,y축명, 범례 표시
plt.title("Temperature by date of August 2024", fontsize=16)
plt.xlabel("August", fontsize=12)
plt.ylabel("Temperature (°C)", fontsize=12)
plt.legend(title="Temperature type")
plt.grid(True)
plt.xticks(rotation=45)  # 날짜가 겹치지 않게 회전
plt.tight_layout()

# 그래프 출력
plt.show()
