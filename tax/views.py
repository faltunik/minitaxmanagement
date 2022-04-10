
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from datetime import datetime


# app import
from .serializer import *
from users.utils import *
from users.models import User



# permission to see post
def has_permission(request, obj):
    if request.user == obj.tax_payer or request.user == obj.tax_accountant or request.user.is_admin:
        return True
    return False


# now we need to create views for
# creating tax
# listing tax based on filters based on status, update and creation
# seeing individual tax and history
# updating tax


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsTaxAccountant])
def create_tax(request, *args, **kwargs):
    tax_payer = User.taxpayermanager.filter(username = request.data.get('tax_payer')).first()
    if tax_payer:
        serializer = TaxSerializers(data=request.data)
        if serializer.is_valid():
            tax = serializer.save(tax_payer = tax_payer, tax_accountant = request.user)
            print('Tax is', tax)
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'detail': 'Tax payer is not found'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrTaxAccountant])
def list_tax(request, *args, **kwargs):
    tax_accountant = request.user
    tax_payer_name = request.GET.get('tax_payer')
    print('tax_payer :', tax_payer_name)
    tax_status = request.GET.get('status')
    print('tax_status :', tax_status)
    update_date = request.GET.get('update_date')
    print('update_date :', update_date)
    create_date = request.GET.get('create_date')
    print('create_date :', create_date)
    tax_accountant_name = request.GET.get('tax_accountant')
    print('tax_accountant_name :', tax_accountant_name)
    tax_accountant = User.objects.filter(username = tax_accountant_name).first()
    tax_payer = User.objects.filter(username = tax_payer_name).first()
    tax_list = Tax.objects.all()
    print('tax payer is :', tax_payer)
    if tax_payer != None:
        tax_list = tax_list.filter(tax_payer = tax_payer)
        print('tax_list is :', tax_list)

    print('tax_status is :', tax_status)
    if tax_status:
        tax_list = tax_list.filter(status = tax_status)
        print('tax_list is :', tax_list)

    print('tax_accountant is :', tax_accountant)
    if tax_accountant:
        tax_list = tax_list.filter(tax_accountant = tax_accountant)
        print('tax_list is :', tax_list)

    print('update_date is :', update_date)
    if update_date:
        tax_list = tax_list.filter(updated_at__gt = update_date)
        print('tax_list is :', tax_list)

    print('create_date is :', create_date)
    if create_date:
        tax_list = tax_list.filter(created_at__gt = create_date)
        print('tax_list is :', tax_list)

    serializer = TaxSerializers(tax_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# viewing individual tax
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_tax(request, id, *args, **kwargs):
    tax = Tax.objects.filter(id = id).first()
    if tax:
        if has_permission(request, tax):     
            serializer = TaxSerializers(tax)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': 'You are not allowed to view this tax'}, status=status.HTTP_403_FORBIDDEN)
    return Response({'detail': 'Tax is not found'}, status=status.HTTP_400_BAD_REQUEST)


# updating tax
@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsTaxAccountant])
def update_tax(request, id, *args, **kwargs):
    print('requesting user is:  ', request.user)
    tax = Tax.objects.filter(id = id).first()
    #tax_payer = User.taxpayermanager.filter(username = request.data.get('tax_payer')).first()
    tax_accountant = User.taxaccountantmanager.filter(username = request.user).first()
    if tax:
        print('request- tax_accountant:  ', tax_accountant)
        print('tax orginal:  ', tax.tax_accountant)
        if tax_accountant == tax.tax_accountant and tax.payment_status != True:
            serializer = TaxSerializers(tax, data=request.data, partial=True)
            if serializer.is_valid():                
                tax = serializer.save(tax_accountant = request.user, updated_at = datetime.now())
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'You are not allowed to update this tax'}, status=status.HTTP_403_FORBIDDEN)
    return Response({'detail': 'Tax or Tax Payer is not found'}, status=status.HTTP_400_BAD_REQUEST)

# pay tax:
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsTaxPayer])
def tax_payment(request, id, *args, **kwargs):
    """
    Payment for tax, only for tax-payer. From point 2.
    """
    user = request.user
    data = request.data
    try:
        tax = Tax.objects.get(pk=id)
    except Exception as e:
        message = {'detail': 'Tax with id not found.'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    if tax.tax_payer == user:
        serializers = TaxPaymentSerializers(data)
        if (serializers.data.get('payment') == tax.total_amount or tax.total_amount == 0) and tax.status != 'PAID':
            tax.payment()
            message = {
                'message': f'Payment of Rs. {tax.total_amount} is success.'}
            return Response(message, status=status.HTTP_204_NO_CONTENT)
        else:
            message = {'message': f'Amount to be paid Rs.{tax.total_amount}'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    else:
        message = {'detail': 'Tax with id not for current user.'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrTaxAccountant])
def tax_history(request, id, *args, **kwargs):
    """
    Get record for tax history or changes, only for admin and tax-accountant. From point 2.
    """
    user = request.user
    tax = Tax.objects.get(pk=id)
    try:
        if user.user_type == 'admin' or user.user_type == 'tax-accountant':
            if user.user_type == 'tax-accountant' and user == tax.tax_accountant:
                tax_hist = TaxHistorySerializers(tax)
                return Response(tax_hist.data, status= status.HTTP_200_OK)
            elif user.user_type == 'admin':
                tax_hist = TaxHistorySerializers(tax)
                return Response(tax_hist.data, status= status.HTTP_200_OK)
        else:
            return Response(
                'User of tax-payer type not allowed.',
                status= status.HTTP_401_UNAUTHORIZED
            )
    except Exception as e:
        message = {'detail': 'Tax with id not found.'}
        return Response(message, status= status.HTTP_400_BAD_REQUEST)




