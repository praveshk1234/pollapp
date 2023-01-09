from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    username=models.CharField(max_length=200,blank=True,null=True)
    def __str__(self):
        return str(self.user.username)

class Poll(models.Model):
    owner= models.ForeignKey(Profile,on_delete=models.CASCADE)
    text=models.TextField()
    publishedAt=models.DateTimeField(default=timezone.now)
    active=models.BooleanField(default=True)
    def __str__(self):
        return str(self.text)
    @property
    def total_vote(self):
        return self.vote_set.count()
    def get_result_dict(self):
        res = []
        for choice in self.choice_set.all():
            d = {}
            d['text'] = choice.choice_value
            d['num_votes'] = choice.total_vote
            if not self.total_vote:
                d['percentage'] = 0
            else:
                d['percentage'] = int((choice.total_vote /
                                   self.total_vote)*100)

            res.append(d)

        return res
    def has_user_vote(self,user):
        owner_votes=user.vote_set.all()
        qs=owner_votes.filter(poll=self)
        if qs.exists():
            return False
        return True

class Choice(models.Model):
    poll= models.ForeignKey(Poll,on_delete=models.CASCADE)
    choice_value=models.CharField(max_length=255)
    @property
    def total_vote(self):
        return self.vote_set.count()

class Vote(models.Model):
    user=models.ForeignKey(Profile,on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll,on_delete=models.CASCADE)
    choices= models.ForeignKey(Choice,on_delete=models.CASCADE)