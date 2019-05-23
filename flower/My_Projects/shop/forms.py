# import unicodedata
#
# from django import forms
# from django.contrib.auth import (
#     authenticate, get_user_model, password_validation,
# )
# from django.contrib.auth.forms import UsernameField, EmailMultiAlternatives
# from django.contrib.auth.hashers import (
#     UNUSABLE_PASSWORD_PREFIX, identify_hasher,
# )
# from django.contrib.auth.models import User
# from django.contrib.auth.tokens import default_token_generator
# from django.contrib.sites.shortcuts import get_current_site
# from django.core.mail import EmailMultiAlternatives
# from django.template import loader
# from django.utils.encoding import force_bytes
# from django.utils.http import urlsafe_base64_encode
# from django.utils.text import capfirst
# from django.utils.translation import gettext, gettext_lazy as _
#
#
# class UserCreationForm(forms.ModelForm):
#     """
#     A form that creates a user, with no privileges, from the given username and
#     password.
#     """
#     error_messages = {
#         'password_mismatch': _("The two password fields didn't match."),
#     }
#     password1 = forms.CharField(
#         label=_("Password"),
#         strip=False,
#         widget=forms.PasswordInput,
#         help_text=password_validation.password_validators_help_text_html(),
#     )
#     password2 = forms.CharField(
#         label=_("Password confirmation"),
#         widget=forms.PasswordInput,
#         strip=False,
#         help_text=_("Enter the same password as before, for verification."),
#     )
#
#
#
#     class Meta:
#         model = User
#         fields = ("username",)
#         field_classes = {'username': UsernameField}
#
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if self._meta.model.USERNAME_FIELD in self.fields:
#             self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})
#
#     def clean_password2(self):
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError(
#                 self.error_messages['password_mismatch'],
#                 code='password_mismatch',
#             )
#         return password2
#
#     def _post_clean(self):
#         super()._post_clean()
#         # Validate the password after self.instance is updated with form data
#         # by super().
#         password = self.cleaned_data.get('password2')
#         if password:
#             try:
#                 password_validation.validate_password(password, self.instance)
#             except forms.ValidationError as error:
#                 self.add_error('password2', error)
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user
