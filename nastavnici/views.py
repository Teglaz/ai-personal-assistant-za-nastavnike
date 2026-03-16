from django.shortcuts import render
from django.http import HttpResponse
import anthropic
import os
from dotenv import load_dotenv

# Učitaj .env fajl
load_dotenv()

# Inicijalizuj Anthropic klijent (čita ANTHROPIC_API_KEY iz okruženja)
client = anthropic.Anthropic()

def home(request):
    return render(request, 'home.html')

def quiz_generator(request):
    if request.method == 'POST':
        tema = request.POST.get('tema')
        razred = request.POST.get('razred')

        try:
            response = client.messages.create(
                model="claude-opus-4-6",
                max_tokens=1000,
                system="Ti si AI asistent za nastavnike. Generiši kviz na srpskom jeziku.",
                messages=[
                    {"role": "user", "content": f"Napravi kviz iz {tema} za {razred}. razred. 5 pitanja sa po 4 odgovora (A, B, C, D). Format: Pitanje, opcije, tačan odgovor."}
                ]
            )

            kviz = response.content[0].text

            return HttpResponse(f"""
            <h1>Generator Kvizova</h1>
            <h2>Kviz iz {tema} za {razred}. razred</h2>
            <pre>{kviz}</pre>
            <br>
            <a href="/kviz/">← Nazad</a>
            """)

        except Exception as e:
            return HttpResponse(f"Greška: {str(e)}")

    return render(request, 'quiz_form.html')

def lesson_planner(request):
    if request.method == 'POST':
        predmet = request.POST.get('predmet')
        tema = request.POST.get('tema')
        razred = request.POST.get('razred')
        tip_casa = request.POST.get('tip_casa')

        try:
            response = client.messages.create(
                model="claude-opus-4-6",
                max_tokens=1500,
                system="Ti si AI asistent za nastavnike. Generiši detaljan plan časa na srpskom jeziku.",
                messages=[
                    {"role": "user", "content": f"Napravi plan časa za {predmet}, tema: {tema}, {razred}. razred osnovne škole. Tip časa: {tip_casa}. Uključi: ciljeve, aktivnosti po fazama časa, materijale i evaluaciju."}
                ]
            )

            plan = response.content[0].text

            return HttpResponse(f"""
            <h1>Plan časa - {tema}</h1>
            <h2>{predmet} - {razred}. razred</h2>
            <pre style="white-space: pre-wrap;">{plan}</pre>
            <br>
            <a href="/nastavnici/plan/">← Nazad</a>
            """)

        except Exception as e:
            return HttpResponse(f"Greška: {str(e)}")

    return render(request, 'lesson_form.html')

def homework_creator(request):
    return render(request, 'homework_form.html')

def osnovna_quiz(request):
    return render(request, 'quiz_form.html')

def osnovna_plan(request):
    return render(request, 'lesson_form.html')

def osnovna_domaci(request):
    return render(request, 'homework_form.html')

def srednja_quiz_form(request):
    if request.method == 'POST':
        tema = request.POST.get('tema')
        razred = request.POST.get('razred')
        tip_skole = request.POST.get('school_type')

        try:
            response = client.messages.create(
                model="claude-opus-4-6",
                max_tokens=1000,
                system="Ti si AI asistent za nastavnike. Generiši kviz na srpskom jeziku.",
                messages=[
                    {"role": "user", "content": f"Napravi kviz iz {tema} za {razred}. razred {tip_skole} srednje škole. 5 pitanja sa po 4 odgovora (A, B, C, D). Format: Pitanje, opcije, tačan odgovor."}
                ]
            )

            kviz = response.content[0].text

            return HttpResponse(f"""
            <h1>Generator Kvizova - Srednja škola</h1>
            <h2>Kviz iz {tema} za {razred}. razred</h2>
            <pre>{kviz}</pre>
            <br>
            <a href="/nastavnici/srednja/kviz/">← Nazad</a>
            """)

        except Exception as e:
            return HttpResponse(f"Greška: {str(e)}")

    return render(request, 'srednja_quiz_form.html')

def srednja_lesson_planner(request):
    if request.method == 'POST':
        predmet = request.POST.get('predmet')
        tema = request.POST.get('tema')
        razred = request.POST.get('razred')
        tip_skole = request.POST.get('tip_skole')

        try:
            response = client.messages.create(
                model="claude-opus-4-6",
                max_tokens=1500,
                system="Ti si AI asistent za nastavnike. Generiši profesionalan plan časa za srednju školu na srpskom jeziku.",
                messages=[
                    {"role": "user", "content": f"Napravi detaljan plan časa za {predmet}, tema: {tema}, {razred}. razred {tip_skole}. Uključi: ishode učenja, metode rada, tok časa po fazama, materijale, i načine evaluacije."}
                ]
            )

            plan = response.content[0].text

            return HttpResponse(f"""
            <h1>Plan časa - Srednja škola</h1>
            <h2>{tema} - {predmet}</h2>
            <h3>{razred}. razred {tip_skole}</h3>
            <pre style="white-space: pre-wrap;">{plan}</pre>
            <br>
            <a href="/nastavnici/srednja/plan/">← Nazad</a>
            """)

        except Exception as e:
            return HttpResponse(f"Greška: {str(e)}")

    return render(request, 'srednja_lesson_form.html')

def srednja_homework_creator(request):
    return render(request, 'homework_form.html')
