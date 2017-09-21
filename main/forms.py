from django import forms

from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
	)


User = get_user_model()




class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError("Invalid Username or password")
			if not user.check_password(password):
				raise forms.ValidationError("Invalid password")
		return super(UserLoginForm,self).clean(*args,**kwargs)



class UserRegisterForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	confirm_password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'password',
			'confirm_password'
		]

	def clean(self, *args, **kwargs):
		password = self.cleaned_data.get('password')
		confirm_password = self.cleaned_data.get('confirm_password')
		email = self.cleaned_data.get('email')
		if password != confirm_password:
			raise forms.ValidationError("password and confirm_password not match.")
		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("This email has already been registered.")
		return super(UserRegisterForm,self).clean(*args, **kwargs)
