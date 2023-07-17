from django.contrib.auth.models import User
from django.shortcuts import render
import json
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
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
    openai.api_key = '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'

    response = requests.post(
     "https://api.openai.com/v1/chat/completions",
     headers={"Authorization": f"Bearer {openai.api_key}"},
     json={"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": f'{prompt}'}]},
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
        print('level: ',level)
        with connection.cursor() as cursor:
            query = "SELECT * FROM problem WHERE level=%s"
            cursor.execute(query, [level])
            problems = cursor.fetchall()
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
        p_id = data.get('p_id')  # pid를 p_id로 변경했습니다.
        print('p_id: ', p_id)
        with connection.cursor() as cursor:
            query = "SELECT * FROM problem WHERE p_id=%s"
            cursor.execute(query, [p_id])
            problems = cursor.fetchall()
        if p_id:
            if problems:
                fields = ['level', 'p_id', 'prob_name', 'prob_desc', 'percent', 'prob_input', 'prob_output']
                problem_dict = dict(zip(fields, problems[0]))  # 가정: p_id는 unique하므로, 첫 번째 결과만 가져옵니다.
                return JsonResponse(problem_dict, safe=False)
            else:
                return JsonResponse({"error": "Problem with id {} not found.".format(p_id)}, status=404)
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
                prompt = '문제는 다음과 같아.'+result[0][3]+'다음은 내가 작성한 코드야.'+answer+'이 코드가 정답이면 True, 정답이 아니면 False로만 대답해줘.'
                res = generate_text(prompt)
                content_value = res['choices'][0]['message']['content']
                print('submit: ', content_value)
                if (content_value.find('True')!=-1):
                    return JsonResponse({"status": "success","message": "success"})
                else:
                    return JsonResponse({"status": "error", "message": "fail"})
                
            elif type=='refactoring':
                prompt = '문제는 다음과 같아.'+result[0][3]+'다음은 내가 작성한 코드야.'+answer+'이 코드를 refactoring하거나 최적화된 방법이 있다면 그 방법을 사용해서 코드를 다시 재 작성해줘.'
                res = generate_text(prompt)
                content_value = res['choices'][0]['message']['content']
                print('refactoring: ', content_value)
                return JsonResponse({"status": "success","content": content_value})
                
            else: #hint
                prompt = '문제는 다음과 같아.'+result[0][3]+'다음은 내가 작성한 코드야.'+answer+'이 코드가 정답이 아니면 어떻게 고쳐야 하는지 말로 hint만 알려주고, 풀이 코드는 절대 작성해서 보내지마.'
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


# @csrf_exempt
# def login_view(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         username = data.get("username")
#         password = data.get('password')
#         return HttpResponse(f"{username} {password}")
#     else:
#         return HttpResponse("not ok")

    # if request.method == "POST":
    #     username = request.POST['username']
    #     password = request.POST['password']
    #     user = authenticate(request, username=username, password=password)

    #     if user is not None:
    #         login(request, user)
    #         return JsonResponse({"status": "success", "message": "login successful"})
    #     else:
    #         return JsonResponse({"status": "error", "message": "login failed, please check your username and password"})
    # else:
    #     return JsonResponse({"status": "error", "message": "Invalid request method"})

def logout_view(request):
    logout(request)
    return redirect('login')