from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,IntegerField,BooleanField,DecimalField,RadioField
from wtforms.validators import DataRequired
from ..models import *


class SearchForm(FlaskForm):
    autocomp= StringField('autocomp',id='autocomplete')

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    birthday = DecimalField('Birth',validators=[DataRequired()])
    submit = SubmitField('Submit')

class PeakAgentForm(FlaskForm):
    current = IntegerField('当前积分：', validators=[DataRequired()])
    expectation = IntegerField('目标积分：', validators=[DataRequired()])
    isSpecialCham = BooleanField('是否指定英雄')
    isChamAsses = BooleanField('是否为辅助英雄')
    submit = SubmitField('查询')
 
class QualifyingAgentForm(FlaskForm):
    current = StringField('当前等级：', validators=[DataRequired()],id='currentInput')
    expectation = StringField('目标等级：', validators=[DataRequired()],id='expectationInput')
    isSpecialCham = BooleanField('是否指定英雄')
    isChamAsses = BooleanField('是否为辅助英雄')
    submit = SubmitField('查询')
 
class QualifyingPlaymateForm(FlaskForm):
    current = StringField('当前等级：', validators=[DataRequired()],id='currentInput')
    expectation = StringField('目标等级：', validators=[DataRequired()],id='expectationInput')
    options = [('qualifying_playmate_formation_3','三排'),('qualifying_playmate_formation_5','五排')]
    formation = RadioField('队形',choices=options,default='qualifying_playmate_formation_5')
    submit = SubmitField('查询')

class ForceAgentForm(FlaskForm):
    current = IntegerField('当前战力：', validators=[DataRequired()])
    expectation = IntegerField('目标战力：', validators=[DataRequired()])
    currentLevel = StringField('当前排位赛等级', validators=[DataRequired()],id='currentLevelInput')
    currentPoint = IntegerField('当前巅峰赛积分', validators=[DataRequired()])
    isSpecialCham = BooleanField('是否指定英雄')
    isChamAsses = BooleanField('是否为辅助英雄')
    submit = SubmitField('查询')


class ComboOrderForm(FlaskForm):
    title = StringField('订单标题', validators=[DataRequired()],id='currentLevelInput')
 #   desc = 