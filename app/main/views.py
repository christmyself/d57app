from . import main
from .. import db
from ..models import *
from flask import flash,url_for,session,render_template, redirect,request,jsonify
from .forms import NameForm,PeakAgentForm,QualifyingAgentForm,QualifyingPlaymateForm,SearchForm,ForceAgentForm
from datetime import datetime

@main.route('/autocomplete',methods=['GET'])
def autocomplete():
    levels=LevelComparison.query.all()
    labels  = []
    for level in levels:
        labels.append(level.label)
    return jsonify(json_list=labels) 

@main.route("/home", methods=["POST", "GET"])
def home():
    form = SearchForm(request.form)
    return render_template("search.html",form=form)


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', current_time=datetime.utcnow())

@main.route('/user', methods=['GET', 'POST'])
def user():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('main.user'))
    return render_template('user.html',
        form=form, name=session.get('name'),
        known=session.get('known', False))

@main.route('/peakAgent',methods = ['GET', 'POST'])
def peak():
    form = PeakAgentForm()
    result = ''
    if form.validate_on_submit():
        currentScore = form.current.data
        expectationScore = form.expectation.data
        if currentScore >= expectationScore:
            flash('目标级别必须比当前级别更高！')
            return redirect(url_for('main.peak'))
        score = expectationScore - currentScore
        money = compute_peak_agent_money(currentScore,expectationScore)
        result = '共需要提升' + str(score) + '分！费用为' + str(money) + '币！'
        print(form.isSpecialCham.data)
    return render_template('peak_agent.html',form=form,current_time=datetime.utcnow(),result = result)

@main.route('/qualifyingAgent',methods = ['GET', 'POST'])
def qualifyingAgent():
    form = QualifyingAgentForm()
    result = ''
    if form.validate_on_submit():
        currentLabel = form.current.data
        expectationLabel = form.expectation.data
        current = LevelComparison.query.filter_by(label=currentLabel).first()
        expectation = LevelComparison.query.filter_by(label=expectationLabel).first()
        if not current or not expectation:
            flash("请正确输入对应级别，比如输入白银，然后在弹出的引导框中选择想要的级别！")
            return redirect(url_for('main.qualifyingAgent'))
        currentLevel = current.level
        expectationLevel = expectation.level
        if currentLevel >= expectationLevel:
            print('current is:' + str(currentLevel) + 'expectation is:' + str(expectationLevel))
            flash('目标级别必须比当前级别更高！')
            return redirect(url_for('main.qualifyingAgent'))
        starCount = expectationLevel - currentLevel
        money = compute_qualifying_agent_money(currentLevel,expectationLevel)
        result = '你希望从' + currentLabel +'升级到' + expectationLabel +'需要' + str(starCount) + '颗星，费用为' + str(money) + '币！'
    return render_template('qualifying_agent.html',form=form,result = result)

@main.route('/qualifyingPlaymate',methods = ['GET', 'POST'])
def qualifyingPlaymate():
    form = QualifyingPlaymateForm()
    result = ''
    if form.validate_on_submit():
        currentLabel = form.current.data
        expectationLabel = form.expectation.data
        current = LevelComparison.query.filter_by(label=currentLabel).first()
        expectation = LevelComparison.query.filter_by(label=expectationLabel).first()
        if not current or not expectation:
            flash("请正确输入对应级别，比如输入白银，然后在弹出的引导框中选择想要的级别！")
            return redirect(url_for('main.qualifyingAgent'))
        currentLevel = current.level
        expectationLevel = expectation.level
        if currentLevel >= expectationLevel:
            print('current is:' + str(currentLevel) + 'expectation is:' + str(expectationLevel))
            flash('目标级别必须比当前级别更高！')
            return redirect(url_for('main.qualifyingAgent'))
        starCount = expectationLevel - currentLevel
        money = compute_qualifying_playmate_money(currentLevel,expectationLevel)
        result = '你希望从' + currentLabel +'陪玩到' + expectationLabel +'需要' + str(starCount) + '颗星，费用为' + str(money) + '币！'

    return render_template('qualifying_playmate.html',form=form,result=result)


@main.route('/force',methods = ['GET', 'POST'])
def force():
    form = ForceAgentForm()
    result = ''
    if form.validate_on_submit():
        currentScore = form.current.data
        expectationScore = form.expectation.data
        if currentScore >= expectationScore:
            flash('目标级别必须比当前级别更高！')
            return redirect(url_for('main.force'))
        score = expectationScore - currentScore
        money = compute_force_agent_money(currentScore,expectationScore)
        result = '共需要提升' + str(score) + '点战力！费用为' + str(money) + '币！'
        print(form.isSpecialCham.data)
    return render_template('force_agent.html',form=form,result=result)

@main.route('/combo')
def combo():
    combos = ComboProduct.query.all()
    return render_template('combo.html',combos = combos)

'''
@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)
'''

@main.route('/comboDeets/<id>',methods = ['GET'])
def comboDeets(id):
    combo = ComboProduct.query.get_or_404(id)
    print(id)
    return render_template('combo_deets.html',combo = combo)

