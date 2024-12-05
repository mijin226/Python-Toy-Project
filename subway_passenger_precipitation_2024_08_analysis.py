import pandas as pd
import chardet
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 한글 폰트를 matplotlib에 적용하는 코드
font_path = "C:/Windows/Fonts/malgun.ttf"  # Windows의 '맑은 고딕' 폰트 경로
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()

# 강수량 데이터 로드 함수
def load_precipitation_data(file_path):
    try:
        df_precipitation = pd.read_csv(file_path, encoding='ANSI')
        print("Loaded precipitation data with ANSI encoding.")
        
        # 열 이름 확인
        print("강수량 데이터 열 확인:", df_precipitation.columns)
        
        # 열 이름을 실제 파일에 맞게 수정
        df_precipitation.columns = ['날짜', '지점', '강수량(mm)']
        df_precipitation['날짜'] = pd.to_datetime(df_precipitation['날짜'], format='%Y-%m-%d')
        return df_precipitation
    except Exception as e:
        print(f"Error loading precipitation data: {e}")
        return None

# 지하철 데이터 로드 함수
def load_subway_data(file_path):
    try:
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
            encoding = result['encoding']
            print(f"Detected encoding: {encoding}")
        
        df_subway = pd.read_csv(file_path, encoding=encoding)
        print(f"Loaded subway data with {encoding} encoding.")
        
        # 열 이름 확인
        print("지하철 데이터 열 확인:", df_subway.columns)
        
        df_subway.columns = ['사용일자', '노선명', '역명', '승차총승객수', '하차총승객수']
        df_subway['사용일자'] = pd.to_datetime(df_subway['사용일자'], format='%Y%m%d')
        return df_subway
    except Exception as e:
        print(f"Error loading subway data: {e}")
        return None

# 데이터 병합 함수
def merge_data(subway_df, precipitation_df):
    try:
        merged_data = pd.merge(subway_df, precipitation_df, left_on='사용일자', right_on='날짜', how='left')
        merged_data['강수량(mm)'] = merged_data['강수량(mm)'].fillna(0)
        print("Data merged successfully.")
        return merged_data
    except Exception as e:
        print(f"Error merging data: {e}")
        return None

# 그래프 그리기 함수
def plot_ridership_vs_precipitation(merged_data):
    try:
        fig, ax1 = plt.subplots(figsize=(10, 6))
        
        # 승차 + 하차 총 승객수 계산
        merged_data['승차 + 하차 총 승객수'] = merged_data['승차총승객수'] + merged_data['하차총승객수']
        
        # 첫 번째 Y축 (승차 + 하차 총 승객수)
        ax1.bar(merged_data['사용일자'], merged_data['승차 + 하차 총 승객수'], color='#FFD700', label='승차 + 하차 총 승객수')
        ax1.set_xlabel('날짜')
        ax1.set_ylabel('승차 + 하차 총 승객수', color='black')
        ax1.tick_params(axis='y', labelcolor='black')
        ax1.set_ylim(100000, 300000)  # 승차 + 하차 총 승객수 y축 범위 설정
        
        # 두 번째 Y축 (강수량)
        ax2 = ax1.twinx()
        ax2.plot(merged_data['사용일자'], merged_data['강수량(mm)'], color='#228B22', label='강수량(mm)', linestyle='-', marker='o')
        ax2.set_ylabel('강수량(mm)', color='#228B22')
        ax2.tick_params(axis='y', labelcolor='#228B22')
        ax2.set_ylim(0, 50)  # 강수량 y축 범위 설정
        
        ax1.set_title('하루 승차 + 하차 총 승객수와 강수량 비교 (24년 8월)')
        
        # 그리드와 범례
        ax1.grid(True, linestyle='--', alpha=0.7)
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')
        
        plt.tight_layout()
        plt.show()
        print("Plot displayed successfully.")
    except Exception as e:
        print(f"Error displaying plot: {e}")

# 메인 코드
if __name__ == "__main__":
    # 파일 경로 설정
    precipitation_file = 'precipitation_202408.csv'  # 강수량 데이터 파일
    subway_file = 'subway_202408.csv'  # 지하철 데이터 파일
    
    # 데이터 로드
    precipitation_data = load_precipitation_data(precipitation_file)
    subway_data = load_subway_data(subway_file)
    
    # 병합 및 시각화
    if precipitation_data is not None and subway_data is not None:
        merged_data = merge_data(subway_data, precipitation_data)
        if merged_data is not None:
            plot_ridership_vs_precipitation(merged_data)
        else:
            print("데이터 병합에 실패했습니다.")
    else:
        print("데이터 로드에 실패했습니다.")
