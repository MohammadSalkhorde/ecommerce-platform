from django.shortcuts import render,get_object_or_404,redirect
from .forms import CommentForm
from .models import Comment,Scoring,Favorite
from django.views import View
from apps.products.models import Product
from django.contrib import messages
from django.http import JsonResponse,HttpResponse
from django.db.models import Q
#-------------------------------------------------------------------------
class CommentView(View):
    def get(self,request,*args, **kwargs):
        productId=request.GET.get('productId')
        commentId=request.GET.get('commentId')
        slug=kwargs['slug']
        initial_dict={
            'product_id': productId,
            'comment_id': commentId,
        }
        form=CommentForm(initial=initial_dict)
        
        return render(request,'csf/partials/create_comment.html',{'form':form,'slug':slug,'comment_id':commentId})
    
    def post(self,request,*args, **kwargs):
        slug=kwargs['slug']
        form=CommentForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            product=get_object_or_404(Product,slug=slug)
            parent=None
            if (cd['comment_id']):
                parentId=cd['comment_id']
                parent=Comment.objects.get(id=parentId)
            
            Comment.objects.create(
                product=product,
                commenting_user=request.user,
                comment_text=cd['comment_text'],
                comment_parent=parent
            )
            
            messages.success(request,'نظر شما با موفقیت ثبت شد')
            return redirect('products:product_detail',product.slug)
        
        messages.error(request,'خطا در ارسال نظر','danger')
        return redirect('products:product_detail',product.slug)
#-------------------------------------------------------------------------
def add_score(request):
    productId=request.GET.get('productId')
    score=request.GET.get('score')
    
    product=Product.objects.get(id=productId)
    scoring=Scoring.objects.filter(Q(product=product) & Q(scoring_user=request.user))
    if scoring.exists():
        return False
    else:
        Scoring.objects.create(
            product=product,
            scoring_user=request.user,
            score=score
        )
    
    return JsonResponse({"average_score":product.get_average_score()})
#-------------------------------------------------------------------------
def add_to_favorites(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status':'error', 'message':'ابتدا وارد شوید'})

    product_id = request.GET.get('product_id')
    product = Product.objects.get(id=product_id)

    exists = Favorite.objects.filter(
        Q(favorite_user=request.user) & Q(product_id=product_id)
    ).exists()

    if not exists:
        Favorite.objects.create(
            product=product,
            favorite_user=request.user,
        )
        return JsonResponse({'status':'ok'})
    else:
        return JsonResponse({'status':'exists'})
#-------------------------------------------------------------------------
def delete_from_favorite(request,*args, **kwargs):
    p_id=kwargs['p_id']
    if not request.user.is_authenticated:
        return redirect("accounts:login") 

    # product_id = request.GET.get('product_id')
    product = Product.objects.get(id=p_id)

    Favorite.objects.filter(product_id=product, favorite_user=request.user).delete()

    return redirect("csf:user_favorite")

#-------------------------------------------------------------------------
def status_favorites(request):
    if request.user.is_authenticated:
        count = Favorite.objects.filter(favorite_user=request.user).count()
    else:
        count = 0
    return HttpResponse(count)
#-------------------------------------------------------------------------
class UserFavoriteView(View):
    def get(self,request,*args, **kwargs):
        user_favorite=Favorite.objects.filter(Q(favorite_user_id=request.user))
        return render(request,'csf/user_favorite.html',{'user_favorite':user_favorite})
#-------------------------------------------------------------------------