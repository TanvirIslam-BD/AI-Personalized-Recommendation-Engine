from django.shortcuts import render
from django.http import JsonResponse
from surprise import Dataset, Reader, SVD
from .models import UserRating, Product
import pandas as pd

def train_model():
    ratings = UserRating.objects.all().values("user_id", "product_id", "rating")
    df = pd.DataFrame(list(ratings))
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(df[["user_id", "product_id", "rating"]], reader)
    trainset = data.build_full_trainset()
    model = SVD()
    model.fit(trainset)
    return model

model = train_model()

def recommend(request):
    user_id = int(request.GET.get("user_id"))
    products = Product.objects.all()
    recommendations = []
    for product in products:
        prediction = model.predict(user_id, product.product_id)
        recommendations.append((product.name, prediction.est))
    recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)[:5]
    return JsonResponse({"recommendations": recommendations})

def home(request):
    return render(request, "recommendation/home.html")
