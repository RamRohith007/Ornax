from django.urls import path
from webapp import views

urlpatterns = [
    path("",views.homepage,name="homepage"),
    path("login",views.userlogin,name="login"),
    path("register",views.userregistration,name="register"),
    path("logout",views.userlogout,name="logout"),
    path("productdashboard",views.productdashboard,name="productdashboard"),
    path("addproduct",views.addproduct,name="addproduct"),
    path("updateproduct/<int:pk>",views.updateproduct,name="updateproduct"),
    path("productdetails/<int:pk>",views.productdetails,name="productdetails"),
    path("deleteproduct/<int:pk>",views.deleteproduct,name="deleteproduct"),
    path("productcards",views.product_cards,name="productcards"),
    path("productpage/<int:pk>",views.productpage,name="productpage"),
    ##apis
    path("api/",views.apioverview,name=""),
    path("api/view-products/",views.apiProductsView,name="api-view-products"),
    path("api/view/product-detail/<int:pk>/",views.apiProductDetail,name="api-product-detail"),
    path("api/add-product/",views.apiProductAdd,name="api-add-product"),
    path("api/update-product/<int:pk>/",views.apiProductUpdate,name="api-update-product"),
    path("api/delete-product/<int:pk>/",views.apiProductDelete,name="api-delete-product"),
    ##ReportLab
    path("products-pdf-list/",views.productsListPdf,name="products-pdf-list"),
]
