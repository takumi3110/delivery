from django import forms
from django.forms import RadioSelect
from .models import conf


class ConfForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		# viewから変数を取得
		user = kwargs.pop('user', None)
		super(ConfForm, self).__init__(*args, **kwargs)
		print(user.pk)
		conf_stt = conf.objects.filter(user=user.pk).get()
		self.fields['Default_stt'].initial = conf_stt.Default_stt
		self.fields['Default_stt'].widget.attrs['class'] = 'form-control input-sm'

	class Meta:
		model = conf
		# fields = ('Default_stt', 'Default_conf', 'test')
		fields = ('Default_stt',)
		widgets = {

		}