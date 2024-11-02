from decimal import Decimal
from django.conf import settings
from coupons.models import Coupon
from courses.models import Course


class Cart:
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # store current applied coupon
        self.coupon_id = self.session.get("coupon_id")

    def add(self, course):
        """
        Add a product to the cart
        """
        course_id = str(course.id)
        if course_id not in self.cart:
            self.cart[course_id] = {
                "price": str(course.price),
            }
        self.save()

    def save(self):
        # mark the session as 'modified' to make sure it gets saved
        self.session.modified = True

    def remove(self, course):
        """
        Remove a product from the cart
        """
        course_id = str(course.id)
        if course_id in self.cart:
            del self.cart[course_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the courses from the database
        """
        course_ids = self.cart.keys()
        # get the course object and add them to the cart
        courses = Course.objects.filter(id__in=course_ids)
        cart = self.cart.copy()
        for course in courses:
            cart[str(course.id)]["course"] = course

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            yield item

    def __len__(self):
        """
        Count all items in the cart
        """
        total = 0
        for _ in self.cart.values():
            total += 1
        return total

    def get_total_price(self):
        return sum(Decimal(item["price"]) for item in self.cart.values())

    def check_item_id(self, id):
        return id

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()

    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass

        return None

    def get_discount(self):
        if self.coupon:
            return self.coupon.discount / Decimal(100) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()

    def get_courses_id(self):
        ids = str()
        keys = list(self.cart.keys())
        for index, value in enumerate(keys):
            print(value, index)
            if index == 0:
                ids += f"{value}"
            else:
                ids += f"-{value}"
        return ids
