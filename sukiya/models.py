from django.db import models
from django.utils import timezone

from user.models import User


class Category(models.Model):
	name = models.CharField(
		verbose_name='カテゴリー名',
		max_length=50,
		null=True, blank=True,
	)

	memo = models.TextField(
		verbose_name='メモ',
		null=True, blank=True,
	)

	img = models.ImageField(
		upload_to='images/',
		null=True,
		blank=True
	)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'カテゴリー'
		verbose_name_plural = 'カテゴリー'


class Item(models.Model):
	name = models.CharField(
		verbose_name='品名',
		max_length=100,
		null=True,
		blank=True
	)
	category = models.ForeignKey(
		Category,
		on_delete=models.CASCADE,
	)

	new = models.BooleanField(
		verbose_name='新商品',
		default=False
	)

	limited = models.BooleanField(
		verbose_name='期間限定',
		default=False
	)

	recommend = models.BooleanField(
		verbose_name='おすすめ',
		default=False
	)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = '品名'
		verbose_name_plural = '品名'


# Todo:消費税計算変更
class Menu(models.Model):
	size_cho = (
		("1", "ミニ"),
		("2", "並盛"),
		("3", "中盛"),
		("4", "大盛"),
		("5", "特盛"),
		("6", "メガ"),
		("7", "キング"),
	)

	item = models.ForeignKey(
		Item,
		on_delete=models.CASCADE
	)
	size = models.CharField(
		choices=size_cho,
		max_length=10,
		null=True,
		blank=True
	)
	tax_price = models.PositiveIntegerField(
		verbose_name='税込価格',
		null=True,
		blank=True,
	)
	price = models.PositiveIntegerField(
		verbose_name='税抜価格',
		null=True,
		blank=True,
	)
	tax = models.IntegerField(
		verbose_name='消費税',
		null=True,
		blank=True,
	)
	calorie = models.PositiveIntegerField(
		verbose_name='カロリー'
	)

	def __str__(self):
		return '%s %s' % (self.item.name, self.get_size_display())

	def save(self, *args, **kwargs):
		tax = int(self.tax_price) * 10 / 110
		price = int(self.tax_price) / 1.1
		self.tax = tax
		self.price = price
		super(Menu, self).save(*args, **kwargs)

	class Meta:
		verbose_name = 'メニュー'
		verbose_name_plural = 'メニュー'


class OrderItem(models.Model):

	menu = models.ForeignKey(
		Menu,
		on_delete=models.CASCADE,
		verbose_name='メニュー'
	)

	quantity = models.PositiveSmallIntegerField(
		verbose_name='数量',
		default=1
	)

	price = models.PositiveIntegerField(
		verbose_name='金額',
	)

	def save(self, *args, **kwargs):
		item_price = self.item.tax_price
		self.price = item_price * self.quantity
		super(OrderItem, self).save(*args, **kwargs)

	def __str__(self):
		return self.menu.item.name

	class Meta:
		verbose_name = '注文商品'
		verbose_name_plural = '注文商品'


# Todo:注文テーブル作成(荒川：藤澤)
class Order(models.Model):
	table = models.PositiveSmallIntegerField(
		verbose_name='卓番',
	)

	number = models.PositiveIntegerField(
		verbose_name="伝票番号",
	)

	date = models.DateTimeField(
		verbose_name="来店時間",
		default=timezone.now,
	)

	order_item = models.ManyToManyField(
		OrderItem,
		verbose_name='注文商品'
	)

	total_price = models.PositiveIntegerField(
		verbose_name='合計金額'
	)

	ordered = models.BooleanField(
		verbose_name='注文済み',
		default=False
	)

	def __str__(self):
		return '%s %s' % (self.table_no, self.order_code)

	class Meta:
		verbose_name = '注文内容'
		verbose_name_plural = '注文内容'


# Todo:集計テーブル作成(悠哉)
class Invoice(models.Model):
	contact_user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		verbose_name='担当者'
	)

	order = models.ForeignKey(
		Order,
		on_delete=models.CASCADE,
		verbose_name='注文内容'
	)

	leaved_date = models.DateTimeField(
		verbose_name='退店時間',
		null=True,
		blank=True
	)

	def __str__(self):
		return self.contact_user

