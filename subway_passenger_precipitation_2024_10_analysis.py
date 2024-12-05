import pandas as pd
import chardet
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 한글 폰트를 matplotlib에 적용하는 코드
font_path = "C:/Windows/Fonts/malgun.ttf"  # 윈도우에서 사용하는 '맑은 고딕' 폰트 경로
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()

# 강수량 데이터 로드 함수
def load_precipitation_data(file_path):
    try:
        # ANSI 인코딩으로 로드
        df_precipitation = pd.read_csv(file_path, encoding='ANSI')
        print(f"Loaded precipitation data with ANSI encoding.")
        
        # 열 이름 확인
        print("강수량 데이터 열 확인:", df_precipitation.columns)
        
        # 열 이름을 실제 파일에 맞게 수정 (지점 열을 제외한 강수량과 날짜 열만 사용)
        df_precipitation.columns = ['날짜', '지점', '강수량(mm)']
        df_precipitation['날짜'] = pd.to_datetime(df_precipitation['날짜'], format='%Y-%m-%d')  # 날짜 형식 변환
        
        return df_precipitation
    
    except Exception as e:
        print(f"Error loading precipitation data: {e}")
        return None

# 지하철 데이터 로드 함수 (자동 인코딩 감지)
def load_subway_data(file_path):
    try:
        # 파일의 인코딩을 자동으로 감지하기 위해 chardet 사용
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
            encoding = result['encoding']
            print(f"Detected encoding: {encoding}")
        
        # 자동으로 감지된 인코딩으로 파일을 읽음
        df_subway = pd.read_csv(file_path, encoding=encoding)
        print(f"Loaded subway data with {encoding} encoding.")
        
        # 열 이름 확인
        print("지하철 데이터 열 확인:", df_subway.columns)
        
        # 열 이름을 실제 파일에 맞게 수정
        df_subway.columns = ['사용일자', '노선명', '역명', '승차총승객수', '하차총승객수']  # 실제 열 이름으로 수정
        
        # 날짜 형식을 맞춰줍니다.
        df_subway['사용일자'] = pd.to_datetime(df_subway['사용일자'], format='%Y%m%d')
        
        return df_subway
    
    except Exception as e:
        print(f"Error loading subway data: {e}")
        return None

# 지하철 데이터와 강수량 데이터를 결합하는 함수
def merge_data(subway_df, precipitation_df):
    try:
        # 날짜를 기준으로 두 데이터프레임 병합
        merged_data = pd.merge(subway_df, precipitation_df, left_on='사용일자', right_on='날짜', how='left')
        
        # 강수량이 결측치인 날에는 0으로 채우기
        merged_data['강수량(mm)'] = merged_data['강수량(mm)'].fillna(0)
        
        print("Data merged successfully.")
        return merged_data
    except Exception as e:
        print(f"Error merging data: {e}")
        return None

# 그래프를 그려주는 함수 (예시: 승차 총 승객수 + 하차 총 승객수와 강수량 비교)
def plot_ridership_vs_precipitation(merged_data):
    try:
        fig, ax1 = plt.subplots(figsize=(10, 6))

        # 첫 번째 Y축: 승차 총 승객수 + 하차 총 승객수 막대 그래프
        merged_data['승차 + 하차 총 승객수'] = merged_data['승차총승객수'] + merged_data['하차총승객수']
        ax1.bar(merged_data['사용일자'], merged_data['승차 + 하차 총 승객수'], color='#FFD700', label='승차 + 하차 총 승객수')  # 따뜻한 금색
        ax1.set_xlabel('날짜')
        ax1.set_ylabel('승차 + 하차 총 승객수', color='black')
        ax1.tick_params(axis='y', labelcolor='black')
        
        # 승하차 총 승객수 범위를 10만부터 30만까지 설정
        ax1.set_ylim(100000, 300000)  # Y축 범위를 100,000 ~ 300,000으로 설정

        ax1.set_title('하루 승차 + 하차 총 승객수와 강수량 비교 (24년 10월)')

        # 두 번째 Y축: 강수량 그래프 (직선 그래프)
        ax2 = ax1.twinx()  # 두 번째 Y축 생성
        ax2.plot(merged_data['사용일자'], merged_data['강수량(mm)'], color='#228B22', label='강수량(mm)', linestyle='-', marker='o')  # 시원한 초록색
        ax2.set_ylabel('강수량(mm)', color='#228B22')
        ax2.tick_params(axis='y', labelcolor='#228B22')

        # 강수량 Y축 범위 설정
        ax2.set_ylim(0, 50)  # Y축 범위를 0 ~ 50으로 설정

        # 그리드, 범례 설정
        ax1.grid(True, linestyle='--', alpha=0.7)  # 그리드 선을 점선으로 설정하고 투명도 설정
        fig.tight_layout()
        
        # 범례 추가
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')
        
        plt.show()
        print("Plot displayed successfully.")
    except Exception as e:
        print(f"Error displaying plot: {e}")

# 메인 코드
if __name__ == "__main__":
    # 강수량 데이터 파일 경로 (예시)
    precipitation_file = 'precipitation_202410.csv'  # 실제 경로를 넣어야 합니다.
    subway_file = 'subway_202410.csv'  # 실제 경로를 넣어야 합니다.
    
    # 강수량 데이터 로드
    precipitation_data = load_precipitation_data(precipitation_file)
    
    # 지하철 데이터 로드
    subway_data = load_subway_data(subway_file)
    
    # 데이터가 모두 로드되었을 때 병합
    if precipitation_data is not None and subway_data is not None:
        merged_data = merge_data(subway_data, precipitation_data)
        
        # 병합된 데이터가 있을 때 그래프 출력
        if merged_data is not None:
            plot_ridership_vs_precipitation(merged_data)
        else:
            print("데이터 병합에 실패했습니다.")
    else:
        print("데이터 로드에 실패했습니다.")
