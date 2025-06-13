from django.contrib.auth.models import User
from django.shortcuts import render
import json
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.db import connection, transaction
from django.db import IntegrityError
from django.http import JsonResponse
from decouple import config
import requests
import openai

@csrf_exempt
def chat_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        prompt = data.get('prompt')
        
        response_text = generate_text(prompt)
        print(prompt)
        return JsonResponse({
            'response': 'response_text'
        })
    else:
        return HttpResponse("NOTOK")


def generate_text(prompt):
    openai.api_key = ' '

    response = requests.post(
     "https://api.openai.com/v1/chat/completions",
     headers={"Authorization": f"Bearer {openai.api_key}"},
     json={"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": f'{prompt}'}], "temperature": 0.1},
 )
    #print(response.json())
    return response.json()

def home_view(request):
    return render(request, 'home.html')

@csrf_exempt
def level_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        level = data.get('level')
        with connection.cursor() as cursor:
            query = "SELECT * FROM problem WHERE level=%s"
            cursor.execute(query, [level])
            problems = cursor.fetchall()
           # print('levels: ',problems)
        if problems:
            fields = ['level','p_id','prob_name', 'prob_desc', 'percent', 'prob_input','prob_output']
            problem_list = [dict(zip(fields,problem)) for problem in problems]
            return JsonResponse(problem_list, safe=False)
            
    else:
        return HttpResponse("Method Not Allowed1", status=405)

@csrf_exempt
def prob_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        p_id = data.get('p_id')
        with connection.cursor() as cursor:
            query = "SELECT * FROM problem WHERE p_id=%s"
            cursor.execute(query, [p_id])
            problems = cursor.fetchall()
           # print('problems: ',problems)
        if p_id:
            if problems:
                fields = ['level', 'p_id', 'prob_name', 'prob_desc', 'percent', 'prob_input', 'prob_output']
                problem_dict = dict(zip(fields, problems[0]))  # 가정: p_id는 unique하므로, 첫 번째 결과만 가져옵니다.
                print(problem_dict)
                cursor.close()
                return JsonResponse(problem_dict, safe=False)
            else:
                cursor.close()
                return JsonResponse({"error": "Problem with id {} not found.".format(p_id)}, status=404)
    else:
        return HttpResponse("Method Not Allowed", status=405)
    
@csrf_exempt
def rank_view(request):
    if request.method == "GET":
        with connection.cursor() as cursor:
            query = "SELECT username, university, point FROM Users ORDER BY point DESC"
            cursor.execute(query)
            users = cursor.fetchall()
            if users:
                fields = ['username', 'university', 'point']
                users_dict = [dict(zip(fields, user)) for user in users]
                print(users_dict)
                return JsonResponse(users_dict, safe=False)
            else:
                return JsonResponse({"status": "error","message": "fail"})
        
    else:
        return HttpResponse("Method Not Allowed", status=405) 
        
    
# @csrf_exempt
# def checkwrong_view(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         print('data: ',data)
#         id = data.get('id')
#         p_id = data.get('p_id')
#         with connection.cursor() as cursor:
#             query = "SELECT answer from try WHERE id=%s AND p_id=%s"
#             cursor.execute(query, [id, p_id])
#             answer = cursor.fetchall()
#             print('answer: ',answer)
            
#             return JsonResponse({"status": "success","message": answer})
#     else:
#         return HttpResponse("Method Not Allowed", status=405)
   
@csrf_exempt
def wrong_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        id = data.get('id')
        print(request.body)
        with connection.cursor() as cursor:
            query = "SELECT level, try.p_id, prob_name,prob_desc, percent FROM try JOIN problem ON try.p_id=problem.p_id WHERE correct='false' AND id=%s"
            
            cursor.execute(query, [id])
            w_problems = cursor.fetchall()
            print(w_problems)
            if w_problems:
                fields = ['level', 'p_id', 'prob_name', 'prob_desc', 'percent']
                problem_dicts = [dict(zip(fields, problem)) for problem in w_problems]    
                print(problem_dicts)
                return JsonResponse(problem_dicts, safe=False)
            else:
                return JsonResponse({"error": "Problem with id {} not found.".format(id)}, status=404)
    else:
        return HttpResponse("Method Not Allowed", status=405)
        