import pandas as pd
import chardet
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 한글 폰트를 matplotlib에 적용하는 코드
font_path = "C:/Windows/Fonts/malgun.ttf"  # Windows의 '맑은 고딕' 폰트 경로
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()

# 강수량 데이터 로드 함수
def load_precipitation_data(file_path):
    try:
        df_precipitation = pd.read_csv(file_path, encoding='ANSI')
        print("Loaded precipitation data with ANSI encoding.")
        
        # 열 이름 확인
        print("강수량 데이터 열 확인:", df_precipitation.columns)
        
        # 열 이름을 실제 파일에 맞게 수정
        df_precipitation.columns = ['날짜', '지점', '강수량(mm)']
        df_precipitation['날짜'] = pd.to_datetime(df_precipitation['날짜'], format='%Y-%m-%d')
        return df_precipitation
    except Exception as e:
        print(f"Error loading precipitation data: {e}")
        return None

# 지하철 데이터 로드 함수
def load_subway_data(file_path):
    try:
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
            encoding = result['encoding']
            print(f"Detected encoding: {encoding}")
        
        df_subway = pd.read_csv(file_path, encoding=encoding)
        print(f"Loaded subway data with {encoding} encoding.")
        
        # 열 이름 확인
        print("지하철 데이터 열 확인:", df_subway.columns)
        
        df_subway.columns = ['사용일자', '노선명', '역명', '승차총승객수', '하차총승객수']
        df_subway['사용일자'] = pd.to_datetime(df_subway['사용일자'], format='%Y%m%d')
        return df_subway
    except Exception as e:
        print(f"Error loading subway data: {e}")
        return None

# 데이터 병합 함수
def merge_data(subway_df, precipitation_df):
    try:
        merged_data = pd.merge(subway_df, precipitation_df, left_on='사용일자', right_on='날짜', how='left')
        merged_data['강수량(mm)'] = merged_data['강수량(mm)'].fillna(0)
        print("Data merged successfully.")
        return merged_data
    except Exception as e:
        print(f"Error merging data: {e}")
        return None

# 그래프 그리기 함수
def plot_ridership_vs_precipitation(merged_data):
    try:
        fig, ax1 = plt.subplots(figsize=(10, 6))
        
        # 승차 + 하차 총 승객수 계산
        merged_data['승차 + 하차 총 승객수'] = merged_data['승차총승객수'] + merged_data['하차총승객수']
        
        # 첫 번째 Y축 (승차 + 하차 총 승객수)
        ax1.bar(merged_data['사용일자'], merged_data['승차 + 하차 총 승객수'], color='#FFD700', label='승차 + 하차 총 승객수')
        ax1.set_xlabel('날짜')
        ax1.set_ylabel('승차 + 하차 총 승객수', color='black')
        ax1.tick_params(axis='y', labelcolor='black')
        ax1.set_ylim(100000, 300000)  # 승차 + 하차 총 승객수 y축 범위 설정
        
        # 두 번째 Y축 (강수량)
        ax2 = ax1.twinx()
        ax2.plot(merged_data['사용일자'], merged_data['강수량(mm)'], color='#228B22', label='강수량(mm)', linestyle='-', marker='o')
        ax2.set_ylabel('강수량(mm)', color='#228B22')
        ax2.tick_params(axis='y', labelcolor='#228B22')
        ax2.set_ylim(0, 50)  # 강수량 y축 범위 설정
        
        ax1.set_title('하루 승차 + 하차 총 승객수와 강수량 비교 (24년 8월)')
        
        # 그리드와 범례
        ax1.grid(True, linestyle='--', alpha=0.7)
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')
        
        plt.tight_layout()
        plt.show()
        print("Plot displayed successfully.")
    except Exception as e:
        print(f"Error displaying plot: {e}")

# 메인 코드
if __name__ == "__main__":
    # 파일 경로 설정
    precipitation_file = 'precipitation_202408.csv'  # 강수량 데이터 파일
    subway_file = 'subway_202408.csv'  # 지하철 데이터 파일
    
    # 데이터 로드
    precipitation_data = load_precipitation_data(precipitation_file)
    subway_data = load_subway_data(subway_file)
    
    # 병합 및 시각화
    if precipitation_data is not None and subway_data is not None:
        merged_data = merge_data(subway_data, precipitation_data)
        if merged_data is not None:
            plot_ridership_vs_precipitation(merged_data)
        else:
            print("데이터 병합에 실패했습니다.")
    else:
        print("데이터 로드에 실패했습니다.")
