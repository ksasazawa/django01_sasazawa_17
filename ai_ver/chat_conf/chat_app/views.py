from django.shortcuts import render, redirect
from .models import Comment
from .forms import CommentForm

from transformers import pipeline 
from transformers import AutoModelForSequenceClassification 
from transformers import BertJapaneseTokenizer 

from decimal import Decimal
from datetime import datetime, date

# パイプラインの準備
model = AutoModelForSequenceClassification.from_pretrained('daigo/bert-base-japanese-sentiment') 
tokenizer = BertJapaneseTokenizer.from_pretrained('cl-tohoku/bert-base-japanese-whole-word-masking') 
nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer) 

flg = 0
cnt = 0

def frontpage(request):
    comments = Comment.objects.all()
    global flg
    global cnt
    if cnt==2:
        flg = 0
        cnt = 0
    # 初期状態は最新のデータを表示
    if comments.count()==0:
        comment = "nothing"
        nlp_label = "わかりません"
        nlp_score = 0
    else:
        comment = comments.latest("data_added")
        nlp_label = list(nlp(str(comment.u1_text)))[0]["label"]
        nlp_score = list(nlp(str(comment.u1_text)))[0]["score"]
        if nlp_label == "ポジティブ":
            nlp_label = "良い調子だね！"
        else:
            nlp_label = "大丈夫？心配、、"
    
    # POSTされていたらそのデータを表示
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            flg = 1 # ポストされたらflgを１に変更
            cnt += 1
            u1_text = form.cleaned_data['u1_text']
            nlp_label = list(nlp(str(u1_text)))[0]["label"]
            if nlp_label == "ポジティブ":
                nlp_label = "良い調子だね！"
            else:
                nlp_label = "大丈夫？心配、、"
            nlp_score = list(nlp(str(u1_text)))[0]["score"]
            print(nlp(str(u1_text)))
            print(list(nlp(str(u1_text)))[0]["score"])
            form = Comment.objects.create(u1_text=u1_text, np_label=nlp_label, np_score=nlp_score)
            return redirect("frontpage")
    else:
        if flg==1 and cnt==1:
            cnt += 1
        form = CommentForm()

    return render(request, "frontpage.html", {"form": form, "nlp_label": nlp_label, "nlp_score": nlp_score, "flg": flg})

def check(request):
    comments = Comment.objects.all()
    sum_score = 0
    np_score = 0
    np_score_cnt = 0 # 今日のデータ数
    for comment in comments:
        print(f"データ日付：{datetime.date(comment.data_added)}/今日の日付：{datetime.date(datetime.now())}")
        # 今日の日付のみ計算対象
        if datetime.date(comment.data_added) == datetime.date(datetime.now()):
            if comment.np_label == "良い調子だね！": # ポジティブなら100-スコア*100
                np_score = 100 - Decimal(str(comment.np_score)) * 100
                print(f"ポジティブスコア：{np_score}")
            elif comment.np_label == "大丈夫？心配、、": # ネガティブならスコア*100
                np_score = Decimal(str(comment.np_score))*100
                print(f"ネガティブスコア：{np_score}")
            sum_score += np_score
            np_score_cnt += 1
            print(f"合計：{sum_score}/個数：{np_score_cnt}")
    score = round(sum_score / np_score_cnt, 2)
    print(f"結果は{score}")
    
    return render(request, "check.html", {"score": score})


