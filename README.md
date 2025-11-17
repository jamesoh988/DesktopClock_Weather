# Ubuntu Desktop Clock & Weather Application

우분투 데스크탑용 시계, 달력, 날씨 표시 애플리케이션

## 프로젝트 개요

Python을 사용하여 우분투 데스크탑에서 실행되는 시계, 달력, 날씨 정보를 표시하는 GUI 애플리케이션입니다.

## 주요 기능

### 1. 시계 기능
- **디지털 시계**: 시간을 숫자로 표시
- **아날로그 시계**: 전통적인 시계 형태로 표시
- 실시간 업데이트
- 디지털/아날로그 모드 전환 기능

### 2. 달력 기능
- 현재 날짜 표시
- 월간 달력 뷰
- 요일 및 날짜 정보

### 3. 날씨 기능
- 현재 날씨 정보
- 기온 표시
- 날씨 아이콘
- 미세먼지 정보 표시

### 4. UI/UX 기능
- **다크 모드**: 어두운 테마
- **화이트 모드**: 밝은 테마
- **크기 조절**: 윈도우 크기 조절 가능
- 모드 간 전환 버튼

## 기술 스택

### GUI 프레임워크
- **PyQt5** 또는 **PyQt6**: 현대적이고 강력한 GUI 프레임워크
  - 아날로그 시계 그리기 지원
  - 테마 커스터마이징 용이
  - 크로스 플랫폼 지원

### 날씨 API
- **OpenWeatherMap API**: 날씨 정보 제공
- **AirVisual API** 또는 **한국환경공단 API**: 미세먼지 정보

### 기타 라이브러리
- `requests`: API 호출
- `datetime`: 시간 및 날짜 처리
- `calendar`: 달력 기능

## 프로젝트 구조

```
month_time/
├── README.md
├── requirements.txt
├── main.py                 # 메인 실행 파일
├── config.py              # 설정 파일
├── src/
│   ├── __init__.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py      # 메인 윈도우
│   │   ├── clock_widget.py     # 시계 위젯
│   │   ├── calendar_widget.py  # 달력 위젯
│   │   └── weather_widget.py   # 날씨 위젯
│   ├── widgets/
│   │   ├── __init__.py
│   │   ├── digital_clock.py    # 디지털 시계
│   │   └── analog_clock.py     # 아날로그 시계
│   ├── services/
│   │   ├── __init__.py
│   │   ├── weather_service.py  # 날씨 API 서비스
│   │   └── air_quality_service.py  # 미세먼지 API 서비스
│   └── themes/
│       ├── __init__.py
│       ├── dark_theme.py       # 다크 모드 스타일
│       └── light_theme.py      # 라이트 모드 스타일
└── resources/
    ├── icons/                  # 아이콘 파일들
    └── fonts/                  # 폰트 파일들 (선택사항)
```

## 설치 및 실행

### 1. 필수 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. 애플리케이션 실행

```bash
python main.py
```

**참고**: 무료 Open-Meteo API를 사용하므로 API 키 설정이 필요하지 않습니다.

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
    "mode": "analog",
    "scale": 1.0
  },
  "location": {
    "city": "Seoul",
    "latitude": 37.5665,
    "longitude": 126.978
  }
}
```

### 설정 항목

- **window**: 윈도우 크기 (자동 저장)
- **theme**: 테마 (`dark` 또는 `light`)
- **clock.mode**: 시계 모드 (`digital` 또는 `analog`)
- **clock.scale**: 시계 크기 배율 (0.5 ~ 2.0)
- **location**: 날씨 위치 정보

설정 파일을 직접 수정하거나, UI에서 변경한 내용이 자동으로 저장됩니다.

## 개발 계획

### Phase 1: 기본 UI 구조
- [ ] PyQt5/6 설치 및 기본 윈도우 생성
- [ ] 레이아웃 구조 설계
- [ ] 크기 조절 가능한 윈도우 구현

### Phase 2: 시계 기능
- [ ] 디지털 시계 구현
- [ ] 아날로그 시계 구현
- [ ] 시계 모드 전환 기능

### Phase 3: 달력 기능
- [ ] 현재 날짜 표시
- [ ] 월간 달력 뷰 구현

### Phase 4: 날씨 기능
- [ ] 날씨 API 연동
- [ ] 미세먼지 API 연동
- [ ] 날씨 정보 UI 구현

### Phase 5: 테마 기능
- [ ] 다크 모드 스타일 구현
- [ ] 화이트 모드 스타일 구현
- [ ] 테마 전환 기능

### Phase 6: 최적화 및 개선
- [ ] 성능 최적화
- [ ] UI/UX 개선
- [ ] 에러 처리
- [ ] 설정 저장 기능 (마지막 사용한 모드, 위치 등)

## 라이선스

MIT License

## 기여

이슈와 PR은 언제나 환영합니다!
