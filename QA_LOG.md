# QA Log

## 2025-11-17

### Issue #1: BTC 등락률이 정상적으로 표시되지 않음

**문제 설명:**
- BTC 위젯에서 등락률이 표시되지 않거나 잘못된 값이 표시됨
- 신호 아이콘도 기본값(⚪⚪⚪⚪⚪)만 표시됨

**원인 분석:**
- API 응답의 실제 필드명과 코드에서 사용하는 필드명이 불일치
- 7code.co.kr API는 `fluctate_rate`를 제공하는데 코드에서는 `fluctate_rate_24H`를 요청
- 거래량도 `volume`을 제공하는데 `acc_trade_value_24H`를 요청

**API 응답 구조:**
```json
{
    "closing_price": 141701000.0,
    "fluctate_rate": -1.1820413400652738,
    "name": "BTC",
    "prev_closing_price": 143396000.0,
    "symbol": "BTC_KRW",
    "volume": 163544589481.12
}
```

**수정 내용:**
- `src/ui/crypto_widget.py:81` - `fluctate_rate_24H` → `fluctate_rate`
- `src/ui/crypto_widget.py:115` - `acc_trade_value_24H` → `volume`
- `src/ui/crypto_widget.py:114` - 툴팁 텍스트 "24h 변동" → "변동"

**수정된 코드:**
```python
# Line 81
change_rate = btc_data.get('fluctate_rate', 0)

# Line 115-117
if 'volume' in btc_data:
    volume = btc_data['volume']
    tooltip += f"거래량: ₩{volume/100000000:.1f}억\n"
```

**테스트 결과:**
- ✅ BTC 등락률이 정상적으로 표시됨 (예: -1.18%)
- ✅ 색상이 올바르게 적용됨 (하락: 빨간색, 상승: 초록색)
- ✅ 신호 아이콘이 등락률에 따라 정상 표시됨 (🔴🔴⚪⚪⚪)
- ✅ 툴팁에 거래량이 정상적으로 표시됨

**Status:** ✅ Resolved

---

## Test Checklist

### BTC Widget Tests
- [x] BTC 가격 표시
- [x] 등락률 표시 및 색상 (양수: 초록, 음수: 빨강)
- [x] 신호 아이콘 표시
  - [x] > 2%: 🟢🟢🟢⚪⚪
  - [x] 0~2%: 🟢🟢⚪⚪⚪
  - [x] -2~0%: 🔴🔴⚪⚪⚪
  - [x] < -2%: 🔴🔴🔴⚪⚪
- [x] 클릭 시 7code.co.kr 웹사이트 열림
- [x] 30초마다 자동 업데이트
- [x] 툴팁 표시 (가격, 등락률, 거래량)

### Weather Widget Tests
- [x] IP 기반 자동 위치 감지
- [x] 현재 온도 표시
- [x] 날씨 아이콘 및 설명
- [x] 습도 표시
- [x] 미세먼지 정보
- [x] 10분마다 자동 업데이트

### Clock Widget Tests
- [x] 디지털/아날로그 모드 전환
- [x] 창 크기에 따른 자동 스케일링
- [x] 한글 요일 표시

### Calendar Widget Tests
- [x] 현재 날짜 강조 표시
- [x] 한글 요일 헤더

### Theme Tests
- [x] 다크/라이트 모드 전환
- [x] 설정 저장 및 복원

### General Tests
- [x] 창 크기 조절 (최소: 735x800)
- [x] 설정 자동 저장 (user_settings.json)
- [x] 애플리케이션 시작 시 이전 설정 복원
