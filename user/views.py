import os
import sys
import json
import requests
import random
import calendar
from decimal import Decimal, getcontext

from django.db.models import Q
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views import generic
from django.views.generic import TemplateView
from django_filters.views import FilterView
from django.urls import reverse_lazy
from stt.models import result
from ChangeLog.models import History
from .models import User, conf, Unit, Unit_Member, Unit_request, Unit_history
from .forms import ConfForm
from django.core.paginator import Paginator


def test(request):
	create_sample(request.user)
	return redirect('user:index')


def get_user(request):
	r_user = request.user
	return r_user


def create_sample(user):
	for num in range(0, 10, 1):
		a = random.random()
		stt_a = result(user=user, costfile_time=round(a * 1521.6958, 2))
		stt_a.save()


def create_sampleuser(request):
	for num in range(1, 11, 1):
		a = random.randint(1000, 9999)
		user = User(username=a, screenname="test" + str(num))
		user.save()
	return redirect('user:index')


# 自分自身か、スーパーユーザーならおｋ！
class OnlyYouMixin(UserPassesTestMixin):
	raise_exception = True

	def __init__(self):
		self.kwargs = None
		self.request = None

	def test_func(self):
		user = self.request.user
		return user.pk == self.kwargs['pk'] or user.is_superuser


class MyPage(OnlyYouMixin, generic.UpdateView):
	model = User
	template_name = 'user/mypage.html'
	form_class = ConfForm

	def get_form_kwargs(self):
		user = self.request.user  # formへ渡す変数
		kwargs = super(MyPage, self).get_form_kwargs()
		kwargs.update({'user': user})
		return kwargs

	def post(self, request, *args, **kwargs):
		form = self.get_form()
		user = self.request.user
		if form.is_valid():
			form = form.save(commit=False)
			query = conf.objects.get(user=user.pk)
			query.Default_conf = True
			query.Default_stt = self.request.POST.get('Default_stt')
			query.test = self.request.POST.get('')
			query.save()
			messages.success(
				self.request, '「{}」を更新しました'.format(self.request.user.screenname))
			return redirect('user:myp', pk=self.request.user.pk)
		if 'add' in self.request.POST:
			print('POST method OK!!')
			print("test")
			unit = Unit.objects.get(admin=user.pk)
			a_g = self.request.POST.getlist('add_group')
			for t in a_g:
				print(t)
				get_u = User.objects.filter(screenname=t)
				for g in get_u:
					print(g)
					unit = Unit.objects.get(admin=user.pk)
					print(unit)
					t = Unit_Member(unit_id=unit.pk, user_id=g.pk)
					t.save()
			return redirect('user:myp', pk=self.request.user.pk)
		if 'filter' in self.request.POST:
			print("filter")
			return redirect('user:myp', pk=self.request.user.pk)

	def get_context_data(self, **kwargs):
		global ur
		sum_cost = 0
		sum_time = 0
		unit_m = 0
		values = []
		unit_name = ""
		user = self.request.user
		now_date = datetime.now()
		print(now_date.month)
		context = super().get_context_data(**kwargs)
		# ログインユーザーの当月利用料金取得
		ami_cost = result.objects.filter(user=user.pk, Payment_Flg=False)
		# 利用料計算
		for ami in ami_cost:
			getcontext().prec = 2
			sum_cost = float(ami.costfile_time) + sum_cost
		unit = Unit.objects.filter(admin=user.pk)
		if unit:
			for u in unit:
				print(u)
				unit_name = u.name
				unit_m = Unit_Member.objects.filter(unit=u)
				context['unit'] = unit
				context['unit_m'] = unit_m
			# グループ管理者のみ使用
			group = group_use_calc(user, now_date)
			group_sum_cost = group['sumcost']
			group_Num_of_ami = group['count'] + ami_cost.count()
			print("グループ利用:%s" % group_sum_cost)
			all_cost = sum_cost + group_sum_cost
			context['group_ami_timecost'] = round(all_cost, 2)
			context['group_ami_sumcost'] = round(int(all_cost) * 0.025, 2)
			context['group_Num_of_ami'] = group_Num_of_ami
		# グループへの参加申請が行われたか判定
		# 参加申請があったときに管理者画面へ表示を行う。
		u_req = Unit_request.objects.filter(
			join_Unit__admin=user.pk).filter(Flg=False)
		if u_req:
			messages.success(self.request, '「%s」へ参加申請がありました。' % unit_name)
		# グループに所属していないユーザーを取得
		values = []
		query = ""
		um = Unit_Member.objects.all()
		if um:
			for u in um:
				print(u.user_id)
				values.append(u.user_id)
				print(values)
				queries = [Q(id=value) for value in values]
				query = queries.pop()
				for item in queries:
					query |= item
			ur = User.objects.exclude(query)
		else:
			# もしメンバーが一人もいなかった場合は、全員取得する
			print("メンバー取得できませんでした。")
			ur = User.objects.all()
		print("個人利用:%s" % sum_cost)
		print("グループ全体利用:%s" % test)
		# context開始
		# 取得したur の中からスーパーユーザーを除外
		# 取得したur の中から自分自身を除外
		context['all_user'] = ur.filter(is_superuser=False).exclude(
			username=self.request.user.username)
		# 個人利用料
		context['ami_cost'] = ami_cost
		# グループ利用料
		# 処理件数カウント
		context['Num_of_ami'] = ami_cost.count()
		# 利用料を足したやつ
		context['ami_timecost'] = round(sum_cost, 2)
		# 単価と利用量計算
		context['ami_sumcost'] = round(int(sum_cost) * 0.025, 2)

		context['unit_req'] = u_req
		# ログインユーザーのコンフィグ取得
		user_conf = user_conf = conf.objects.get(user=user.pk)
		context['conf'] = user_conf
		if user_conf.Default_stt == '2':
			messages.error(
				self.request, '音声認識エンジン「GCP」を選択されています。検証エンジンのため使用不可となっております。', extra_tags='danger')
		context['stt_flg'] = conf.objects.filter(user=self.request.user)
		context['History'] = History.objects.all().order_by('-created_at')
		# context終了
		###
		return context


