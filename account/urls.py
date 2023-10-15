from django.urls import path

from account.views import (
    AccountResetApiView,
    ChangePasswordApiView,
    CreateAccountApiView,
    ForgotPassword,
    LoginApiView,
    ResendActivationCode,
    VerifyAccountApiView,
)

app_name = "account"

urlpatterns = [
    path("signup/", CreateAccountApiView.as_view(), name="signup"),
    path("login/", LoginApiView.as_view(), name="login"),
    path("verify/", VerifyAccountApiView.as_view(), name="verify"),
    path("resend_otp/", ResendActivationCode.as_view(), name="resend_otp"),
    path("change_password/", ChangePasswordApiView.as_view(), name="change_password"),
    path("forgot_password/", ForgotPassword.as_view(), name="forgot_password"),
    path("reset_password/", AccountResetApiView.as_view(), name="reset_password"),
]
