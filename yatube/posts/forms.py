from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['placeholder'] = (
            'Желательно добавить какой нибудь текст'
        )
        self.fields['group'].empty_label = (
            'Выберите группу, если желаете 🙂'
        )

    class Meta:
        model = Post
        fields = ('text', 'group')
        labels = {
            'text': 'Введите текст',
            'group': 'Выберете группу'
        }
        help_texts = {
            'text': 'Попробуй ввести текст',
            'group': 'Выбираем только существующие группы'
        }