@csrf_exempt
def submit_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        answer = data.get('answer')
        p_id = data.get('p_id')
        id = data.get('id')
        type = data.get('type') #submit, refactoring, hint
        
        with connection.cursor() as cursor:
            query = "SELECT * FROM problem WHERE p_id=%s"
            cursor.execute(query, [p_id])
            result = cursor.fetchall()
            
            if type=='submit':
                # Few-shot prompting + Chain-of-thought + Output formatting
                prompt = f"""
당신은 코딩 문제 채점 전문가입니다. 다음 단계를 따라 코드를 평가하세요:

## 문제:
{result[0][3]}

## 제출된 코드:
```
{answer}
```

## 평가 과정:
1. 코드 로직 분석
2. 예상 입출력 검증
3. 엣지 케이스 고려
4. 최종 판정

## 출력 형식 (반드시 준수):
정답: [True/False]
근거: [간단한 이유]

예시:
정답: True
근거: 모든 테스트 케이스 통과
"""
                res = generate_text(prompt)
                content_value = res['choices'][0]['message']['content']
                print('submit: ', content_value)
                if (content_value.find('True')!=-1):      
                    try:
                        with transaction.atomic():
                            #cursor.execute("INSERT INTO try (p_id, id, correct, answer) VALUES (%s, %s, %s, %s)", [p_id, id, 'true', answer])
                            #_query = "UPDATE Users set point = point+10 WHERE id=%s"
                            #cursor.execute(_query, [id])
                            cursor.execute("INSERT INTO try (id, p_id, correct, answer) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE answer = VALUES(answer), correct = VALUES(correct)", [id, p_id, 'true', answer])
                        return JsonResponse({"status": "success","message": "success"})
                    except Exception as e:
                        return JsonResponse({"status": "error", "message": str(e)})
    
                else:
                    #try테이블에 insert
                    try:
                        with transaction.atomic():
                            cursor.execute("INSERT INTO try (id, p_id, correct, answer) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE answer = VALUES(answer), correct = VALUES(correct)", [id, p_id, 'false', answer])
                        return JsonResponse({"status": "error","message": "fail"})
                    except Exception as e:
                        return JsonResponse({"status": "error", "message": str(e)})
                
            elif type=='refactoring':
                # Role-based prompting + Step-by-step instruction
                prompt = f"""
당신은 시니어 소프트웨어 엔지니어입니다. 다음 코드를 개선해주세요:

## 원본 문제:
{result[0][3]}

## 현재 코드:
```
{answer}
```

## 리팩토링 요구사항:
1. 시간복잡도 최적화
2. 코드 가독성 향상
3. 메모리 효율성 개선
4. 에러 처리 강화

## 출력 형식:
```
[개선된 코드]
```

개선사항:
- [변경점 1]
- [변경점 2]
"""
                res = generate_text(prompt)
                content_value = res['choices'][0]['message']['content']
                print('refactoring: ', content_value)
                return JsonResponse({"status": "success","content": content_value})
                
            else: #hint
                # Constraint-based prompting + Scaffolding
                prompt = f"""
당신은 친절한 튜터입니다. 학생의 코드를 분석하고 힌트를 제공하세요:

## 문제:
{result[0][3]}

## 학생 코드:
```
{answer}
```

## 분석 단계:
1. 코드 의도 파악
2. 오류 지점 식별
3. 학습 방향 제시

## 힌트 제공 (30자 이내, 직접적인 답 금지):
힌트: [구체적이고 건설적인 조언]

예시 형식:
힌트: 반복문 종료 조건을 다시 확인해보세요
"""
                res = generate_text(prompt)
                content_value = res['choices'][0]['message']['content']
                print('hint: ', content_value)
                return JsonResponse({"status": "success","content": content_value})

    else:
        return HttpResponse("Method Not Allowed", status=405)    
            

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_id = data.get('id')
        password = data.get('password')
        print('data',data)
        with connection.cursor() as cursor:
            query = "SELECT * FROM Users WHERE id=%s AND password=%s"
            cursor.execute(query, [user_id, password])
            user = cursor.fetchall()
            print('user',user)
        if user:
            print(1)
            return JsonResponse({"status": "success", "message": "login successful"})
        else:
            print(2)
            return JsonResponse({"status": "error", "message": "login failed, please check your username and password"})
    else:
        print(3)
        return HttpResponse("NOTOK")
    
@csrf_exempt
def signup_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
       # print(data)
        name = data.get('username')
        user_id = data.get('id')
        password = data.get('password')
        weak = data.get('weak_algorithm')
        university = data.get('university')

        with connection.cursor() as cursor:
            # Check if the user_id already exists
            cursor.execute("SELECT * FROM Users WHERE id=%s", [user_id])
            existing_user = cursor.fetchone()
            print(existing_user)
            if existing_user: 
                return JsonResponse({"status": "error", "message": "User ID already exists"})

            # If not, insert the new user
            try:
                cursor.execute(
                    "INSERT INTO Users (username, id, password, university) VALUES (%s, %s, %s, %s)",
                    [name, user_id, password, university]
                )
                return JsonResponse({"status": "success", "message": "User registered successfully"})

            except IntegrityError:
                return JsonResponse({"status": "error", "message": "An error occurred while registering the user"})

    else:
        return HttpResponse("Method Not Allowed", status=405)

def logout_view(request):
    logout(request)
    return redirect('login')
