from django.urls import path,re_path
from rest_framework.authtoken.views import obtain_auth_token
#from . import views
from pages.api.views import registration_view, logout_view,login_view,TransactionView,BillPaymentView,StaduimsView,LogView


urlpatterns = [
    path('login', login_view, name='login'),
    path('register', registration_view, name='register'),
    path('logout', logout_view, name='logout'),
    # path('accountcreate', AccountCreateView.as_view(), name='account-create'),
    # path('accounts/<int:account_id>', AccountDetailView.as_view(), name='account-detail'),
    # path('accountlist', AccountListView.as_view(), name='account-list'),
    path('TransactionView', TransactionView.as_view(), name='account-list'),
    path('billpayments', BillPaymentView.as_view(), name='billpayment-list'),
    path('staduims', StaduimsView.as_view(), name='staduims-list'),
    path('Logs', LogView.as_view(), name='LogUser'),
    #re_path('register-by-access-token/'+r'social/(?P<backend>[^/]+)/$',views.register_by_access_token),
    #path('authentication-test',views.authentication_test),




    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]