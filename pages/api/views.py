from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from pages.api.serializers import RegistrationSerializer,LoginSerializer
from pages import models
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from .serializers import AccountSerializer,TransactionSerializer,BillPaymentSerializer,StaduimsSerializer,TicketSerializer,LogSerializer
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response 
from social_django.utils import psa 
from requests.exceptions import HTTPError 
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail,EmailMessage
from CashMoney.settings import EMAIL_HOST_USER
from pages.api.tasks import send_notification_mail
#from twilio.rest import Client



@api_view(['POST'])
@permission_classes([AllowAny])
@psa()
def register_by_access_token(request, backend): 
    token = request.data.get('access_token') 
    user = request.backend.do_auth(token) 
    print(request) 
    if user: 
        token, _ = Token.objects.get_or_create(user=user) 
        return Response( 
            { 
                'token': token.key 
            },
            status=status.HTTP_200_OK,
            ) 
    else: 
        return Response( 
                { 
                    'errors': 
                    { 'token':
                    'Invalid token' 
                    } 
                },
                status=status.HTTP_400_BAD_REQUEST, ) 
@api_view(['GET', 'POST'])
def authentication_test(request): 
    print(request.user) 
    return Response( 
        { 
            'message': "User successfully authenticated" 
        },
        status=status.HTTP_200_OK, 
    )
@api_view(['POST',])
@permission_classes([AllowAny])
def registration_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)

        data = {}
        if serializer.is_valid():
            subject = "New Account is created"
            message= 'Dear Freind,Your Account is created'
            account = serializer.save()
            
            user_account =models.Account(user=account,account_balance=0)
            user_account.save() 

            log_entry =models.Log(user=account, log_type='7')
            log_entry.save()
            send_notification_mail(account.email,message)

            data['response'] = "Registration Successful!"
            data['username'] = account.username
            data['email'] = account.email
            token,created = Token.objects.get_or_create(user=account)
            data['token'] = token.key

            #models.Log()
            

       
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data, status=status.HTTP_201_CREATED)

@api_view(['POST',])
def logout_view(request):
    if request.method == 'POST':
        log_entry =models.Log(user=request.user.auth, log_type='8')
        log_entry.save()
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)  # Use your LoginSerializer

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)

            log_entry =models.Log(user=user, log_type='6')
            log_entry.save()

            data = {
                'response': 'Login Successful!',
                'username': user.username,
                'email': user.email,
                'token': token.key,
            }
        else:
            data = serializer.errors

        return Response(data)


# class AccountCreateView(APIView):
#     permission_classes = [IsAuthenticated]  # Requires user authentication

#     def post(self, request):
#         serializer = AccountSerializer(data=request.data)
#         if serializer.is_valid():
#             account = serializer.save() 

#             log_entry =models.Log(user=account, log_type='7')
#             log_entry.save()

#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class AccountDetailView(APIView):
#     permission_classes = [IsAuthenticated]  

#     def get_object(self, account_id):
#         try:
#             return models.Account.objects.get(account_id=account_id)
#         except models.Account.DoesNotExist:
#             raise status.HTTP_404_NOT_FOUND

#     def get(self, request, account_id):
#         account = self.get_object(account_id)
#         serializer = AccountSerializer(account)
#         return Response(serializer.data)

#     def put(self, request, account_id):
#         account = self.get_object(account_id)
#         serializer = AccountSerializer(account, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, account_id):
#         account = self.get_object(account_id)
#         account.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class AccountListView(APIView):
#     permission_classes = [IsAuthenticated, IsAdminUser]  # Requires admin access

#     def get(self, request):
#         accounts = models.Account.objects.all()
#         serializer = AccountSerializer(accounts, many=True)
#         return Response(serializer.data)

