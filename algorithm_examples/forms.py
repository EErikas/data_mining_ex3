from django import forms


class UploadForm(forms.Form):
    docfile = forms.FileField(
        label='Select a data file',
        help_text='Note: Data must be separated by commas, max file size is 42 megabytes'
    )
    criterion = forms.ChoiceField(
        label='Select criterion',
        help_text='The function to measure the quality of a split. Supported criteria are “gini” for the Gini impurity and “entropy” for the information gain.',
        choices=(('gini', 'Gini'), ('entropy', 'Entropy'))
    )
    splitter = forms.ChoiceField(
        label='Select splitter strategy',
        help_text='The strategy used to choose the split at each node. Supported strategies are “best” to choose the best split and “random” to choose the best random split.',
        choices=(('best', 'Best'), ('random', 'Random'))
    )


class IdCarverForm(forms.Form):
    text = forms.CharField(
        label='Enter your text',
        widget=forms.Textarea
    )
