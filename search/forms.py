from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, MultiField, Field
from crispy_forms.bootstrap import InlineRadios

from django.contrib.sessions.backends.db import SessionStore

from MATOM.models import TranscriptionFactor

class SearchForm(forms.Form):
    ORG_CHOICES =(("SAPIENS", 'Human'), ("MELANONGASTER", 'Drosophila'))
    org = forms.ChoiceField(
        choices=ORG_CHOICES,
        label="Select the organism:",
        #widget=forms.RadioSelect(attrs={'id': 'id-org'}),
        initial='SAPIENS'
    )
    search = forms.CharField(
        label="Enter TF name",
        initial='Atf1'
    )

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-SearchForm'
        #self.helper.form_style = 'hidden'
        self.helper.form_class = 'SearchForm'
        #self.helper.label_class = 'add_Bold'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.form_method = 'post'
        self.helper.form_action = '/search/'
        self.helper.layout = Layout(
            'org',
            'search'

        )


class AssessByComparisonForm(forms.Form):
    ORG_CHOICES =(("SAPIENS", 'Human'), ("MELANONGASTER", 'Drosophila'))
    org = forms.ChoiceField(
        choices=ORG_CHOICES,
        label="Select the organism:",
        #widget=forms.RadioSelect(attrs={'id': 'id-org'}),
        initial='SAPIENS'
    )
    COMPARE_CHOICES =(("FISIM", 'FISim'), ("TOMTOM", 'Tomtom'))
    mode = forms.ChoiceField(
        choices=COMPARE_CHOICES,
        label="Choose motif comparison tool to use:",
        widget=forms.RadioSelect(attrs={'id': 'id-mode'}),
        initial='TOMTOM'
    )
    tf = forms.CharField(
        label="Transcription factor name:",
        initial='Atf1'
    )
    MEME_CHOICES = (('upload', "Upload motifs"), ('paste', "Paste motifs"))
    formats = forms.ChoiceField(
        choices=MEME_CHOICES,
        label="Upload or Paste MEME formatted motifs (Optional):",
        widget=forms.RadioSelect(attrs={'id': 'id-seq'}),
        #initial='upload',
        required=False
    )
    test_motif = forms.CharField(
        label="Paste motif/s:",
        required=False,
        widget=forms.Textarea
    )
    uploaded_motif = forms.FileField(
        label="Upload motif/s:",
        required=False)

    def __init__(self, *args, **kwargs):
        super(AssessByComparisonForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_id = 'id-comparisonForm'
        #self.helper.form_style = 'hidden'
        self.helper.form_class = 'comparisonForm'
        self.helper.label_class = 'add_Bold'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.form_method = 'post'
        self.helper.form_action = '/comparison/'
        self.helper.layout = Layout(
            'org',
            'tf',
            'mode',
            InlineRadios('formats'),
            'test_motif',
            'uploaded_motif'

        )


class AssessByScoreForm(forms.Form):
    ORG_CHOICES =(("SAPIENS", 'Human'), ("MELANONGASTER", 'Drosophila'))
    org = forms.ChoiceField(
        choices=ORG_CHOICES,
        label="Select the organism:",
        #widget=forms.RadioSelect(attrs={'id': 'id-org'}),
        initial='SAPIENS'
    )
    MODE_CHOICES = (("ASSESS", 'SCORE'), ('GIMME', 'Gimme'))
    mode = forms.ChoiceField(
        choices=MODE_CHOICES,
        label="Choose assess by scoring algorithm to use:",
        widget=forms.RadioSelect,
        initial="ASSESS"
    )
    tf = forms.CharField(
        label="Enter transcription factor name:",
        initial='Hnf4a'

    )
    MEME_CHOICES = (('upload', "Upload motifs"), ('paste', "Paste motifs"))
    formats = forms.ChoiceField(
        choices=MEME_CHOICES,
        label="Upload or Paste MEME formatted motifs (Optional):",
        widget=forms.RadioSelect(attrs={'id': 'id-seq'}),
        #initial='upload',
        required=False
    )
    test_motif = forms.CharField(
        label="Paste motif/s:",
        required=False,
        widget=forms.Textarea,
    )
    uploaded_motif = forms.FileField(
        label="Upload motif/s:",
        required=False
    )
    data = forms.ChoiceField(
        choices=[(x, x) for x in ("ChIP-seq", "PBM")],
        label="Select data type:",
        widget=forms.RadioSelect,
        initial='ChIP-seq'
    )
    uploaded_chipseq = forms.FileField(
        label="Upload a ChIP-seq data in BED format (optional)",
        required=False,
        help_text="BED: chr start end score"
    )
    SCORE_CHOICES = (("gomeroccupancyscore", 'GOMER Occupancy score'), ("energyscore", 'BEEML Energy score'),
               ("sumlogoddsscore", 'Sum log-odds score'), ("sumoccupancyscore", 'Sum occupancy score'),
               ("amaoccupancyscore", 'AMA occupancy score'), ("maxoccupancyscore", 'Maximum occupancy score'),
               ("maxlogoddsscore", 'Maximum log-odds score'))

    score = forms.ChoiceField(
        choices=SCORE_CHOICES,
        label="Select scoring function:",
        widget=forms.RadioSelect,
        initial='energyscore'

    )

    def __init__(self, *args, **kwargs):
        super(AssessByScoreForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-ScoreForm'
        self.helper.form_class = 'ScoreForm'
        self.helper.label_class = 'add_Bold'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.form_method = 'post'
        self.helper.form_action = '/score/'
        self.helper.layout = Layout(
            'org',
            'tf',
            'mode',
            InlineRadios('formats'),
            'test_motif',
            'uploaded_motif',
            InlineRadios('data'),
            'uploaded_chipseq',
            'score',

        )


class AssessByEnrichmentForm(forms.Form):
    ORG_CHOICES =(("SAPIENS", 'Human'), ("MELANONGASTER", 'Drosophila'))
    org = forms.ChoiceField(
        choices=ORG_CHOICES,
        label="Select the organism:",
        #widget=forms.RadioSelect(attrs={'id': 'id-org'}),
        initial='SAPIENS'
    )
    mode = forms.ChoiceField(
        choices=[(x, x) for x in ("CENTRIMO", "AME")],
        label="Select Motif enrichment algorithm",
        widget=forms.RadioSelect,
        initial='CENTRIMO'
    )
    tf = forms.CharField(
        label="Transcription factor name:",
        initial='Hnf4a'
    )
    MEME_CHOICES = (('upload', "Upload Motifs"), ('paste', "Paste Motifs"))
    formats = forms.ChoiceField(
        choices=MEME_CHOICES,
        label="Upload or Paste MEME formatted motifs (Optional):",
        widget=forms.RadioSelect(attrs={'id': 'id-seq'}),
        #initial='upload',
        required=False
    )
    test_motif = forms.CharField(
        label="Paste motif/s:",
        required=False,
        widget=forms.Textarea,
    )
    uploaded_motif = forms.FileField(
        label="Upload motif/s:",
        required=False
    )
    uploaded_chipseq = forms.FileField(
        label="Upload a ChIP-seq data in BED format (optional)",
        required=False,
        help_text="BED: chr start end score"
    )

    def __init__(self, *args, **kwargs):
        super(AssessByEnrichmentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-EnrichmentForm'
        self.helper.form_class = 'EnrichmentForm'
        self.helper.label_class = 'add_Bold'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.form_method = 'post'
        self.helper.form_action = '/enrichment/'
        self.helper.layout = Layout(
            'org',
            'tf',
            'mode',
            InlineRadios('formats'),
            'test_motif',
            'uploaded_motif',
            InlineRadios('data'),
            'uploaded_chipseq',

        )


class UnknownForm(forms.Form):
    # search = forms.ModelMultipleChoiceField(
    #     queryset=TranscriptionFactor.objects.filter(tf_name='Atf1'),  # not optional, use .all() if unsure
    #     widget=forms.CheckboxSelectMultiple,
    # )

    SCORE_CHOICES = (("gomeroccupancyscore", 'GOMER Occupancy score'),)
    tf_choices = forms.ChoiceField(
        choices=SCORE_CHOICES,
        label=" ",
        required=False
        #widget=forms.RadioSelect,
    )

    def __init__(self, *args, **kwargs):
        super(UnknownForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-UnknownForm'
        self.helper.form_class = 'UnknownForm'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.form_method = 'POST'
        self.helper.form_action = '/search/select/'
        self.helper.form_show_labels = False,
        self.helper.layout = Layout(
            'tf_choices',
            # 'tf',
            # InlineRadios('formats'),
            # 'test_motif',
            # 'uploaded_motif',
            # InlineRadios('data'),
            # 'uploaded_chipseq',

        )