class TransactionView(APIView):
    permission_classes = [IsAuthenticated]  

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)

        if serializer.is_valid():
            # Determine the transaction type based on the serializer data
            transaction_type = serializer.validated_data.get('transaction_type')

            if transaction_type == "1":  # Deposit
                serializer.validated_data['sender'] = request.user
                serializer.validated_data['receiver'] = request.user  # Deposits go to the user's own account
                serializer.validated_data['transaction_type'] = '1'  # Deposit
                serializer.validated_data['status'] = '2'  # Completed
                # Update user's account balance
                amount = serializer.validated_data['amount']
                if not amount:
                    return Response({'error': 'Amount is required.'}, status=status.HTTP_400_BAD_REQUEST)
                try:
                    # Retrieve the user's account
                    account = models.Account.objects.get(user=request.user)

                    # Update the account balance by adding the deposit amount
                    account.account_balance += amount
                    account.save()
                    serializer.save()
                    message= 'Dear Freind,Your Transaction is done'
                    send_notification_mail(EMAIL_HOST_USER,message)
                    log_entry =models.Log(user=request.user, log_type='1')
                    log_entry.save()
                
                    return Response({'message': 'Deposit successful', 'new_balance': account.account_balance}, status=status.HTTP_200_OK)

                except models.Account.DoesNotExist:
                        return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)


            elif transaction_type == '2':
                serializer = TransactionSerializer(data=request.data)
                if serializer.is_valid():
                    amount = serializer.validated_data['amount']
                    try:
                        account = models.Account.objects.get(user=request.user)
                        if amount and account.account_balance >= amount :
                            # Set transaction details
                            serializer.validated_data['sender'] = request.user
                            serializer.validated_data['receiver'] = request.user  # Withdrawals are from the user's own account
                            serializer.validated_data['transaction_type'] = '2'  # Withdrawal
                            serializer.validated_data['status'] = '2'  # Completed

                            # Update user's account balance
                            account.account_balance -= amount
                            account.save()

                            # Save the transaction
                            serializer.save()
                            message= 'Dear Freind,Your Transaction is done'
                            send_notification_mail(EMAIL_HOST_USER,message)
                            log_entry =models.Log(user=request.user, log_type='2')
                            log_entry.save()

                            return Response(serializer.data, status=status.HTTP_201_CREATED)
                        else:
                            return Response({'error': 'Insufficient balance.'}, status=status.HTTP_400_BAD_REQUEST)
                    except models.Account.DoesNotExist:
                        return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            elif transaction_type == '3':  
                serializer = TransactionSerializer(data=request.data)

                if serializer.is_valid():
                    sender = models.Account.objects.get(user=request.user)
                    receiver_username = request.data.get('receiver_username', None)
                    if receiver_username is None:
                        return Response({'receiver_username': 'Receiver username is required.'}, status=status.HTTP_400_BAD_REQUEST)
                    amount = serializer.validated_data['amount']

                    try:
                        receiver = User.objects.get(username=receiver_username)
                    except User.DoesNotExist:
                        return Response({'error': 'Receiver not found.'}, status=status.HTTP_400_BAD_REQUEST)

                    if sender != receiver:
                        if sender.account_balance >= amount:
                            # Set transaction details
                            serializer.validated_data['sender'] = request.user
                            serializer.validated_data['receiver'] = receiver
                            serializer.validated_data['transaction_type'] = '3'  # Money Transfer
                            serializer.validated_data['status'] = '2'  # Completed
                            sender_account = models.Account.objects.get(user__username = request.user.username)
                            receiver_account = models.Account.objects.get(user__username = receiver.username)
                            # Update sender's and receiver's account balances
                            message= 'Dear Freind,Your Transaction is done'
                            send_notification_mail(EMAIL_HOST_USER,message)                            
                            sender_account.account_balance -= amount
                            receiver_account.account_balance += amount
                            sender_account.save()
                            receiver_account.save()

                            log_entry =models.Log(user=request.user, log_type='3')
                            log_entry.save()
                            # Save the transaction
                            serializer.save()

                            return Response(serializer.data, status=status.HTTP_201_CREATED)
                        else:
                            return Response({'error': 'Insufficient balance.'}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'error': 'You cannot transfer money to yourself.'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'message': 'Invalid transaction type'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BillPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Retrieve the payment history for the authenticated user
        payments =models.BillPayment.objects.filter(user=request.user)
        serializer = BillPaymentSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Create a new bill payment record
        serializer = BillPaymentSerializer(data=request.data)
        
        if serializer.is_valid():
            # Set the user to the authenticated user
            serializer.validated_data['user'] = request.user
            account_user = models.Account.objects.get(user=request.user)
            if account_user.account_balance >= serializer.validated_data['bill_amount']:
                serializer.validated_data['payment_status'] = '2'  # Completed
                account_user.account_balance -= serializer.validated_data['bill_amount']
                account_user.save()

                serializer.save()

                log_entry =models.Log(user=request.user, log_type='4')
                log_entry.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StaduimsView(APIView):
    permission_classes=[(AllowAny)]
    def get(self, request):
        # Retrieve all stadiums
        stadiums = models.Staduims.objects.all()
        serializer = StaduimsSerializer(stadiums, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
     
class TicketView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            stadium_name = request.data.get('Stauim_name')
            try:
            # Retrieve the stadium object based on the stadium name
                stadium = models.Staduims.objects.get(Staduim_name=stadium_name)
            except models.Staduims.DoesNotExist:
                return Response({'error': 'Stadium not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer.validated_data['user'] = request.user
            ticket_price = stadium.Ticket_Price
            account_user = models.Account.objects.get(user=request.user)
            if account_user.account_balance >= ticket_price:
                serializer.validated_data['status'] = '2'  # Completed
                account_user.account_balance -= ticket_price
                account_user.save()

                serializer.save()

                log_entry =models.Log(user=request.user, log_type='5')
                log_entry.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        # Retrieve all tickets
        tickets = models.Ticket.objects.all()
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        logs = models.Log.objects.filter(user=request.user)
        serializer = LogSerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
