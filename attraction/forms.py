from django import forms
from django.db import transaction

from attraction.models import Comment, Attraction


class PostCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('attraction', 'rating', 'content')

    def clean_attraction(self):
        attraction = self.cleaned_data['attraction']
        if not attraction.is_valid:
            raise forms.ValidationError('Attraction is not valid')
        return attraction

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if not 0 <= rating <= 5:
            raise forms.ValidationError('Rating is out of range')
        return rating

    def save(self, user, commit=False):
        # create a comment_obj, assign the other fields and save
        comment_obj = super().save(commit=commit)
        comment_obj.user = user
        comment_obj.save()

        return comment_obj
