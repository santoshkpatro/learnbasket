import uuid
import shortuuid
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from techowiz.models.coupon import Coupon
from techowiz.models.program import Program
from techowiz.models.order import Order
from techowiz.api.v1.orders.serializers import OrderCreateSerializer


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

            order = Order(
                order_id=shortuuid.ShortUUID().random(length=10).upper(),
                program=program,
                user=request.user,
                price=float(program.price),
                amount=float(program.price) - discount,
                discount=discount,
                coupon=discount_coupon,
                transaction_id=uuid.uuid4().hex
            )
            serializer = OrderCreateSerializer(order)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except Program.DoesNotExist:
            return Response(data={'detail': 'Program not found'}, status=status.HTTP_404_NOT_FOUND)