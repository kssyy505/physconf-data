# 주간 자동 업데이트 지침

이 문서는 매주 실행되는 예약 작업(Claude)이 `conferences.json`을 갱신할 때 따르는 규칙이다.
PhysConf Hunter 앱은 이 저장소의 `main` 브랜치 `conferences.json`을 그대로 내려받아 쓴다.
**잘못된 값은 곧바로 사용자의 마감 알림에 영향을 주므로, 확인되지 않은 정보는 절대 넣지 않는다.**

## 1. 원칙

1. **출처 없는 정보 금지.** 날짜·장소·마감은 웹에서 직접 확인한 값만 쓴다. 각 학회의 `sources`에 근거 URL을 남긴다.
2. **공식 출처 우선.** 학회 공식 사이트·CFP PDF·주최 학회(IEEE, MRS, APS, KPS 등) 페이지에서 확인하면 `verified: "primary"`.
   일정 모음 사이트(semihub.io, conference 목록 사이트, 업체 이벤트 페이지 등)에서만 확인되면 `verified: "secondary"`, `pendingNote`에 "2차 출처 기준" 명시.
3. **모르면 비운다.** 확인 못 한 마감은 `deadlines`에 넣지 않고 `pendingNote`에 "마감 미발표" 등으로 적는다. 날짜를 추정해서 넣지 않는다(작년 패턴으로 올해 날짜를 만들지 말 것).
4. **시간 처리.** `deadlines[].at`은 UTC ISO(`YYYY-MM-DDTHH:MM:SSZ`). 공지된 현지 시각을 UTC로 변환한다.
   - 시각까지 공지됨 → 그대로 변환, `tz`에 공지 기준 시간대(예: `PDT`, `JST`, `AoE`, `EDT 15:00`).
   - 날짜만 공지됨 → 공지 시간대의 23:59로 가정해 변환하고 `timeUnknown: true`.
   - AoE = UTC−12 (예: 10/5 23:59 AoE → `2026-10-06T11:59:00Z`). KST = UTC+9. 미국은 서머타임(대개 3월 둘째 일요일~11월 첫째 일요일) 여부 확인.
5. **기존 정보가 바뀌면** (마감 연장, 장소 변경 등) 값을 고치고 `pendingNote`에 변경 사실을 짧게 남긴다 (예: "마감 10/12→10/18 연장 (2026-10-20 확인)").

## 2. 매주 할 일

1. 저장소 최신 상태를 받는다 (`git pull`).
2. `conferences.json`의 **모든 시리즈**(`series` 값 기준)에 대해 공식 사이트/CFP를 확인한다.
   - 예정된 회차: 날짜·장소·마감이 그대로인지, 미발표였던 마감이 새로 나왔는지 확인.
   - **다음 회차 추가:** 회차가 종료됐거나 6개월 이내로 다가왔는데 다음 회차가 목록에 없으면, 다음 회차 공지를 찾아본다. 공지가 있으면 새 항목을 추가한다 (`id = series + 연도`, 예: `iedm2027`).
     공지가 없으면 추가하지 않는다.
   - 확인한 항목은 `lastChecked`를 오늘 날짜(KST, `YYYY-MM-DD`)로 바꾼다. 사이트가 열리지 않아 확인 못 한 항목은 `lastChecked`를 바꾸지 않는다.
3. **오래된 회차 정리:** 종료일(`end`)이 90일 넘게 지났고, 같은 시리즈의 더 최신 회차가 목록에 있으면 그 오래된 항목을 삭제한다. 최신 회차가 없으면 남겨둔다 (시리즈가 앱에서 사라지지 않도록).
4. **새 시리즈는 임의로 추가하지 않는다.** 단, 이 저장소의 `WATCHLIST.md`에 사용자가 적어둔 학회가 있으면 조사해서 추가한다.
5. 최상위 `version`을 오늘 날짜(KST), `updatedAt`을 현재 시각(KST ISO)으로 바꾼다. **실제 데이터 변경이 없으면** `version`/`updatedAt`/`lastChecked`만 바뀌는 커밋은 하지 않는다 — 이 경우 아무것도 커밋하지 않고 종료해도 된다. (lastChecked 갱신만 있는 주는 커밋 생략 가능)
6. `python3 scripts/validate.py`를 실행해 **오류 0**을 확인한다. 오류가 있으면 고친 뒤 다시 실행. 고칠 수 없으면 커밋하지 않는다.
7. `CHANGELOG.md` 맨 위에 이번 주 변경 내역을 추가한다 (학회별 무엇이 왜 바뀌었는지 + 출처 URL).
8. 커밋 메시지: `data: YYYY-MM-DD 주간 업데이트 (변경 N건)` 후 `main`에 push.

## 3. 필드 참고

| 필드 | 설명 |
|---|---|
| `id` | 회차 ID = `series` + `edition` (예: `kcs2027`) |
| `series` | 연도와 무관한 시리즈 키. **절대 바꾸지 말 것** — 앱의 추적·알림이 이 값에 묶여 있음 |
| `edition` | 회차 연도 (숫자) |
| `categories` | `DEV` 소자·공정, `CIR` 회로, `MAT` 재료·나노, `PHY` 물리, `QNT` 양자, `NEU` 뉴로모픽·AI HW, `OPT` 광학, `IND` 산업·전시 |
| `region` | `KR` 국내 / `INTL` 해외 |
| `start`/`end` | `YYYY-MM-DD` (현지 날짜). 미발표면 `null` |
| `lat`/`lng` | 지도 핀 좌표(개최지 근처면 충분). 모르면 `null` |
| `deadlines[]` | `type`: abstract/paper/latenews/poster/registration, `label`(선택), `at`(UTC), `tz`, `timeUnknown`(선택) |
| `pendingNote` | 사용자에게 보여줄 "확인 필요 사항" |
| `description` / `descriptionEn` | 학회 범위 한 줄 설명 (출처에서 확인된 범위만) |
| `verified` | `primary` / `secondary` |
| `sources[]` | `{title, url}` 최소 1개 |
| `lastChecked` | 마지막으로 출처를 확인한 날짜 (KST) |
