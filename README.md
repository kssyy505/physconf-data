# physconf-data

[PhysConf Hunter](#) 안드로이드 앱이 읽는 **반도체·물리 학회 일정 데이터**입니다.

- 앱은 `https://raw.githubusercontent.com/kssyy505/physconf-data/main/conferences.json`을 앱을 열 때(12시간 간격) 내려받습니다.
- 매주 월요일 아침 예약 작업(Claude)이 [`UPDATE_GUIDE.md`](UPDATE_GUIDE.md) 규칙에 따라 공식 사이트를 확인하고 이 파일을 갱신합니다. 변경 내역은 [`CHANGELOG.md`](CHANGELOG.md)와 커밋 기록에 남습니다.
- 추적하고 싶은 학회를 추가하려면 [`WATCHLIST.md`](WATCHLIST.md)에 학회 이름을 적어두세요. 다음 주간 업데이트 때 조사해서 추가합니다.
- 직접 고친 경우 `python3 scripts/validate.py`로 형식을 확인한 뒤 커밋하세요. 형식이 깨지면 앱은 새 데이터를 무시하고 이전 데이터를 계속 씁니다.

> 학회 일정은 바뀔 수 있습니다. 마감 전에는 반드시 각 학회 공식 사이트에서 다시 확인하세요.
