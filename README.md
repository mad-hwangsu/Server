# Code Helper🙏🏻
> 몰입캠프 3주차 프로젝트
- CHAT GPT 3.5를 이용한 코딩 테스트 연습 플랫폼
- 백준의 단계별로 풀어보기의 <재귀, 백트래킹, 동적계획법 1, 그리디 알고리즘, 분할 정복, 이분 탐색, 그래프와  순회> 문제들을 새롭게 7개의 레벨로 분류함
- 유명한 알고리즘 문제들을 GPT를 활용하여 연습할 수 있는 환경을 제공함

## 개발 팀원
- 최수연 - 숙명여자대학교 컴퓨터과학전공 19학번
- 이황근 - 성균관대학교 소프트웨어학과 19학번

## 개발 환경
- Language: JavaScript, Python
- Front-end: React.js
- Back-end: Django
- DataBase: MySQL
- IDE: VSCode

## 화면 소개

### 메인 페이지
- 백준 단계별로 풀어보기 중 주요 알고리즘 카테고리(재귀 ,백트래킹, 동적계획법..)를 총 7단계의 레벨로 분류하여 코딩 테스트 연습을 할 수 있는 페이지를 구현
- 각 레벨 버튼을 클릭하면 레벨 별 상세 페이지로 이동하여 레벨에 맞는 문제들의 목록을 볼 수 있음

<image src="https://github.com/mad-hwangsu/Client/assets/63749140/874d7df7-b851-4f4b-a41c-58e1da464c3f" />

---

### 로그인 / 회원가입 화면
<image src="https://github.com/mad-hwangsu/Client/assets/63749140/6e35be08-c4d8-47c9-aa54-80d0667d636c" />
<br/>
<image src="https://github.com/mad-hwangsu/Client/assets/63749140/784938e5-3e50-47c4-bd71-39737107adab" /> 

---

### 레벨 별 상세 페이지
- 선택한 레벨에 맞는 문제들의 목록을 확인하여, 원하는 문제 번호를 선택하여 코딩 테스트 연습하는 페이지로 넘어감

<image src="https://github.com/mad-hwangsu/Client/assets/63749140/c03bb5b9-0bd5-44ae-93ba-d31c78baff43" />

---

### 문제 페이지
- 문제 제목 (백준과 동일), 문제 설명, 문제 조건, 문제 풀이 란이 있음

<image src="https://github.com/mad-hwangsu/Client/assets/63749140/6a412b76-014c-4dfe-be5f-ea357c3d32f8" />

### a. Submit 버튼 클릭
- 문제 풀이 후 제출 버튼을 클릭하면 챗 GPT를 이용한 컴파일 과정으로 정답/오답 여부를 알 수 있음
- 정답의 경우: Refactoring 버튼이 활성화
- 오답의 경우: Hint 버튼이 활성화

<image src="https://github.com/mad-hwangsu/Client/assets/63749140/5d02b0f9-1caa-45b1-a21b-20d979e1da35" />

### b. Hint 버튼 클릭
- 힌트 버튼 클릭 시 사용자의 오답을 기반으로 챗 GPT가 30자 이내의 힌트를 제공해줌

<image src="https://github.com/mad-hwangsu/Client/assets/63749140/d6a0f0a1-2138-4d1d-a325-f6986b96f0ac" />

### c. Refactoring 버튼 클릭

- 왼쪽 란에는 사용자의 기존 답을 제공해주고, 오른쪽 란에는 챗 GPT가 제안한 최적화된 방법을 사용한 문제 풀이를 제공해줌

<image src="https://github.com/mad-hwangsu/Client/assets/63749140/d48de4a9-5541-4d20-942d-d1e7400e05af" />

---

### 틀린 문제 모아보기

- 사용자가 현재까지 정답을 내지 못한 문제들을 모아서 보여주는 페이지
-  문제 번호를 눌러서 다시 문제를 풀 기회를 제공함

<image src="https://github.com/mad-hwangsu/Client/assets/63749140/41802ae2-aa70-4337-aff4-4a1e9baa767c" />

---

### 랭킹 페이지

- 사용자들은 문제를 맞히면 10점씩 포인트를 얻음
- 얻은 포인트를 기준으로 랭킹 페이지에서 포인트가 높은 순서대로 정렬하여 보여줌

<image src="https://github.com/mad-hwangsu/Client/assets/63749140/66c90d5d-e032-4cf2-8d14-384d78be9f80" />


## ChatGPT API란?

<image src="https://github.com/mad-hwangsu/Client/assets/63749140/0feea810-ff4a-48d7-a107-265975516900" />


OpenAI의 ChatGPT API는 GPT-3 기반의 대화형 AI를 쉽게 사용할 수 있도록 제공하는 인터페이스입니다. 이 API를 사용하면 사용자의 메시지나 프롬프트에 대해 모델의 응답을 받을 수 있습니다.

기본적으로 ChatGPT API는 다음과 같은 정보를 포함하는 메시지 리스트를 받아 처리합니다:

'role': 메시지의 송신자 역할을 지정합니다. 일반적으로 'system', 'user', 'assistant' 중 하나입니다.
'content': 메시지의 내용을 포함합니다.
'role'이 'system'인 메시지는 대화의 설정이나 목표를 지정하는데 사용되고, 'user' 메시지는 사용자의 입력을 나타내며, 'assistant' 메시지는 AI의 이전 응답을 나타냅니다.

응답을 받으려면 이러한 메시지 리스트를 API에 전달하면, API는 그에 맞는 적절한 'assistant' 메시지를 반환합니다.

이 API는 언어 모델이 대화 컨텍스트를 사용하여 동적으로 응답을 생성하는 방식을 통해 더 자연스러운 대화 체험을 제공합니다.

단, API를 사용하려면 OpenAI의 이용 규정과 가격 정책을 확인해야 합니다. 세부적인 정보나 업데이트는 OpenAI의 공식 문서나 웹사이트를 참고하는 것이 좋습니다.
