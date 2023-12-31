import cv2
import requests
import numpy as np
import random
from google.colab.patches import cv2_imshow

# 첫 번째 감지된 원에 선을 그리는 함수
def detect_circle_and_draw_line(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            cv2.circle(image, (x, y), r, (0, 255, 0), 4)
            cv2.line(image, (x - r, y), (x + r, y), (255, 0, 0), 3)
            break


# 점수 구역 시각화 함수
def define_score_zones(image, target_x, target_y, radii):
    for radius in radii:
        cv2.circle(image, (target_x, target_y), radius, (255, 255, 255), 2)



# 이미지 URL

image_path = 'https://github.com/wnsrl3/TeamProject/blob/main/1.png?raw=true'

# 이미지 다운로드 및 디코딩
try:
    response = requests.get(image_path)
    response.raise_for_status()  # 요청이 실패할 경우 오류 발생 (4xx 또는 5xx 상태 코드)
    img_array = np.frombuffer(response.content, dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # 그레이스케일로 변환하고 에지 검출
    if img is not None:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        
        # 창에 에지 이미지 표시 후 키 입력 대기
        cv2_imshow(edges)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("이미지를 로드하는 데 실패했습니다.")
except requests.HTTPError as e:
    print(f"HTTP 오류 발생: {e}")
except requests.RequestException as e:
    print(f"요청 예외 발생: {e}")
except Exception as e:
    print(f"오류 발생: {e}")

# 윤곽선 찾기 및 그리기
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img, contours, -1, (0, 255, 0), 3)

# 원 감지 및 선 그리기
detect_circle_and_draw_line(img)

# 타겟 위치 및 점수 구역 정의
radii_scores = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
target_x, target_y = 100, 100
#점수 구역 색으로 표시
def draw_score_zones(image,target_x,target_y,radii):
    for radius in radii:
        cv2.circle(image,(target_x, target_y),radius,(0,0,255),-1)
#이미지 점수 구역 그리기 
draw_score_zones(img, target_x, target_y, radii_scores)
# 타겟 위치와 점수 구역 표시 이미지
cv2_imshow(img)