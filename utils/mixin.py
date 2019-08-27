# 作者     ：gw
# 创建日期 ：2019-08-27  下午 22:31
# 文件名   ：mixin.py
from django.contrib.auth.decorators import login_required

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, ** initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(** initkwargs)
        return login_required(view)