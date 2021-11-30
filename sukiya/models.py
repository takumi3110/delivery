from django.db import models
from django.utils import timezone


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

	def __str__(self):
		# return self.name
		return '%s %s' % (self.name, self.memo)


# Todo:もう少しモデル構造を変更する


class Menu(models.Model):
	name = models.CharField(
		verbose_name='品名',
		max_length=100)
	category = models.ForeignKey(
		Category,
		on_delete=models.CASCADE,
	)

	def __str__(self):
		return self.name


# Todo:消費税計算変更
class Item(models.Model):
	size_cho = (
		("1", "ミニ"),
		("2", "並盛"),
		("3", "中盛"),
		("4", "大盛"),
		("5", "特盛"),
		("6", "メガ"),
		("7", "キング"),
	)

	menu = models.ForeignKey(
		Menu, on_delete=models.CASCADE
	)
	size = models.CharField(
		choices=size_cho,
		max_length=10
	)
	tax_price = models.PositiveIntegerField(
		verbose_name='税込価格',
		null=True, blank=True,
	)
	price = models.PositiveIntegerField(
		verbose_name='税抜価格',
		null=True, blank=True,
	)
	tax = models.IntegerField(
		verbose_name='消費税',
		null=True, blank=True,
	)
	calorie = models.PositiveIntegerField(
		verbose_name='カロリー'
	)

	def __str__(self):
		return '%s %s' % (self.menu, self.get_size_display())

	def save(self, *args, **kwargs):
		print(self.menu)
		tax = int(self.tax_price) * 10 / 110
		price = int(self.tax_price) / 1.1
		self.tax = tax
		self.price = price
		super(Item, self).save(*args, **kwargs)


# Todo:注文テーブル作成(荒川：藤澤)
class Order(models.Model):
	datetime = models.DateTimeField(
		verbose_name="来店時間",
		default=timezone.now,
	)

	table_no = models.PositiveIntegerField(
		verbose_name='卓番',
	)

	order_code = models.PositiveIntegerField(
		verbose_name="伝票番号",
	)

	total_price = models.PositiveIntegerField(
		verbose_name='合計金額',
		null=True,
		blank=True,
	)

	def __str__(self):
		return '%s %s' % (self.table_no, self.order_code)

# Todo:集計テーブル作成(悠哉)