# グループへユーザー追加
def group_join(request, uid):
	print("join")
	print(uid)
	u_req = Unit_request.objects.filter(pk=uid)
	for r in u_req:
		# メンバー追加
		um = Unit_Member(unit_id=r.join_Unit_id, user_id=r.user_id)
		um.save()
		# 申請情報更新
		r.Flg = True
		r.end_Date = datetime.now()
		r.save()
		# 履歴更新
		unit_hist = Unit_history(
			status="4", user=request.user, target=um.unit.name)
		unit_hist.save()
	return redirect('user:myp', pk=request.user.pk)


# 申請拒否
def group_Reject(request, uid):
	print("Reject")
	u_req = Unit_request.objects.filter(pk=uid)
	for r in u_req:
		r.Flg = True
		r.end_Date = datetime.now()
		r.save()
		message = r.join_Unit.name + "へ参加申請があった「" + r.user.screenname + "」を拒否しました。"
		unit_hist = Unit_history(status="6", user=request.user,
		                         target=r.join_Unit.name, memo=message)
		unit_hist.save()
	return redirect('user:myp', pk=request.user.pk)


# グループからユーザー削除
def group_remove(request, uid):
	print("test")
	um = Unit_Member.objects.get(pk=uid)
	um.delete()
	unit_hist = Unit_history(
		status="5", user=request.user, target=um.unit.name)
	unit_hist.save()
	return redirect('user:myp', pk=request.user.pk)


def group_use_calc(user, now_date):
	global unitm_test
	group_sumtimecost = 0
	group_Num_of_ami = 0
	Amiarray = {}
	unit = Unit.objects.filter(admin=user)
	for u in unit:
		# print(u.name)
		unitm_test = Unit_Member.objects.filter(unit__name=u.name)
		if not unitm_test:
			Amiarray = {'count': group_Num_of_ami,
			            'sumcost': group_sumtimecost}
	for umt in unitm_test:
		print("PBT:%s" % umt.user.username)
		user = User.objects.filter(username=umt.user.username)
		for u in user:
			print("user:%s" % u)
			ami = result.objects.filter(user=u, Payment_Flg=False)
			if not ami:
				group_sumtimecost = group_sumtimecost + 0
				group_Num_of_ami = group_Num_of_ami + 0
				Amiarray = {'count': group_Num_of_ami,
				            'sumcost': group_sumtimecost}
			for aa in ami:
				group_Num_of_ami = group_Num_of_ami + 1
				print(aa.pk, aa.file, aa.costfile_time)
				group_sumtimecost = group_sumtimecost + float(aa.costfile_time)
				Amiarray = {'count': group_Num_of_ami,
				            'sumcost': group_sumtimecost}

	return Amiarray