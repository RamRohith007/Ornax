from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import UserCreationForm, UserLoginForm, ProductEntryForm, ProductUpdateForm
from django.contrib import messages
##for api
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer
##for ReportLab
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Create your views here.
def homepage(request):
    topproducts = Product.objects.all()
    products = {'products':topproducts}
    return render(request,'webapp/index.html',context=products)
    # return render(request,"webapp/index.html")

# --UserRegistration
def userregistration(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    formvalue = {'registrationform':form}
    return render(request,"webapp/register.html",context=formvalue)

# --UserLogin
def userlogin(request):
    form = UserLoginForm()
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username,password=password)
            if user is not None:
                auth.login(request,user)
                return redirect("homepage")
    formvalue = {'loginform':form}
    return render(request,"webapp/login.html",context=formvalue)        

# --UserLogout
def userlogout(request):
    auth.logout(request)
    return redirect("homepage")


## --Admin/Seller Level
# --Product's Dashboard
@login_required(login_url='login')
def productdashboard(request):
    all_products = Product.objects.all()
    products = {'products':all_products}
    return render(request,'webapp/productdashboard.html',context=products)

# --ProductEntry
@login_required(login_url="login")
def addproduct(request):
    form = ProductEntryForm()
    if request.method == "POST":
        form = ProductEntryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Your product is added!")
            return redirect("productdashboard")
    formvalue = {'addproductform':form}
    return render(request,'webapp/addproduct.html',context=formvalue)

# --ProductUpdate
@login_required(login_url='login')
def updateproduct(request,pk):
    product = Product.objects.get(id=pk)
    form = ProductUpdateForm(instance=product)
    if request.method == "POST":
        form = ProductUpdateForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            messages.success(request,"Your product details are updated!")
            return redirect("productdashboard")
    formvalue = {'updateproductform':form}
    return render(request,'webapp/updateproduct.html',context=formvalue)

# --ProductDetails
@login_required(login_url='login')
def productdetails(request,pk):
    product = Product.objects.get(id=pk)
    formvalue = {'product':product}
    return render(request,"webapp/productdetails.html",context=formvalue)

@login_required(login_url='login')
def deleteproduct(request,pk):
    product = Product.objects.get(id=pk)
    product.delete()
    messages.success(request,"Your product was deleted!")
    return redirect("productdashboard")



##Code    
def product_cards(request):
    all_products = Product.objects.all()
    products = {'products':all_products}
    return render(request,'webapp/productcards.html',context=products)

#Code    
def productpage(request,pk):
    product = Product.objects.get(id=pk)
    formvalue = {'product':product}
    return render(request,"webapp/productpage.html",context=formvalue)



##Django REST Api
@api_view(['GET'])
def apioverview(request):
    api_urls = {
        'View all Products':'/api/view-products/',
        'Detail View' : '/api/view/product-detail/<int:pk>/',
        'Add' : '/api/add-product/',
        'Update' : '/api/update-product/<int:pk>/',
        'Delete' : '/api/delete-product/<int:pk>/'
    }
    return Response(api_urls)

@api_view(['GET'])
def apiProductsView(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def apiProductDetail(request,pk):
    products = Product.objects.get(id=pk)
    serializer = ProductSerializer(products, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def apiProductAdd(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['GET','POST'])
def apiProductUpdate(request,pk):
    product = Product.objects.get(id=pk)
    serializer = ProductSerializer(instance=product, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def apiProductDelete(request,pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return Response("Item deleted successfully")



##Report lab PDF

def productsListPdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter,bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont('Helvetica', 14)

    products = Product.objects.all()

    lines=[]

    for product in products:
        lines.append(str(product.product_id))
        lines.append(product.product_name)
        lines.append(product.product_brand)
        lines.append(str(product.product_mfg_year))
        lines.append(str(product.product_stock))
        lines.append(str(product.product_price))
        lines.append(product.product_description)
        lines.append("---------------------------------------------")

    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename="productlist.pdf")