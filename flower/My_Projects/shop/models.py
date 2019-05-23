from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm


class Good(models.Model):
    name = models.CharField(max_length=120, null=False, blank=False, help_text='назва товару')
    price = models.FloatField(blank=False, null=False, default=0, help_text='ціна товару')
    quantity = models.IntegerField(default=0, help_text="кількість доступних одиниць")
    description = models.CharField(max_length=500, help_text='описання товару')
    category = models.CharField(max_length=1, choices=(('b', 'bouket'), ('g', 'gift'), ('c', 'composition')),
                                default='b')
    good_item = models.CharField(max_length=11,
                                 choices=(('item_hit', 'item_hit'),
                                          ('item_action', 'item_action'),
                                          ('item_new', 'item_new'),
                                          ('', '')),
                                 default='', blank=True)
    img_content = models.ImageField(upload_to='static/content/', help_text='картинка для переліку', default='')
    img1 = models.ImageField(upload_to='static/img/', help_text='перша картинка для відображення')
    img2 = models.ImageField(upload_to='static/img/',
                             help_text='ще одна картинка для відображення', blank=True, null=True)
    img3 = models.ImageField(upload_to='static/img/',
                             help_text='картинка для відображення', blank=True, null=True)

    @property
    def availability(self):
        return bool(self.quantity > 0)

    def __str__(self):
        return self.name + " " + "(" + self.description + ")" + " за ціною " + str(self.price) + " грн"


class Reviews(models.Model):
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    rating = models.IntegerField(choices=((1, 1), (2, 2), (3, 3), (4, 4), (5, 5)), default=5)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-date']


class ReviewForm(ModelForm):
    class Meta:
        model = Reviews
        fields = ['good', 'user', 'text']


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date_order = models.DateField(auto_now=True)
    sended = models.BooleanField(default=False)
    paied = models.BooleanField(default=False)

    send = models.BooleanField(default=False)
    date_resive = models.DateTimeField(auto_now=True)
    address_city = models.CharField(max_length=300, blank=True, default="")
    address_local = models.CharField(max_length=300, default='')
    receiver_surname = models.CharField(max_length=100, blank=True, null=True)
    receiver_name = models.CharField(max_length=100, blank=True, null=True)
    receiver_lastname = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=13, blank=True, null=True)
    receiver_card = models.BooleanField(default=False)
    receiver_text = models.CharField(max_length=1000, blank=True, default="")
    sum_total = models.FloatField(default=0)
    shipping_date = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return "Користувач " + str(self.user) + " замовив на сумму " + str(self.sum_total) + " грн " + str(
            self.date_order)


class FormOrder(ModelForm):
    class Meta:
        model = Order
        # fields = ['address_city', 'ad' 'phone', 'sum_total', 'send']
        exclude = ['date_order', 'sended', 'paied']
        # widgets = {
        #     'date_resive': DateInput(attrs={'type': 'date'})



class GoodsInOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return "замовлення" + "(" + str(self.order.id) + ") товар: " + self.good.name + " кількість: " + str(
            self.quantity) + "шт" + " від користувача " + self.order.user.username
