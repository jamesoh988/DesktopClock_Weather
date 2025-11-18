# Ubuntu Desktop Clock & Weather Application

우분투 데스크탑용 시계, 달력, 날씨, 암호화폐 표시 애플리케이션

## 프로젝트 개요

Python과 PyQt5를 사용하여 우분투 데스크탑에서 실행되는 시계, 달력, 날씨, 암호화폐 정보를 표시하는 GUI 애플리케이션입니다.

## 주요 기능

### 1. 시계 기능
- **디지털 시계**: 시간을 숫자로 표시
  - 영어 날짜 표시 (예: "January 15, 2025 Monday")
- **아날로그 시계**: 전통적인 시계 형태로 표시
  - 시계 하단에 디지털 시간 표시 (개선된 30px 간격)
  - 크기 조절 시 디지털 시간 잘림 방지 (v1.3.0)
  - 다크/라이트 테마 자동 적용
- 실시간 업데이트 (1초 간격)
- 디지털/아날로그 모드 전환 기능
- 윈도우 크기에 따른 자동 스케일링

### 2. 달력 기능
- 현재 날짜 강조 표시
- 월간 달력 뷰
- 영어 날짜 표시 (예: "January 15, 2025 Monday")
- 이전/다음 달 탐색
- **자동 날짜 동기화**: 1분마다 현재 날짜 자동 업데이트

### 3. 날씨 기능
- **자동 위치 감지**: IP 기반으로 현재 위치 자동 감지
- 현재 기온 표시
- 날씨 아이콘 및 설명
- 습도 정보
- **미세먼지(PM2.5) 정보**: 실시간 대기질 표시
- 10분마다 자동 업데이트
- 위치 표시 (도시명)

### 4. 암호화폐 위젯
- **다중 코인 순환 표시**: BTC, USDT, ETH, XRP, SOL
- **부드러운 슬라이드 애니메이션**: 5초마다 자동 전환
- 실시간 가격 및 등락률 표시
- 색상 코드:
  - 상승: 초록색
  - 하락: 빨간색
- **분석 신호 표시**: 5단계 신호 인디케이터 (●)
  - 등락률 기반 자동 신호 생성
- **개선된 레이아웃**:
  - 최적화된 라벨 폭 (코인: 200px, 가격: 180px, 신호: 170px)
  - 최소 너비 570px로 고정하여 축소 방지
- 7code.co.kr API 연동
- 클릭 시 웹사이트 열기
- 30초마다 데이터 갱신

### 5. UI/UX 기능
- **다크 모드**: 어두운 테마
- **라이트 모드**: 밝은 테마
- **크기 조절**: 윈도우 크기 조절 가능 (최소: 735x800)
- **시계/달력 크기 조절**: 마우스 드래그로 위젯 간 비율 조정
- 모드 간 전환 버튼 (영어 표시)
- 설정 자동 저장 및 복원
- 균형잡힌 레이아웃 (날씨 좌측, 암호화폐 우측)

## 기술 스택

### GUI 프레임워크
- **PyQt5**: 크로스 플랫폼 GUI 프레임워크
  - 아날로그 시계 그리기 지원
  - 테마 커스터마이징
  - 애니메이션 지원 (QPropertyAnimation)

### API 서비스
- **Open-Meteo API**: 무료 날씨 정보 제공 (API 키 불필요)
- **7code.co.kr API**: 암호화폐 시세 정보
- **ip-api.com**: IP 기반 위치 감지
- **ipapi.co**: 위치 감지 백업 서비스

### 라이브러리
- `PyQt5`: GUI 프레임워크
- `requests`: API 호출
- `python-dateutil`: 날짜/시간 처리

## 프로젝트 구조

```
month_time/
├── README.md
├── requirements.txt
├── main.py                # 메인 실행 파일
├── config.py             # 설정 파일
├── user_settings.json    # 사용자 설정 (자동 생성)
├── src/
│   ├── ui/
│   │   ├── main_window.py       # 메인 윈도우
│   │   ├── calendar_widget.py   # 달력 위젯
│   │   ├── weather_widget.py    # 날씨 위젯
│   │   └── crypto_widget.py     # 암호화폐 위젯 (NEW!)
│   ├── widgets/
│   │   ├── digital_clock.py     # 디지털 시계
│   │   └── analog_clock.py      # 아날로그 시계
│   ├── services/
│   │   ├── free_weather_service.py   # Open-Meteo API
│   │   ├── location_service.py       # 위치 감지 서비스
│   │   └── crypto_service.py         # 암호화폐 API (NEW!)
│   ├── themes/
│   │   ├── dark_theme.py        # 다크 모드
│   │   └── light_theme.py       # 라이트 모드
│   └── utils/
│       └── settings_manager.py  # 설정 관리
└── .github/
    └── workflows/
        └── build.yml            # CI/CD 자동 빌드
```

## 설치 및 실행

### 1. 시스템 요구사항

