# -*- coding: utf-8-*-
import os
from hashlib import sha1
from urllib import urlencode
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_str
from .gridder import PDFGridder
from .utils import hex_to_rgba, parse_unit

# Create your models here.
UNITS_CHOICES = (
    ('in', 'inches'),
    ('mm', 'millimeters'),
    ('px', 'pixels'),
    ('pt', 'points'),
)


class Grid(models.Model):
    """A Grid System"""
    name = models.CharField(blank=True, null=True, default='Untitled', max_length=100)
    description = models.TextField(blank=True, null=True)
    star = models.BooleanField(default=False)
    hash = models.CharField(blank=True, null=True, max_length=40)
    width = models.FloatField(default=210)
    width_unit = models.CharField(blank=False, max_length=2, choices=UNITS_CHOICES, default='mm')
    height = models.FloatField(default=297)
    height_unit = models.CharField(blank=False, max_length=2, choices=UNITS_CHOICES, default='mm')
    margin_left = models.FloatField("Left", default=5)
    margin_left_unit = models.CharField(blank=False, max_length=2, choices=UNITS_CHOICES, default='mm')
    margin_right = models.FloatField("Right", default=5)
    margin_right_unit = models.CharField(blank=False, max_length=2, choices=UNITS_CHOICES, default='mm')
    margin_top = models.FloatField("Top", default=5)
    margin_top_unit = models.CharField(blank=False, max_length=2, choices=UNITS_CHOICES, default='mm')
    margin_bottom = models.FloatField("Bottom", default=5)
    margin_bottom_unit = models.CharField(blank=False, max_length=2, choices=UNITS_CHOICES, default='mm')

    columns = models.IntegerField(blank=False, null=False, default=7)
    columns_gutter = models.FloatField(default=3)
    columns_gutter_unit = models.CharField(blank=False, max_length=2, choices=UNITS_CHOICES, default='mm')

    baseline = models.FloatField(default=15)
    baseline_unit = models.CharField(blank=False, max_length=2, choices=UNITS_CHOICES, default='pt')

    grid = models.FileField(upload_to='grids', blank=True, null=True)

    columns_color = models.CharField(blank=False, max_length=7, default='#eeeeee')
    columns_opacity = models.FloatField(blank=False, default=1.0)

    baseline_color = models.CharField(blank=False, max_length=7, default='#c0c0c0')
    baseline_opacity = models.FloatField(blank=False, default=1.0)
    created = models.DateTimeField(blank=True, auto_now_add=True)
    is_spread = models.BooleanField("Facing pages", default=False)

    user = models.ForeignKey('auth.User', blank=True, null=True)
    session_key = models.CharField(blank=True, null=True, max_length=128, db_index=True)

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        self.hash = self.grid_hash()
        filename = os.path.join('grids', self.hash + '.pdf')
        output = os.path.join(settings.MEDIA_ROOT, filename)
        if settings.DEBUG or not os.path.exists(output):
            gridder = PDFGridder(self)
            gridder.build(output=output)
        self.grid = filename
        super(Grid, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return self.grid.url

    def __unicode__(self):
        if self.name:
            return self.name
        return self.summary()

    def summary(self):
        if self.is_spread:
            summary = u'Spread, '
        else:
            summary = u''

        summary += u'%d cols, gutter %.1f%s, baseline %.1f%s' % (self.columns, self.columns_gutter, self.columns_gutter_unit, self.baseline, self.baseline_unit)
        return summary

    def grid_hash(self):
        """Generates an hash unique for a grid system based on its paramaters.
This is used as the name for the generated PDF on the file-system, as a sort of naive cache.
"""
        sets = '%d%.2fx%.2fg%.2ft%.2fr%.2fb%.2fl%.2fb%.2fc%s%.2fb%s%.2f%s' % (self.columns,
                   parse_unit(self.width, self.width_unit),
                   parse_unit(self.height, self.height_unit),
                   parse_unit(self.columns_gutter, self.columns_gutter_unit),
                   parse_unit(self.margin_top, self.margin_top_unit),
                   parse_unit(self.margin_right, self.margin_right_unit),
                   parse_unit(self.margin_bottom, self.margin_bottom_unit),
                   parse_unit(self.margin_left, self.margin_left_unit),
                   parse_unit(self.baseline, self.baseline_unit),
                   self.columns_color.lstrip('#'),
                   self.columns_opacity,
                   self.baseline_color.lstrip('#'),
                   self.baseline_opacity,
                   self.is_spread)
        hashed_sets = sha1(sets).hexdigest()
        return hashed_sets

    def get_params_url(self):
        params = [(f.name, smart_str(getattr(self, f.name), strings_only=True)) for f in self._meta.fields]
        encoded = urlencode(params)
        return reverse('home') + '?' + encoded

    def get_edit_url(self):
        return reverse('edit_grid', kwargs={'object_id': self.id})

    @property
    def columns_width(self):
        w = parse_unit(self.width, self.width_unit)
        gutter = parse_unit(self.columns_gutter, self.columns_gutter_unit)
        right = parse_unit(self.margin_right, self.margin_right_unit)
        left = parse_unit(self.margin_left, self.margin_left_unit)
        cols = self.columns

        cols_width = (w / cols) - gutter + (gutter / cols) - (left / cols) - (right / cols)
        return cols_width

    @property
    def columns_rgba(self):
        return hex_to_rgba(self.columns_color, self.columns_opacity)

    @property
    def baseline_rgba(self):
        return hex_to_rgba(self.baseline_color, self.baseline_opacity)

    @property
    def width_str(self):
        return u'%.2f%s' % (self.width, self.width_unit)

    @property
    def height_str(self):
        return u'%.2f%s' % (self.height, self.height_unit)

    def paper(self):
        return u'%s x %s' % (self.width_str, self.height_str)

    def margins(self):
        return u'%.2f%s %.2f%s %.2f%s %.2f%s' % (self.margin_top, self.margin_top_unit, self.margin_right, self.margin_right_unit, self.margin_bottom, self.margin_bottom_unit, self.margin_left, self.margin_left_unit)

    def baseline_str(self):
        return u"%.2f%s" % (self.baseline, self.baseline_unit)

    def columns_gutter_str(self):
        return u"%.2f%s" % (self.columns_gutter, self.columns_gutter_unit)
