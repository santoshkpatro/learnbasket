import uuid
import shortuuid
import razorpay
from django.conf import settings
from django.shortcuts import render
from django.db import IntegrityError, Error
from rest_framework import permissions, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from techowiz.models.coupon import Coupon
from techowiz.models.program import Program
from techowiz.models.order import Order
from techowiz.models.program_enrollment import ProgramEnrollment
from techowiz.api.v1.orders.serializers import OrderCreateSerializer, RazorpayPaymentSerializer, OrderSerializer


razorpay_payment_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.user_objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class OrderCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        program_id = request.query_params.get('program_id', None)
        discount = 0
        discount_coupon = None

        if not program_id:
            return Response(data={'detail': 'Program id not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            program = Program.available_objects.get(pk=program_id)
            
            # Check for coupon code
            coupon_code = request.query_params.get('coupon_code', None)
            if coupon_code:
                try:
                    coupon = Coupon.active_objects.get(coupon_code=coupon_code)
                    
                    # Checking for coupon code
                    if coupon.programs:
                        if not program in coupon.programs.all():
                            return Response(data={'detail': 'Invalid coupon code'}, status=status.HTTP_403_FORBIDDEN)

                    discount = float(coupon.discount_percentage) * 0.01 * float(program.price)
                    discount_coupon = coupon
                except Coupon.DoesNotExist:
                    return Response(data={'detail': 'Coupon code is invalid'}, status=status.HTTP_404_NOT_FOUND)

            DATA = {
                "amount": (float(program.price) - discount) * 100,
                "currency": "INR",
                "receipt": f"{uuid.uuid4().hex}"
            }

            exiting_enrollment = ProgramEnrollment.objects.get(user=request.user, program=program)
            if exiting_enrollment:
                return Response(data={'detail': 'User already enrolled'}, status=status.HTTP_403_FORBIDDEN)
            
            payment_order = razorpay_payment_client.order.create(data=DATA)
            order = Order(
                order_id=shortuuid.ShortUUID().random(length=10).upper(),
                program=program,
                user=request.user,
                price=float(program.price),
                amount=float(program.price) - discount,
                discount=discount,
                coupon=discount_coupon,
                transaction_id=uuid.uuid4().hex,
                payment_id=payment_order['id']
            )
            order.save()
            serializer = OrderCreateSerializer(order)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except Program.DoesNotExist:
            return Response(data={'detail': 'Program not found'}, status=status.HTTP_404_NOT_FOUND)


class OrderProcessView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request, order_id=None):
        if not order_id:
            return Response(data={'detail': 'Order Id missing'}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = RazorpayPaymentSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Verifying payment signature
                razorpay_payment_client.utility.verify_payment_signature(serializer.data)
                
                try:
                    order = Order.objects.get(order_id=order_id, payment_id=serializer.data['razorpay_order_id'])
                    try:
                        ProgramEnrollment.objects.create(user=order.user, program=order.program)
                        order.status = 2
                        order.save()
                        return Response(data={'detail': 'Order processing complete'}, status=status.HTTP_200_OK)
                    except IntegrityError:
                        order.status = 1
                        order.save()
                        return Response(data={'detail': 'User already enrolled'}, status=status.HTTP_202_ACCEPTED)
                    except Error:
                        return Response(data={'detail': 'Error while saving'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except Order.DoesNotExist:
                    return Response(data={'detail': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
            except razorpay.errors.SignatureVerificationError:
                return Response(data={'detail': 'Payment signature error'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Local development payment method
def payment_view(request, order_id=None):
    if not order_id:
        return Response(data={'detail': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    try:
        order = Order.objects.get(order_id=order_id)
        return render(request, 'orders/payment.html', {
            'order': order,
            'razorpay_key_id': settings.RAZORPAY_KEY_ID
        })
    except Order.DoesNotExist:
        return Response(data={'detail': 'Order does not exist'}, status=status.HTTP_404_NOT_FOUND)