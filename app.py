import os
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Fanlar va darajalar bo'yicha 10 tadan savollar bazasi
QUESTIONS_DATA = {
    "english": {
        "easy": [
            {"id": 1, "question": "'Book' so'zining o'zbekcha tarjimasi nima?", "options": ["Kitob", "Daftar", "Qalam", "Stol"], "answer": "Kitob"},
            {"id": 2, "question": "'Apple' so'zi nimani anglatadi?", "options": ["Olma", "Nok", "Uzum", "Banan"], "answer": "Olma"},
            {"id": 3, "question": "'I ___ a student.' Bo'sh joyni to'ldiring.", "options": ["am", "is", "are", "be"], "answer": "am"},
            {"id": 4, "question": "'Cat' nima?", "options": ["Kuchuk", "Mushuk", "Sichqon", "Qush"], "answer": "Mushuk"},
            {"id": 5, "question": "'Red' qaysi rang?", "options": ["Qizil", "Ko'k", "Yashil", "Sariq"], "answer": "Qizil"},
            {"id": 6, "question": "'Good morning' nima degani?", "options": ["Xayrli tong", "Xayrli kun", "Xayrli tun", "Kechirasiz"], "answer": "Xayrli tong"},
            {"id": 7, "question": "'Thank you' tarjimasi?", "options": ["Rahmat", "Iltimos", "Mayli", "Xayr"], "answer": "Rahmat"},
            {"id": 8, "question": "Qaysi biri ko'plik shakli?", "options": ["Cats", "Cat", "a Cat", "One cat"], "answer": "Cats"},
            {"id": 9, "question": "'Sun' nimani anglatadi?", "options": ["Oltin", "Quyosh", "Oydin", "Yulduz"], "answer": "Quyosh"},
            {"id": 10, "question": "'Water' so'zining ma'nosi?", "options": ["Suv", "Sut", "Choy", "Sharbat"], "answer": "Suv"}
        ],
        "medium": [
            {"id": 1, "question": "Past Simple fe'li: 'Go' fe'lining o'tgan zamon shakli?", "options": ["Goed", "Went", "Gone", "Going"], "answer": "Went"},
            {"id": 2, "question": "'She ___ to school every day.'", "options": ["go", "goes", "went", "going"], "answer": "goes"},
            {"id": 3, "question": "'Beautiful' so'zining antonimi nima?", "options": ["Ugly", "Pretty", "Nice", "Smart"], "answer": "Ugly"},
            {"id": 4, "question": "'Always' so'zining tarjimasi?", "options": ["Har doim", "Ba'zan", "Hech qachon", "Tez-tez"], "answer": "Har doim"},
            {"id": 5, "question": "Plural of 'Child'?", "options": ["Childs", "Children", "Childrens", "Childes"], "answer": "Children"},
            {"id": 6, "question": "'Fast' so'zining sinonimi?", "options": ["Quick", "Slow", "Heavy", "Hard"], "answer": "Quick"},
            {"id": 7, "question": "Qaysi biri predlog (preposition)?", "options": ["In", "Run", "Big", "And"], "answer": "In"},
            {"id": 8, "question": "'He is interested ___ music.'", "options": ["in", "on", "at", "for"], "answer": "in"},
            {"id": 9, "question": "'Buy' fe'lining o'tgan zamoni?", "options": ["Bought", "Buyd", "Bring", "Boughted"], "answer": "Bought"},
            {"id": 10, "question": "'Cold' so'zining qarama-qarshisi?", "options": ["Hot", "Warm", "Ice", "Cool"], "answer": "Hot"}
        ],
        "hard": [
            {"id": 1, "question": "If I ___ rich, I would buy a house.", "options": ["was", "were", "am", "been"], "answer": "were"},
            {"id": 2, "question": "By the time we arrived, the movie ___.", "options": ["started", "has started", "had started", "will start"], "answer": "had started"},
            {"id": 3, "question": "Choose the correct passive voice: 'They built this bridge.'", "options": ["This bridge was built", "This bridge is built", "This bridge built", "This bridge has built"], "answer": "This bridge was built"},
            {"id": 4, "question": "What is the idiom 'Piece of cake'?", "options": ["Juda oson ish", "Shirinlik yemak", "Qiyin vazifa", "Pishiriq retsepti"], "answer": "Juda oson ish"},
            {"id": 5, "question": "Which word is an adverb?", "options": ["Quickly", "Quick", "Quickness", "Quicker"], "answer": "Quickly"},
            {"id": 6, "question": "He insisted ___ paying the bill.", "options": ["on", "in", "at", "to"], "answer": "on"},
            {"id": 7, "question": "'Despite' so'zidan keyin nima ishlatilmaydi?", "options": ["of", "noun", "gerund", "the fact"], "answer": "of"},
            {"id": 8, "question": "Neither my friend nor I ___ going to the party.", "options": ["am", "are", "is", "were"], "answer": "am"},
            {"id": 9, "question": "'Scarcely had I entered the room ___ the phone rang.'", "options": ["when", "than", "that", "then"], "answer": "when"},
            {"id": 10, "question": "What is the synonym of 'Meticulous'?", "options": ["Careful", "Careless", "Lazy", "Rude"], "answer": "Careful"}
        ]
    },
    "math": {
        "easy": [
            {"id": 1, "question": "15 + 27 nechaga teng?", "options": ["42", "40", "44", "38"], "answer": "42"},
            {"id": 2, "question": "8 x 7 ko'paytmasi nechiga teng?", "options": ["56", "54", "64", "48"], "answer": "56"},
            {"id": 3, "question": "100 - 45 ayirmani toping.", "options": ["55", "65", "45", "50"], "answer": "55"},
            {"id": 4, "question": "Kvadratning necha tomoni bor?", "options": ["4", "3", "5", "6"], "answer": "4"},
            {"id": 5, "question": "36 : 4 bo'linma nechiga teng?", "options": ["9", "8", "7", "6"], "answer": "9"},
            {"id": 6, "question": "Eng kichik juft son qaysi?", "options": ["2", "0", "1", "4"], "answer": "2"},
            {"id": 7, "question": "15 ning yarmi nechaga teng?", "options": ["7.5", "7", "8", "6.5"], "answer": "7.5"},
            {"id": 8, "question": r"5 ning kvadrati ($5^2$) nechaga teng?", "options": ["25", "10", "15", "20"], "answer": "25"},
            {"id": 9, "question": "100 metr necha santimetr?", "options": ["10000", "1000", "100", "10"], "answer": "10000"},
            {"id": 10, "question": "3 x 0 + 5 javobi nechiga teng?", "options": ["5", "0", "3", "8"], "answer": "5"}
        ],
        "medium": [
            {"id": 1, "question": "Tenglamani yeching: 2x + 10 = 20. x = ?", "options": ["5", "10", "2", "8"], "answer": "5"},
            {"id": 2, "question": "Uchburchak ichki burchaklari yig'indisi necha daraja?", "options": ["180", "360", "90", "270"], "answer": "180"},
            {"id": 3, "question": r"$\sqrt{144}$ ildizdan nechchi chiqadi?", "options": ["12", "14", "11", "16"], "answer": "12"},
            {"id": 4, "question": "20% ning 150 ga teng qiymatini toping.", "options": ["30", "20", "15", "45"], "answer": "30"},
            {"id": 5, "question": r"2 ning 5-darajasi ($2^5$) nechaga teng?", "options": ["32", "16", "64", "10"], "answer": "32"},
            {"id": 6, "question": r"Aylananing yuzasi formulasi qaysi?", "options": [r"$\pi r^2$", r"$2\pi r$", r"$a^2$", r"$a \cdot b$"], "answer": r"$\pi r^2$"},
            {"id": 7, "question": "15, 20, 25 sonlarining o'rta arifmetigi?", "options": ["20", "18", "22", "15"], "answer": "20"},
            {"id": 8, "question": "Tenglamani yeching: x / 4 = 12.", "options": ["48", "3", "16", "36"], "answer": "48"},
            {"id": 9, "question": "To'g'ri burchak necha daraja bo'ladi?", "options": ["90", "180", "45", "60"], "answer": "90"},