Ubuntu 24.04 LTS 이상 권장

필수 시스템 패키지:
```bash
sudo apt-get install -y \
    libxcb-xinerama0 libxcb-cursor0 libxkbcommon-x11-0 \
    libxcb-icccm4 libxcb-image0 libxcb-keysyms1 \
    libxcb-randr0 libxcb-render-util0 libxcb-shape0 \
    libdbus-1-3 libxcb-xfixes0 libxcb1 libx11-xcb1 \
    libgl1 libegl1
```

### 2. Python 가상환경 설정 (권장)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Python 패키지 설치

```bash
pip install -r requirements.txt
```

### 4. 애플리케이션 실행

```bash
python main.py
```

## 사용자 설정

애플리케이션의 설정은 `user_settings.json` 파일에 자동으로 저장됩니다:

```json
{
  "window": {
    "width": 1200,
    "height": 900
  },
  "theme": "dark",
  "clock": {
    "mode": "analog"
  }
}
```

### 설정 항목

- **window**: 윈도우 크기 (자동 저장)
- **theme**: 테마 (`dark` 또는 `light`)
- **clock.mode**: 시계 모드 (`digital` 또는 `analog`)

설정 파일을 직접 수정하거나, UI에서 변경한 내용이 자동으로 저장됩니다.

## 빌드 및 배포

### GitHub Actions 자동 빌드

프로젝트는 GitHub Actions를 통해 자동으로 빌드됩니다:
- Windows용 `.exe` 파일
- macOS용 실행 파일
- Linux용 실행 파일

### 릴리즈 생성

```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

릴리즈는 자동으로 GitHub Releases 페이지에 업로드됩니다.

## 스크린샷

### 다크 모드
- 디지털 시계 모드
- 아날로그 시계 모드
- 날씨 및 미세먼지 정보
- 암호화폐 가격 순환 표시

### 라이트 모드
- 밝은 테마
- 깔끔한 UI

## 주요 특징

### 자동 위치 감지
IP 주소를 기반으로 자동으로 위치를 감지하여 해당 지역의 날씨를 표시합니다.
- 주 서비스: ip-api.com
- 백업 서비스: ipapi.co
- 실패 시 기본값: 서울

### 암호화폐 위젯 애니메이션
- **슬라이드 효과**: 400ms 부드러운 InOutCubic 이징
- **자동 순환**: BTC → USDT → ETH → XRP → SOL (5초 간격)
- **최적화된 레이아웃** (v1.1.0):
  - 코인명+등락률: 200px
  - 가격: 180px
  - 신호: 170px
  - 전체 최소 폭: 570px (축소 방지)

### 반응형 디자인
- 시계 크기가 윈도우 크기에 따라 자동으로 조절
- 최소 윈도우 크기: 735x800

## 개발 로드맵

### ✅ 완료된 기능
- [x] PyQt5 기본 윈도우 생성
- [x] 디지털 시계 구현
- [x] 아날로그 시계 구현
- [x] 시계 모드 전환 기능
- [x] 달력 뷰 구현
- [x] 날씨 API 연동 (Open-Meteo)
- [x] 미세먼지 정보 표시
- [x] 다크/라이트 모드
- [x] 설정 저장 기능
- [x] IP 기반 자동 위치 감지
- [x] GitHub Actions CI/CD
- [x] 암호화폐 위젯 (다중 코인 순환)
- [x] 슬라이드 애니메이션
- [x] 반응형 레이아웃
- [x] 달력 자동 날짜 동기화 (v1.1.0)
- [x] 암호화폐 위젯 레이아웃 최적화 (v1.1.0)
- [x] 아날로그 시계 디지털 표시 간격 개선 (v1.1.0)
- [x] 시계/달력 크기 조절 (QSplitter) (v1.2.0)
- [x] 날씨/암호화폐 위젯 레이아웃 균형 (v1.2.0)
- [x] 영어 UI 지원 (v1.3.0)
- [x] 아날로그 시계 크기 조절 시 디지털 시간 잘림 방지 (v1.3.0)

### 🔜 향후 계획
- [ ] 알림 기능
- [ ] 시스템 트레이 통합
- [ ] 추가 암호화폐 지원
- [ ] 차트 표시 기능
- [ ] 사용자 정의 코인 리스트

## 트러블슈팅

### PyQt5 XCB 플러그인 오류
```bash
sudo apt-get install libxcb-xinerama0 libxcb-cursor0
```

### 이모지 표시 문제
Unicode 원형(●) 문자를 사용하여 호환성 개선

### 위치 감지 실패
기본 위치(서울)로 폴백하며, 수동으로 설정 파일 수정 가능

## 라이선스

MIT License

## 기여

이슈와 PR은 언제나 환영합니다!

## 링크

- GitHub: https://github.com/jamesoh988/DesktopClock_Weather
- Releases: https://github.com/jamesoh988/DesktopClock_Weather/releases
