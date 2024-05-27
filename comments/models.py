from django.db import models
from spots.models import Spot
from members.models import Member  # 引入自定義的 Member 模型

class Comment(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)  # 外鍵關聯到自定義的 Member 模型
    spot = models.ForeignKey(Spot, null=True, blank=True, on_delete=models.CASCADE)  # 設置為可選
    content = models.TextField()
    value = models.IntegerField(default=None)  # 合併 Rating 的 value 字段
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.created_at} - Rating: {self.value}"
