from .models import NetflixTitle, Review
from django import forms
from django.utils.safestring import mark_safe
from decimal import Decimal, InvalidOperation


class StarRatingWidget(forms.Widget):
    """Reusable star rating widget (0.0 - 5.0 in 0.5 steps).
    Renders a compact number spinner and a star display filled proportionally.
    """
    template_name = None

    def __init__(self, attrs=None):
        default_attrs = {'type': 'number', 'min': '0', 'max': '5', 'step': '0.5'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    def render(self, name, value, attrs=None, renderer=None):
        try:
            val = Decimal(value) if value is not None and value != '' else Decimal('0.0')
        except (InvalidOperation, TypeError):
            val = Decimal('0.0')

        final_attrs = self.build_attrs(self.attrs, attrs)
        input_id = final_attrs.get('id', f'id_{name}')

        # calculate percentage fill (0-100)
        pct = float((val / Decimal('5.0')) * 100)

        html = """
<div class="star-rating-widget" style="display:inline-block; font-size:24px; position:relative;">
    <!-- compact number spinner (up/down) -->
    <input name="{name}" id="{input_id}" type="number" min="0" max="5" step="0.5" value="{val}"
           style="width:4.2ch; vertical-align:middle; padding:2px;">
    <div class="stars" aria-hidden="true" style="display:inline-block; position:relative; margin-left:8px; vertical-align:middle;">
        <div class="stars-back" style="color:#bbb; font-size:24px;">
            <span>★★★★★</span>
        </div>
        <div class="stars-front" style="color:#c00; font-size:24px; position:absolute; left:0; top:0; overflow:hidden; width:{pct}%; white-space:nowrap; transition:width .15s linear;">
            <span>★★★★★</span>
        </div>
    </div>
</div>
<script>
(function(){
    var input = document.getElementById('{input_id}');
    if(!input) return;
    var display = document.getElementById('{input_id}_display');
    var front = input.parentNode.querySelector('.stars-front');
    function update(){
        var raw = input.value;
        var v = parseFloat(raw);
        if (isNaN(v)) v = 0;
        // clamp
        if (v < 0) v = 0;
        if (v > 5) v = 5;
        // show with one decimal (so 3 -> 3.0, 3.5 -> 3.5)
        var shown = v.toFixed(1).replace(/\.0$/,'');
        if(display) display.textContent = shown;
        var pct = (v/5)*100;
        if(front) front.style.width = pct + '%';
    }
    input.addEventListener('input', update);
    input.addEventListener('change', update);
    // init
    update();
})();
</script>
"""

        # Substitute placeholders safely
        html = html.replace('{input_id}', input_id).replace('{pct}', str(pct)).replace('{name}', name).replace('{val}', str(val))

        return mark_safe(html)


class NetflixTitleForm(forms.ModelForm):
    class Meta:
        model = NetflixTitle
        fields = [
            'title_type',
            'title',
            'director',
            'cast',
            'country',
            'date_added',
            'release_year',
            'rating',
            'duration',
            'genres',
            'description',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'cast': forms.Textarea(attrs={'rows': 3}),
            'date_added': forms.DateInput(attrs={'type': 'date'}),
            'rating': StarRatingWidget(),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_text', 'date_watched']
        widgets = {
            'review_text': forms.Textarea(attrs={'rows': 3}),
            'date_watched': forms.DateInput(attrs={'type': 'date'}),
        }

    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # override widget for rating to use module-level star widget
        self.fields['rating'].widget = StarRatingWidget()

    def clean_rating(self):
        raw = self.cleaned_data.get('rating')
        try:
            rating = Decimal(raw)
        except (InvalidOperation, TypeError):
            raise forms.ValidationError("Enter a valid rating between 0 and 5 in 0.5 steps.")
        if rating < Decimal('0') or rating > Decimal('5'):
            raise forms.ValidationError("Rating must be between 0 and 5.")
        # enforce 0.5 step
        multiplied = rating * 2
        if multiplied != multiplied.quantize(Decimal('1')):
            raise forms.ValidationError("Rating must be in 0.5 increments.")
        return rating